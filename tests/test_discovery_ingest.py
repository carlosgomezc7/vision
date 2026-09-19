import sys
import json
import tempfile
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.memory.vector_store import VisionMemoryStore
from src.tools.discovery_ingest import ingest_discovery_data


class TestDiscoveryIngest:
    def setup_method(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.tmp_dir, "test_discovery.db")
        self.store = VisionMemoryStore(db_path=self.db_path)

    def teardown_method(self):
        for ext in ["", "-wal", "-shm"]:
            p = self.db_path + ext
            if os.path.exists(p):
                os.remove(p)
        os.rmdir(self.tmp_dir)

    def test_ingest_structured_discovery_payload(self):
        payload = {
            "business_profile": {
                "company_name": {"value": "InnovaTech", "certainty": "reported"},
                "business_sector": {"value": "Fintech", "certainty": "reported"},
                "primary_goal": {"value": "Portal de Clientes", "certainty": "reported"},
                "value_proposition": {"value": "Transacciones bancarias seguras", "certainty": "reported"}
            },
            "branding_assets": {
                "color_palette": {
                    "hex_codes": {"value": ["#0F172A", "#38BDF8"], "certainty": "reported"}
                },
                "typography": {
                    "font_families": {"value": ["Inter", "Roboto Mono"], "certainty": "reported"}
                },
                "style_adjectives": {"value": ["minimalista", "tecnológico"], "certainty": "reported"}
            },
            "technical_scope": {
                "estimated_pages": {"value": 8, "certainty": "reported"},
                "required_integrations": {"value": ["Stripe", "OAuth"], "certainty": "reported"},
                "preferred_cms": {"value": "Next.js", "certainty": "reported"}
            },
            "infrastructure": {
                "domain_name": {"value": "innovatech.io", "certainty": "reported"},
                "hosting_preference": {"value": "AWS ECS", "certainty": "reported"}
            }
        }

        res_str = ingest_discovery_data(payload, store=self.store)
        res = json.loads(res_str)
        assert res["status"] == "INGESTED_SUCCESSFULLY"
        assert res["client"] == "InnovaTech"
        assert res["business_sector"] == "Fintech"
        assert "#38BDF8" in res["branding"]["palette_hex"]

        # Verify indexed in memory
        mem = self.store.query_memory("InnovaTech Fintech", n_results=1)
        docs = mem.get("documents", [[]])[0]
        assert len(docs) == 1
        assert "InnovaTech" in docs[0]
