# HosPRIME - Deployment & Operations Requirements

## 1. Overview

This document outlines the deployment architecture, operational requirements, monitoring strategies, and maintenance procedures for HosPRIME.

## 2. Deployment Environments

### 2.1 Environment Strategy

HosPRIME follows a **4-environment deployment model**:

```
Development → Staging → Pre-Production → Production
```

**Environment Specifications:**

| Aspect | Development | Staging | Pre-Production | Production |
|--------|-------------|---------|----------------|------------|
| **Purpose** | Active development | Feature testing | Final validation | Live system |
| **Data** | Mock/Test data | Anonymized real data | Anonymized real data | Real data |
| **Users** | Developers | QA Team | Selected users | All users |
| **Uptime SLA** | N/A | 95% | 99% | 99.9% |
| **Backup** | None | Daily | Daily | Hourly |
| **Monitoring** | Basic | Standard | Full | Full + Alerts |
| **Access** | All developers | Authorized only | Limited | Limited |

### 2.2 Infrastructure Requirements

#### Development Environment

**Local Development (Developer Machine):**
```yaml
Minimum Hardware:
  CPU: 4 cores
  RAM: 16 GB
  Disk: 100 GB SSD
  
Software:
  - Docker & Docker Compose
  - Node.js 18+
  - Python 3.11+
  - Git
  - VS Code / IDE

Services (Docker Compose):
  - MongoDB (port 27017)
  - Neo4j (port 7687, 7474)
  - Redis (port 6379) [future]
  - Backend (port 8001)
  - Frontend (port 3000)
```

#### Production Environment

**Cloud Infrastructure (AWS/GCP/Azure):**

```yaml
Compute:
  Frontend:
    - Instance Type: t3.medium (2 vCPU, 4 GB RAM)
    - Count: 3 instances (load balanced)
    - Auto-scaling: Min 3, Max 10
    
  Backend:
    - Instance Type: t3.large (2 vCPU, 8 GB RAM)
    - Count: 5 instances (load balanced)
    - Auto-scaling: Min 5, Max 20
    
  AI/ML Service:
    - Instance Type: c5.2xlarge (8 vCPU, 16 GB RAM)
    - Count: 2 instances
    - GPU: Optional (for heavy ML workloads)

Database:
  MongoDB:
    - Instance Type: r5.xlarge (4 vCPU, 32 GB RAM)
    - Replica Set: 3 nodes (Primary + 2 Secondaries)
    - Storage: 500 GB SSD (expandable to 2 TB)
    - IOPS: 3000 provisioned
    
  Neo4j:
    - Instance Type: r5.large (2 vCPU, 16 GB RAM)
    - Count: 1 (3 for HA)
    - Storage: 200 GB SSD
    
  Redis (Cache):
    - Instance Type: cache.m5.large (2 vCPU, 6.38 GB RAM)
    - Count: 1 (2 with replication)

Load Balancer:
  - Application Load Balancer (ALB)
  - SSL/TLS termination
  - Health checks enabled
  - Cross-zone load balancing

Storage:
  - Object Storage (S3/GCS): 1 TB (for documents, images, backups)
  - EBS Volumes: Encrypted, daily snapshots

Networking:
  - VPC with public and private subnets
  - NAT Gateway for outbound traffic
  - Security Groups / Firewall rules
  - VPN for admin access
```

**Total Infrastructure Cost Estimate:**
- Development: ~$200/month
- Staging: ~$500/month
- Production: ~$3,000-$5,000/month (depending on scale)

## 3. Deployment Architecture

### 3.1 Container Architecture

**Docker Images:**

```dockerfile
# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8001"]
```

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine AS build

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**Docker Compose (Development):**

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongo_data:/data/db
  
  neo4j:
    image: neo4j:5
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      NEO4J_AUTH: neo4j/password
    volumes:
      - neo4j_data:/data
  
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      MONGO_URL: mongodb://admin:password@mongodb:27017
      NEO4J_URI: bolt://neo4j:7687
    depends_on:
      - mongodb
      - neo4j
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_BACKEND_URL: http://localhost:8001
    depends_on:
      - backend
    volumes:
      - ./frontend/src:/app/src

volumes:
  mongo_data:
  neo4j_data:
