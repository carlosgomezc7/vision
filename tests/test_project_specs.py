import sys
import json
import tempfile
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.memory.vector_store import VisionMemoryStore
from src.tools.project_specs import create_landing_page_spec, generate_supabase_rls_policies


class TestProjectSpecs:
    def setup_method(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_specs.db")
        self.store = VisionMemoryStore(db_path=self.db_path)

    def teardown_method(self):
        for ext in ["", "-wal", "-shm"]:
            p = self.db_path + ext
            if os.path.exists(p):
                os.remove(p)
        os.rmdir(self.tmp_dir)

    def test_create_landing_page_spec(self):
        spec_str = create_landing_page_spec(
            company_name="Grupo Alfa",
            sections=["Hero", "Servicios", "Nosotros", "Contacto"],
            cta_goal="Agendar una auditoría gratuita",
            style_adjectives=["moderno", "seguro"],
            store=self.store
        )
        spec = json.loads(spec_str)
        assert spec["client"] == "Grupo Alfa"
        assert "Bifurcation A" in spec["architecture_branch"]
        assert "src/components/landing/Hero.tsx" in spec["component_structure"]["Hero"]["file"]
        assert spec["primary_cta_goal"] == "Agendar una auditoría gratuita"

        # Verify saved in memory store
        mem = self.store.query_memory("Grupo Alfa", n_results=1)
        docs = mem.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "Grupo Alfa" in docs[0]

    def test_generate_supabase_rls_policies(self):
        sql = generate_supabase_rls_policies(
            company_name="Acme Corp",
            modules=["announcements", "tickets"],
            roles=["admin", "lead", "employee"]
        )
        assert "user_role AS ENUM" in sql
        assert "public.profiles" in sql
        assert "ENABLE ROW LEVEL SECURITY" in sql
        assert "public.intranet_announcements" in sql
        assert "public.intranet_tickets" in sql
        assert "Authenticated employees can read" in sql
