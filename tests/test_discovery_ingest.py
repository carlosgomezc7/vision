import sys
import json
import tempfile
import os
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.memory.vector_store import VisionMemoryStore
from src.tools.discovery_ingest import (
    ingest_discovery_data,
    audit_client_readiness,
    get_client_intake_guide,
)


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
            "perfil_negocio": {
                "nombre_empresa": {"valor": "InnovaTech", "certeza": "reported"},
                "sector_industria": {"valor": "Fintech", "certeza": "reported"},
                "objetivo_principal_landing": {"valor": "Captar Leads", "certeza": "reported"},
                "propuesta_de_valor": {"valor": "Transacciones bancarias seguras", "certeza": "reported"}
            },
            "identidad_visual_y_marca": {
                "paleta_de_colores": {
                    "colores_deseados_hex": {"valor": ["#0F172A", "#38BDF8"], "certeza": "reported"}
                },
                "tipografia": {
                    "familias_preferidas": {"valor": ["Inter", "Roboto Mono"], "certeza": "reported"}
                },
                "adjetivos_estilo_visual": {"valor": ["minimalista", "tecnológico"], "certeza": "reported"}
            },
            "estructura_y_contenido": {
                "secciones_requeridas": {"valor": ["Hero", "Beneficios", "Contacto"], "certeza": "reported"}
            },
            "infraestructura_y_entrega": {
                "dominio": {"valor": "innovatech.io", "certeza": "reported"}
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

    def test_audit_client_readiness_complete_payload(self):
        payload = {
            "perfil_negocio": {
                "nombre_empresa": "Café Artesanal La Sierra",
                "propuesta_de_valor": "Café de especialidad de altura cultivado de forma sostenible",
                "sector_industria": "Alimentos y Bebidas"
            },
            "estructura_y_contenido": {
                "llamado_a_la_accion_cta": "Comprar Café en Línea",
                "secciones_requeridas": ["Hero", "Variedades", "Historia", "Tienda", "Contacto"]
            },
            "identidad_visual_y_marca": {
                "paleta_de_colores": {
                    "colores_deseados_hex": ["#2D1810", "#8D5B4C", "#D4A373", "#F5EBE0"]
                },
                "adjetivos_estilo_visual": ["cálido", "artesanal", "elegante"]
            },
            "conversion_y_contacto": {
                "canales_de_contacto": ["WhatsApp", "Instagram"],
                "dominio": "cafelasierra.mx"
            }
        }

        res_str = audit_client_readiness(payload, store=self.store)
        res = json.loads(res_str)
        assert res["status"] == "READY_TO_BUILD"
        assert res["readiness_score"] == 100
        assert len(res["missing_for_repo"]) == 0
        assert "create_landing_page_specification" in res["ready_to_execute_tools"]
        assert "audit_theme_palette" in res["ready_to_execute_tools"]

    def test_audit_client_readiness_incomplete_payload(self):
        # Payload missing CTA, colors, and sections
        payload = {
            "perfil_negocio": {
                "nombre_empresa": "Clínica Dental Sonrisas",
                "propuesta_de_valor": ""
            }
        }

        res_str = audit_client_readiness(payload, store=self.store)
        res = json.loads(res_str)
        assert res["status"] == "NEEDS_CLIENT_INPUT"
        assert res["readiness_score"] < 80
        assert len(res["missing_for_repo"]) >= 3
        assert len(res["next_questions_for_client"]) >= 3
        # Check that missing parameters have clear reasons
        missing_params = [m["parametro"] for m in res["missing_for_repo"]]
        assert "llamado_a_la_accion_cta" in missing_params
        assert "colores_deseados_hex" in missing_params

    def test_get_client_intake_guide(self):
        guide_str = get_client_intake_guide()
        guide = json.loads(guide_str)
        assert "bloques_de_escucha" in guide
        assert len(guide["bloques_de_escucha"]) == 5
        # Verify first block maps to repo tool
        first = guide["bloques_de_escucha"][0]
        assert "create_landing_page_specification" in first["herramienta_repo"]
