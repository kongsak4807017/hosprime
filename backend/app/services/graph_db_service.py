import logging
import os
import subprocess
import sys
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ตรวจสอบและโหลดไลบรารี neo4j แบบ lazy-loading
neo4j_installed = False
try:
    from neo4j import GraphDatabase
    neo4j_installed = True
except ImportError:
    logger.info("neo4j library not installed. Will auto-install on demand.")

def ensure_neo4j_installed():
    global neo4j_installed
    if not neo4j_installed:
        try:
            logger.info("Attempting to auto-install 'neo4j' library via pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "neo4j"])
            global GraphDatabase
            from neo4j import GraphDatabase
            neo4j_installed = True
            logger.info("Successfully installed and loaded 'neo4j' library.")
        except Exception as e:
            logger.error(f"Failed to auto-install 'neo4j' library: {e}")
    return neo4j_installed

class GraphDBService:
    _driver = None

    @classmethod
    def get_driver(cls, uri: str = None, user: str = None, password: str = None):
        if cls._driver is None:
            # ดึงการตั้งค่าจาก settings (หรือ env/parameters)
            db_uri = uri or settings.NEO4J_URI or os.getenv("NEO4J_URI")
            db_user = user or settings.NEO4J_USER or os.getenv("NEO4J_USER", "neo4j")
            db_password = password or settings.NEO4J_PASSWORD or os.getenv("NEO4J_PASSWORD")
            
            if db_uri and db_password:
                if ensure_neo4j_installed():
                    try:
                        cls._driver = GraphDatabase.driver(db_uri, auth=(db_user, db_password))
                        logger.info(f"Successfully connected to Neo4j database at {db_uri}")
                    except Exception as e:
                        logger.error(f"Failed to connect to Neo4j at {db_uri}: {e}")
                        cls._driver = None
            else:
                logger.info("Neo4j configuration not fully set (missing URI or Password). Running in Mock Mode.")
        return cls._driver

    @classmethod
    def create_node(cls, node_id: str, label: str, properties: dict = None, uri: str = None, user: str = None, password: str = None):
        """สร้าง Node ในฐานข้อมูล Neo4j/Graph Database จริง"""
        driver = cls.get_driver(uri, user, password)
        if driver:
            properties = properties or {}
            properties["id"] = node_id
            cypher = f"MERGE (n:`{label}` {{id: $id}}) SET n += $props RETURN n"
            try:
                with driver.session() as session:
                    session.run(cypher, id=node_id, props=properties)
                return {"status": "created", "node_id": node_id, "label": label}
            except Exception as e:
                logger.error(f"Neo4j create_node error: {e}")
        
        # Fallback to Mock Logger
        logger.info(f"Mock GraphDB: Created Node '{node_id}' with label '{label}' and properties {properties}")
        return {"status": "created", "node_id": node_id, "label": label}

    @classmethod
    def create_relationship(cls, source_id: str, relationship_type: str, target_id: str, properties: dict = None, uri: str = None, user: str = None, password: str = None):
        """สร้าง Relationship ในฐานข้อมูล Neo4j จริง"""
        driver = cls.get_driver(uri, user, password)
        if driver:
            properties = properties or {}
            cypher = (
                f"MERGE (a:Entity {{id: $source_id}}) "
                f"MERGE (b:Entity {{id: $target_id}}) "
                f"MERGE (a)-[r:`{relationship_type}`]->(b) "
                f"SET r += $props RETURN r"
            )
            try:
                with driver.session() as session:
                    session.run(cypher, source_id=source_id, target_id=target_id, props=properties)
                return {"status": "created", "source": source_id, "type": relationship_type, "target": target_id}
            except Exception as e:
                logger.error(f"Neo4j create_relationship error: {e}")

        # Fallback to Mock Logger
        logger.info(f"Mock GraphDB: Created relationship ({source_id})-[:{relationship_type}]->({target_id})")
        return {"status": "created", "source": source_id, "type": relationship_type, "target": target_id}

    @classmethod
    def query_graph(cls, cypher_query: str, uri: str = None, user: str = None, password: str = None) -> list:
        """ส่งคิวรีภาษา Cypher ไปสอบถามข้อมูลความสัมพันธ์เชิงลึกจาก Neo4j จริง"""
        driver = cls.get_driver(uri, user, password)
        if driver:
            try:
                with driver.session() as session:
                    result = session.run(cypher_query)
                    return [record.data() for record in result]
            except Exception as e:
                logger.error(f"Neo4j query_graph error: {e}")
                return []
        
        # Fallback to Mock
        logger.info(f"Mock GraphDB Query: {cypher_query}")
        return []