```

### 3.2 Kubernetes Deployment (Production)

**Kubernetes Resources:**

```yaml
# backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hosprime-backend
spec:
  replicas: 5
  selector:
    matchLabels:
      app: hosprime-backend
  template:
    metadata:
      labels:
        app: hosprime-backend
    spec:
      containers:
      - name: backend
        image: hosprime/backend:latest
        ports:
        - containerPort: 8001
        env:
        - name: MONGO_URL
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: mongo_url
        - name: EMERGENT_LLM_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: emergent_key
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: hosprime-backend
spec:
  selector:
    app: hosprime-backend
  ports:
  - protocol: TCP
    port: 8001
    targetPort: 8001
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hosprime-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hosprime-backend
  minReplicas: 5
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

```yaml
# frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hosprime-frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hosprime-frontend
  template:
    metadata:
      labels:
        app: hosprime-frontend
    spec:
      containers:
      - name: frontend
        image: hosprime/frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: hosprime-frontend
spec:
  selector:
    app: hosprime-frontend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: LoadBalancer
```

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hosprime-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - hosprime.example.com
    secretName: hosprime-tls
  rules:
  - host: hosprime.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: hosprime-backend
            port:
              number: 8001
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hosprime-frontend
            port:
              number: 80
```

### 3.3 Database Deployment

**MongoDB Replica Set (Kubernetes):**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb
spec:
  serviceName: mongodb
  replicas: 3
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:6
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: username
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mongodb-secret
              key: password
        volumeMounts:
        - name: mongodb-data
          mountPath: /data/db
  volumeClaimTemplates:
  - metadata:
      name: mongodb-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 500Gi
      storageClassName: fast-ssd
```

## 4. CI/CD Pipeline

### 4.1 Continuous Integration

**GitHub Actions Workflow:**

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run linters
        run: |
          cd backend
          black --check .
          isort --check .
          flake8 .
      
      - name: Run tests
        run: |
          cd backend
          pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          yarn install
      
      - name: Run linters
        run: |
          cd frontend
          yarn lint
      
      - name: Run tests
        run: |
          cd frontend
          yarn test --coverage
      
      - name: Build
        run: |
          cd frontend
          yarn build
  
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
```

### 4.2 Continuous Deployment

**Deployment Workflow:**

```yaml
# .github/workflows/cd.yml
name: CD Pipeline

on:
  push:
    branches: [main]
    tags:
      - 'v*'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to ECR
        run: |
          aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${{ secrets.ECR_REGISTRY }}
      
      - name: Build and push backend image
        run: |
          cd backend
          docker build -t ${{ secrets.ECR_REGISTRY }}/hosprime-backend:${{ github.sha }} .
          docker tag ${{ secrets.ECR_REGISTRY }}/hosprime-backend:${{ github.sha }} ${{ secrets.ECR_REGISTRY }}/hosprime-backend:latest
          docker push ${{ secrets.ECR_REGISTRY }}/hosprime-backend:${{ github.sha }}
          docker push ${{ secrets.ECR_REGISTRY }}/hosprime-backend:latest
      
      - name: Build and push frontend image
        run: |
          cd frontend
          docker build -t ${{ secrets.ECR_REGISTRY }}/hosprime-frontend:${{ github.sha }} .
          docker tag ${{ secrets.ECR_REGISTRY }}/hosprime-frontend:${{ github.sha }} ${{ secrets.ECR_REGISTRY }}/hosprime-frontend:latest
          docker push ${{ secrets.ECR_REGISTRY }}/hosprime-frontend:${{ github.sha }}
          docker push ${{ secrets.ECR_REGISTRY }}/hosprime-frontend:latest
      
      - name: Deploy to Kubernetes
        run: |
          aws eks update-kubeconfig --name hosprime-cluster --region us-east-1
          kubectl set image deployment/hosprime-backend backend=${{ secrets.ECR_REGISTRY }}/hosprime-backend:${{ github.sha }}
          kubectl set image deployment/hosprime-frontend frontend=${{ secrets.ECR_REGISTRY }}/hosprime-frontend:${{ github.sha }}
          kubectl rollout status deployment/hosprime-backend
          kubectl rollout status deployment/hosprime-frontend
      
      - name: Run smoke tests
        run: |
          ./scripts/smoke-tests.sh
```

### 4.3 Deployment Strategies

**Blue-Green Deployment:**
```
1. Deploy new version (Green) alongside current version (Blue)
2. Run tests on Green environment
3. Switch traffic from Blue to Green
4. Monitor for issues
5. Keep Blue as rollback option for 24 hours
6. Decommission Blue if no issues
```

**Rolling Deployment:**
```
1. Update pods one at a time
2. Wait for new pod to be ready
3. Health check before proceeding to next pod
4. Automatic rollback if health checks fail
```

**Canary Deployment:**
```
1. Deploy new version to 10% of traffic
2. Monitor metrics (error rate, latency)
3. Gradually increase traffic: 25% → 50% → 100%
4. Rollback if metrics degrade
```

## 5. Monitoring & Observability

### 5.1 Application Monitoring

**Metrics to Monitor:**

```yaml
Application Metrics:
  - Request rate (requests/second)
  - Response time (p50, p95, p99)
  - Error rate (%)
  - Active users
  - Database query time
  - API endpoint performance
  - LLM API calls and latency

