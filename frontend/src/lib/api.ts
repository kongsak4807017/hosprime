const API_BASE_URL = ((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api';


export interface UserResponse {
  id: number;
  username: string;
  role: string;
  department: string | null;
  confidentiality_level: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: UserResponse;
}

export interface DocumentResponse {
  id: number;
  title: string;
  document_type: string | null;
  department: string | null;
  program: string | null;
  year: string | null;
  owner: string | null;
  confidentiality_level: string;
  file_path: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface SourceChunkInfo {
  document_id: number;
  document_title: string;
  chunk_id: number;
  chunk_text: string;
  page_number: number | null;
  section_title: string | null;
  score: number;
}

export interface QueryResponse {
  answer: string;
  sources: SourceChunkInfo[];
  confidence: number;
  query_log_id: number;
}

export interface QueryLogResponse {
  id: number;
  user_id: string;
  question: string;
  answer: string;
  sources: {
    document_id: number;
    document_title: string;
    page_number: number | null;
    section_title: string | null;
    score: number;
  }[] | null;
  confidence: number;
  feedback: string | null;
  created_at: string;
}

export interface EntityRelationResponse {
  id: number;
  document_id: number;
  source_node: string;
  relation_type: string;
  target_node: string;
  source_type: string | null;
  target_type: string | null;
  confidence: number;
  extracted_at: string;
}

function getHeaders(extraHeaders: Record<string, string> = {}): Record<string, string> {
  const headers: Record<string, string> = { ...extraHeaders };
  const token = localStorage.getItem('hosprime_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export const api = {
  async login(username: string, password: string): Promise<TokenResponse> {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง');
    }
    const data: TokenResponse = await res.json();
    localStorage.setItem('hosprime_token', data.access_token);
    localStorage.setItem('hosprime_user', JSON.stringify(data.user));
    return data;
  },

  async register(username: string, password: string, role: string, department?: string): Promise<UserResponse> {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ username, password, role, department }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'การลงทะเบียนล้มเหลว');
    }
    return res.json();
  },

  async getMe(): Promise<UserResponse> {
    const res = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch user profile');
    return res.json();
  },

  logout() {
    localStorage.removeItem('hosprime_token');
    localStorage.removeItem('hosprime_user');
  },

  getCurrentUser(): UserResponse | null {
    const userStr = localStorage.getItem('hosprime_user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },

  async askOracle(question: string, userId: string = 'guest'): Promise<QueryResponse> {
    const res = await fetch(`${API_BASE_URL}/oracle/ask`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ question, user_id: userId }),
    });
    if (!res.ok) throw new Error('Failed to ask Oracle');
    return res.json();
  },

  async uploadDocument(file: File, title?: string, confidentialityLevel: string = 'Internal'): Promise<DocumentResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);
    formData.append('confidentiality_level', confidentialityLevel);

    const res = await fetch(`${API_BASE_URL}/documents/upload`, {
      method: 'POST',
      headers: getHeaders(),
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to upload document');
    }
    return res.json();
  },

  async getCatalog(filters?: {
    document_type?: string;
    department?: string;
    program?: string;
    status?: string;
  }): Promise<DocumentResponse[]> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, val]) => {
        if (val) params.append(key, val);
      });
    }
    const res = await fetch(`${API_BASE_URL}/documents/catalog?${params.toString()}`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch catalog');
    return res.json();
  },

  async getDocumentRelations(docId: number): Promise<EntityRelationResponse[]> {
    const res = await fetch(`${API_BASE_URL}/documents/${docId}/relations`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch relations');
    return res.json();
  },

  async deleteDocument(docId: number): Promise<void> {
    const res = await fetch(`${API_BASE_URL}/documents/${docId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to delete document');
  },

  async getPendingDocuments(): Promise<DocumentResponse[]> {
    const res = await fetch(`${API_BASE_URL}/admin/pending`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch pending documents');
    return res.json();
  },

  async updateDocumentMetadata(docId: number, metadata: Partial<DocumentResponse>): Promise<DocumentResponse> {
    const res = await fetch(`${API_BASE_URL}/admin/documents/${docId}`, {
      method: 'PUT',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(metadata),
    });
    if (!res.ok) throw new Error('Failed to update metadata');
    return res.json();
  },

  async reviewDocument(docId: number, action: 'approve' | 'reject', metadata?: any): Promise<DocumentResponse> {
    const res = await fetch(`${API_BASE_URL}/admin/documents/${docId}/review`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ action, metadata }),
    });
    if (!res.ok) throw new Error('Failed to review document');
    return res.json();
  },

  async getQueryLogs(): Promise<QueryLogResponse[]> {
    const res = await fetch(`${API_BASE_URL}/oracle/logs`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch query logs');
    return res.json();
  },

  async submitFeedback(logId: number, feedback: 'positive' | 'negative'): Promise<void> {
    const res = await fetch(`${API_BASE_URL}/oracle/logs/${logId}/feedback`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ feedback }),
    });
    if (!res.ok) throw new Error('Failed to submit feedback');
  },

  // Meetings API
  async getMeetings(): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/meetings/list`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch meetings');
    return res.json();
  },

  // Twins API
  async getTwinProfile(): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/profile`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch twin profile');
    return res.json();
  },

  async draftTwinLetter(prompt: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/draft-letter?prompt=${encodeURIComponent(prompt)}`, {
      method: 'POST',
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to draft letter');
    return res.json();
  },

  // Graph API
  async getGraphNetwork(): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/graph/network`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch graph network');
    return res.json();
  },

  // Workflows API
  async getLatestWorkflowStatus(): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/workflows/status/latest`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch workflow status');
    return res.json();
  },

  async triggerWorkflow(location: string, level: string, maskQty: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/workflows/trigger?workflow_name=DisasterAlert`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ location, level, mask_qty: maskQty }),
    });
    if (!res.ok) throw new Error('Failed to trigger workflow');
    return res.json();
  },

  async approveWorkflow(workflowId: string | number): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/workflows/approve/${workflowId}`, {
      method: 'POST',
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to approve workflow');
    return res.json();
  },

  async migrateSystem(data: {
    db_migration: boolean;
    postgres_url?: string;
    graph_migration: boolean;
    neo4j_uri?: string;
    neo4j_user?: string;
    neo4j_password?: string;
  }): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/admin/migrate`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'ระบบการย้ายข้อมูลขัดข้อง');
    }
    return res.json();
  },

  async uploadMeetingDocument(meetingId: number, file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/meetings/${meetingId}/upload-document`, {
      method: 'POST',
      headers: getHeaders(),
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to upload meeting document');
    }
    return res.json();
  },

  async askMeetingOracle(meetingId: number, question: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/meetings/${meetingId}/ask`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ question }),
    });
    if (!res.ok) throw new Error('Failed to query meeting RAG');
    return res.json();
  },

  async getRoles(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/twins/roles`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch roles');
    return res.json();
  },

  async getOrganizations(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/twins/organizations`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch organizations');
    return res.json();
  },

  async createOrganization(org: any): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/organizations`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(org),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to create organization');
    }
    return res.json();
  },

  async deleteOrganization(orgId: number): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/organizations/${orgId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to delete organization');
    return res.json();
  },

  async getPersons(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/twins/persons`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch persons');
    return res.json();
  },

  async createRole(role: any): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/roles`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(role),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to create role');
    }
    return res.json();
  },

  async createPerson(person: any): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/persons`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(person),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to create person');
    }
    return res.json();
  },

  async deleteRole(roleId: number): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/roles/${roleId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to delete role');
    return res.json();
  },

  async deletePerson(personId: number): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/persons/${personId}`, {
      method: 'DELETE',
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to delete person');
    return res.json();
  },

  async getAdminAgentSummary(): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/admin/agent-summary`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch admin agent summary');
    return res.json();
  },

  async getAgentLogs(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/admin/agent-logs`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch agent logs');
    return res.json();
  },

  async getAgents(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/twins/agents`, {
      headers: getHeaders(),
    });
    if (!res.ok) throw new Error('Failed to fetch AI agents');
    return res.json();
  },

  async updateAgent(agentId: string, payload: { is_active?: boolean; temperature?: number; token_quota?: number; model_name?: string }): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/agents/${agentId}`, {
      method: 'PUT',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to update AI Agent configurations');
    }
    return res.json();
  },

  async installAgentPack(packId: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/install-pack`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ pack_id: packId }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to install Agent Pack');
    }
    return res.json();
  },

  async simulateTwinMetrics(opdLoad: number, icuBeds: number, staffFte: number): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/simulate`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ opd_load: opdLoad, icu_beds: icuBeds, staff_fte: staffFte }),
    });
    if (!res.ok) throw new Error('Failed to simulate metrics');
    return res.json();
  },

  async orchestrateEnterpriseFlow(goal: string): Promise<any> {
    const res = await fetch(`${API_BASE_URL}/twins/orchestrate`, {
      method: 'POST',
      headers: getHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ goal }),
    });
    if (!res.ok) throw new Error('Failed to orchestrate enterprise flow');
    return res.json();
  },
};

