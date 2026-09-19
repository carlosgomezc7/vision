import sys
import json
import tempfile
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.memory.vector_store import VisionMemoryStore
from src.memory.seeder import seed_vision_mind
from src.tools.knowledge_tool import ingest_knowledge_document
from src.tools.devops_tool import get_project_health_status, trigger_git_checkpoint
from src.tools.prd_intranet import generate_intranet_prd
from src.tools.architecture_tool import get_architecture_blueprint
from src.tools.retrospect_tool import record_lesson_learned


class TestKnowledgeAndDevops:
    def setup_method(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_integration.db")
        self.store = VisionMemoryStore(db_path=self.db_path)

    def teardown_method(self):
        for ext in ["", "-wal", "-shm"]:
            p = self.db_path + ext
            if os.path.exists(p):
                os.remove(p)
        os.rmdir(self.tmp_dir)

    def test_ingest_knowledge_document(self):
        res_str = ingest_knowledge_document(
            title="Active Directory GPO Guide",
            category="Infrastructure",
            content="Guidelines for mapping Active Directory groups to Intranet RBAC roles.",
            tags=["AD", "Security", "ZeroTrust"],
            store=self.store
        )
        res = json.loads(res_str)
        assert res["status"] == "SUCCESS"
        assert res["title"] == "Active Directory GPO Guide"

        # Search using FTS5
        search_res = self.store.query_memory("Active Directory GPO", n_results=1)
        docs = search_res.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "Active Directory GPO Guide" in docs[0]

    def test_generate_intranet_prd(self):
        prd_str = generate_intranet_prd(
            company_name="Soluciones Globales",
            employee_count=350,
            modules=["deep_search", "announcements", "directory"],
            sso_provider="Azure AD",
            store=self.store
        )
        prd = json.loads(prd_str)
        assert prd["client"] == "Soluciones Globales"
        assert prd["employees"] == 350
        assert prd["sso_provider"] == "Azure AD"
        assert "deep_search" in prd["required_modules"]

    def test_get_architecture_blueprint(self):
        self.store.add_memory("arch_rbac", "Blueprint: Zero Trust RBAC with Supabase", {"type": "architecture"})
        blueprint = get_architecture_blueprint("Zero Trust RBAC", store=self.store)
        assert "Zero Trust RBAC with Supabase" in blueprint

    def test_record_lesson_learned(self):
        result = record_lesson_learned("Project Beta", "Always configure WAL mode in SQLite for multi-agent concurrency", store=self.store)
        assert "successfully recorded" in result

    def test_get_project_health_status(self):
        health_str = get_project_health_status(store=self.store)
        health = json.loads(health_str)
        assert "database" in health
        assert "knowledge_base" in health
        assert "git_status" in health
        assert health["database"]["integrity"] == "ok"
        assert health["knowledge_base"]["seed_files_count"] == 13

    def test_seed_vision_mind_execution(self):
        count = seed_vision_mind(store=self.store)
        assert count == 13
        # Query indexed seed
        res = self.store.query_memory("Deep Search RAG", n_results=1)
        docs = res.get("documents", [[]])[0]
        assert len(docs) >= 1
        assert "Deep Search" in docs[0]


