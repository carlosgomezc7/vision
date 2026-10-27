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
            title="Landing Page SEO & Typography Guide",
            category="Frontend",
            content="Guidelines for responsive typography hierarchy and OpenGraph metatags.",
            tags=["Typography", "SEO", "Next.js"],
            store=self.store
        )
        res = json.loads(res_str)
        assert res["status"] == "SUCCESS"
        assert res["title"] == "Landing Page SEO & Typography Guide"

        # Search using FTS5
        search_res = self.store.query_memory("Landing Page SEO", n_results=1)
        docs = search_res.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "Landing Page SEO" in docs[0]

    def test_get_architecture_blueprint(self):
        self.store.add_memory("arch_landing", "Blueprint: Next.js Modular Landing Page with Tailwind and shadcn", {"type": "architecture"})
        blueprint = get_architecture_blueprint("Next.js Modular Landing", store=self.store)
        assert "Next.js Modular Landing Page" in blueprint

    def test_record_lesson_learned(self):
        result = record_lesson_learned("Project Alfa", "Always audit WCAG 2.2 AA contrast on primary CTA buttons", store=self.store)
        assert "successfully recorded" in result

    def test_get_project_health_status(self):
        health_str = get_project_health_status(store=self.store)
        health = json.loads(health_str)
        assert "database" in health
        assert "knowledge_base" in health
        assert "git_status" in health
        assert health["database"]["integrity"] == "ok"

    def test_seed_vision_mind_execution(self):
        count = seed_vision_mind(store=self.store)
        assert count > 0
        # Query indexed seed
        res = self.store.query_memory("Landing Page", n_results=1)
        docs = res.get("documents", [[]])[0]
        assert len(docs) >= 1