Business Metrics:
  - New patient registrations/day
  - Appointments booked/day
  - Prescriptions issued/day
  - Revenue generated/day
  - User satisfaction score

Infrastructure Metrics:
  - CPU utilization (%)
  - Memory utilization (%)
  - Disk I/O
  - Network throughput
  - Pod/container restarts
  - Database connections
```

**Monitoring Stack (Prometheus + Grafana):**

```yaml
# prometheus-config.yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'hosprime-backend'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: hosprime-backend
  
  - job_name: 'mongodb'
    static_configs:
      - targets: ['mongodb-exporter:9216']
  
  - job_name: 'neo4j'
    static_configs:
      - targets: ['neo4j-exporter:9100']
```

**Grafana Dashboards:**
- System Overview Dashboard
- Application Performance Dashboard
- Database Performance Dashboard
- Business Metrics Dashboard
- Error Tracking Dashboard

### 5.2 Logging

**Centralized Logging (ELK Stack):**

```yaml
Log Sources:
  - Application logs (FastAPI, React)
  - Access logs (Nginx)
  - Database logs (MongoDB, Neo4j)
  - System logs (Kubernetes)
  - Audit logs (Security events)

Log Processing Pipeline:
  1. Collect logs (Filebeat / Fluentd)
  2. Parse and enrich (Logstash)
  3. Index (Elasticsearch)
  4. Visualize (Kibana)

Log Retention:
  - Application logs: 30 days
  - Access logs: 90 days
  - Audit logs: 7 years
  - Error logs: 1 year
```

**Structured Logging Format:**
```json
{
  "timestamp": "2026-06-12T10:30:00Z",
  "level": "INFO",
  "service": "hosprime-backend",
  "module": "patient_service",
  "message": "Patient created successfully",
  "patient_id": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "98765432-e89b-12d3-a456-426614174001",
  "duration_ms": 145,
  "request_id": "req_abc123"
}
```

### 5.3 Alerting

**Alert Rules:**

```yaml
Critical Alerts (Immediate - PagerDuty):
  - Service down (no response for 2 minutes)
  - Error rate > 10%
  - Database connection failures
  - Disk space > 90%
  - Memory utilization > 95%

High Priority Alerts (15 min response):
  - Error rate > 5%
  - Response time p95 > 2 seconds
  - High CPU usage > 80% for 10 minutes
  - Failed backups
  - SSL certificate expiring in 7 days

Medium Priority Alerts (1 hour response):
  - Error rate > 2%
  - Response time p95 > 1 second
  - Unusual traffic patterns
  - High database query times

Low Priority Alerts (Next business day):
  - Deprecation warnings
  - Non-critical configuration changes
  - Performance degradation < 10%
```

**Alert Channels:**
- PagerDuty (Critical)
- Slack (High/Medium)
- Email (Low)
- SMS (Critical, after hours)

### 5.4 Distributed Tracing

**Jaeger Tracing:**

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracing
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# Trace requests
@tracer.start_as_current_span("create_patient")
async def create_patient(data: PatientCreate):
    with tracer.start_as_current_span("validate_data"):
        validate(data)
    
    with tracer.start_as_current_span("save_to_db"):
        patient = await db.patients.insert_one(data.dict())
    
    return patient
```

## 6. Backup & Disaster Recovery

### 6.1 Backup Strategy

**MongoDB Backup:**

```bash
#!/bin/bash
# backup-mongodb.sh

BACKUP_DIR="/backups/mongodb/$(date +%Y%m%d_%H%M%S)"
S3_BUCKET="s3://hosprime-backups/mongodb"

# Full backup
mongodump --uri="$MONGO_URL" --out="$BACKUP_DIR" --gzip

# Upload to S3
aws s3 sync "$BACKUP_DIR" "$S3_BUCKET/$(date +%Y%m%d_%H%M%S)" --storage-class STANDARD_IA

# Cleanup local backups older than 7 days
find /backups/mongodb -type d -mtime +7 -exec rm -rf {} +

# Cleanup S3 backups older than 30 days (lifecycle policy)
```

**Backup Schedule:**
- **Full Backup**: Daily at 2 AM
- **Incremental Backup**: Hourly
- **Continuous Backup**: MongoDB Change Streams (future)

