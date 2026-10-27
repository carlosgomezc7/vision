import sys
import json
import tempfile
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.memory.vector_store import VisionMemoryStore
from src.tools.project_specs import create_landing_page_spec


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

    def test_create_landing_page_spec_complete(self):
        spec_str = create_landing_page_spec(
            company_name="Grupo Alfa",
            sections=["Hero", "Servicios", "Nosotros", "Testimonios", "Contacto"],
            cta_goal="Agendar una auditoría gratuita",
            style_adjectives=["moderno", "limpio", "elegante"],
            palette_hex=["#0F172A", "#3B82F6", "#FFFFFF"],
            typography=["Inter", "sans-serif"],
            contact_channels=["WhatsApp", "Formulario Web"],
            store=self.store
        )
        spec = json.loads(spec_str)
        assert spec["client"] == "Grupo Alfa"
        assert "Landing Page" in spec["project_type"]
        assert "Header.tsx" in spec["component_structure"]["Header"]["file"]
        assert "Hero.tsx" in spec["component_structure"]["Hero"]["file"]
        assert "Footer.tsx" in spec["component_structure"]["Footer"]["file"]
        assert spec["primary_cta_goal"] == "Agendar una auditoría gratuita"
        assert spec["color_palette_hex"] == ["#0F172A", "#3B82F6", "#FFFFFF"]
        assert "Cero dependencias de autenticación" in spec["rules"][4]

        # Verify saved in memory store
        mem = self.store.query_memory("Grupo Alfa Landing", n_results=1)
        docs = mem.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "Grupo Alfa" in docs[0]

    def test_create_landing_page_spec_defaults(self):
        spec_str = create_landing_page_spec(
            company_name="Pastelería Dulce",
            store=self.store
        )
        spec = json.loads(spec_str)
        assert spec["client"] == "Pastelería Dulce"
        assert "Hero" in spec["required_sections"]
        assert len(spec["component_structure"]) >= 4