**Backup Retention:**
- Daily backups: 30 days
- Weekly backups: 3 months
- Monthly backups: 1 year
- Yearly backups: 7 years

### 6.2 Disaster Recovery Plan

**Recovery Objectives:**
- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 1 hour

**DR Procedures:**

```markdown
## Disaster Recovery Runbook

### Scenario 1: Complete System Failure

1. Declare Disaster (5 minutes)
   - Assess situation
   - Notify stakeholders
   - Activate DR team

2. Spin Up DR Environment (30 minutes)
   - Launch compute instances
   - Configure networking
   - Deploy Kubernetes cluster

3. Restore Databases (2 hours)
   - Restore MongoDB from latest backup
   - Restore Neo4j from latest backup
   - Verify data integrity

4. Deploy Application (1 hour)
   - Deploy backend services
   - Deploy frontend
   - Run smoke tests

5. Switch Traffic (15 minutes)
   - Update DNS records
   - Verify routing
   - Monitor errors

6. Verify & Monitor (30 minutes)
   - End-to-end testing
   - Monitor metrics
   - Communicate status

Total Time: ~4 hours
```

### 6.3 Rollback Procedures

**Application Rollback:**
```bash
# Kubernetes rollback
kubectl rollout undo deployment/hosprime-backend
kubectl rollout undo deployment/hosprime-frontend

# Verify rollback
kubectl rollout status deployment/hosprime-backend
```

**Database Rollback:**
```bash
# Restore from specific backup
mongorestore --uri="$MONGO_URL" --gzip --drop /backups/mongodb/20260612_020000
```

## 7. Operational Procedures

### 7.1 Daily Operations

**Daily Checklist:**
- [ ] Check system health dashboard
- [ ] Review overnight alerts
- [ ] Verify backup completion
- [ ] Check error logs for anomalies
- [ ] Monitor database performance
- [ ] Review user-reported issues

### 7.2 Weekly Operations

**Weekly Tasks:**
- [ ] Review system performance trends
- [ ] Analyze error patterns
- [ ] Security vulnerability scan
- [ ] Update documentation
- [ ] Capacity planning review
- [ ] Team sync meeting

### 7.3 Monthly Operations

**Monthly Tasks:**
- [ ] Full security audit
- [ ] Disaster recovery drill
- [ ] Performance optimization review
- [ ] Cost optimization analysis
- [ ] User feedback review
- [ ] Vendor patch updates

## 8. Maintenance Windows

**Scheduled Maintenance:**
- **Frequency**: Monthly (last Sunday of the month)
- **Time**: 2 AM - 6 AM (low traffic period)
- **Duration**: 4 hours maximum
- **Notification**: 7 days advance notice to users

**Maintenance Activities:**
- Database maintenance (reindexing, optimization)
- Security patches
- Infrastructure updates
- Major version upgrades

## 9. Capacity Planning

**Growth Projections:**

```yaml
Current Capacity (Year 1):
  Patients: 10,000
  Daily Appointments: 500
  Daily Transactions: 5,000
  Storage: 500 GB

Year 2:
  Patients: 25,000 (2.5x)
  Daily Appointments: 1,250
  Daily Transactions: 12,500
  Storage: 1.2 TB
  Infrastructure: Scale compute by 2x

Year 3:
  Patients: 50,000 (5x)
  Daily Appointments: 2,500
  Daily Transactions: 25,000
  Storage: 2.5 TB
  Infrastructure: Scale compute by 4x
```

**Scaling Triggers:**
- CPU utilization > 70% sustained
- Memory utilization > 80%
- Database storage > 80% capacity
- Response time degradation > 20%

## 10. Cost Optimization

**Cost Management Strategies:**

1. **Right-sizing**: Match instance types to workload
2. **Auto-scaling**: Scale down during off-peak hours
3. **Reserved Instances**: 30-50% savings for predictable workloads
4. **Spot Instances**: Use for non-critical batch jobs
5. **Storage Tiering**: Move old data to cheaper storage
6. **CDN Caching**: Reduce bandwidth costs
7. **Database Query Optimization**: Reduce compute costs

**Monthly Cost Breakdown (Estimated):**

```
Compute (EC2/GKE): $1,500
Database (RDS/MongoDB Atlas): $800
Storage (S3/GCS): $200
Network (Data Transfer): $300
Load Balancer: $50
Monitoring (CloudWatch/Stackdriver): $100
Backups: $150
LLM API Calls: $400
Miscellaneous: $200

Total: ~$3,700/month
```

---

*Document Version: 1.0*
*Last Updated: June 2026*