import os
import sys
import unittest
import numpy as np
from PIL import Image
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class TestAttendanceSystem(unittest.TestCase):

    def test_01_assets_exist_and_valid(self):
        assets_dir = PROJECT_ROOT / "assets"
        self.assertTrue(assets_dir.exists(), "assets folder must exist")

        required_assets = [
            "logo_url.png",
            "student_illustration.png",
            "teacher_illustration.png"
        ]
        for asset in required_assets:
            p = assets_dir / asset
            self.assertTrue(p.exists(), f"Asset {asset} must exist")
            img = Image.open(p)
            self.assertGreater(img.width, 0)
            self.assertGreater(img.height, 0)
            print(f"[PASS] Asset {asset} verified ({img.size})")

    def test_02_no_college_branding(self):
        forbidden_terms = ["apna college", "apnacollege", "college name"]
        # Scan all python and markdown files
        for py_file in PROJECT_ROOT.rglob("*"):
            if any(part in py_file.parts for part in [".git", "venv", ".venv", "__pycache__", "scratch", "tests"]):
                continue
            if py_file.suffix in [".py", ".md", ".toml"]:
                content = py_file.read_text(errors="ignore").lower()
                for term in forbidden_terms:
                    self.assertNotIn(term, content, f"Forbidden college branding '{term}' found in {py_file}")
        print("[PASS] No college-specific branding detected across codebase.")

    def test_03_db_helpers_and_password_hashing(self):
        from src.database.db import hash_pass, check_pass, cheack_pass

        pwd = "SecretPassword123!"
        hashed = hash_pass(pwd)
        self.assertNotEqual(pwd, hashed)
        self.assertTrue(check_pass(pwd, hashed))
        self.assertTrue(cheack_pass(pwd, hashed))
        self.assertFalse(check_pass("WrongPassword", hashed))
        print("[PASS] Password hashing and verification working correctly.")

    def test_04_face_pipeline_models_and_embeddings(self):
        from src.pipelines.face_pipeline import load_dlib_models, get_face_embeddings

        detector, sp, facerec = load_dlib_models()
        self.assertIsNotNone(detector)
        self.assertIsNotNone(sp)
        self.assertIsNotNone(facerec)

        # Test with synthetic RGB image (100x100)
        blank_img = np.zeros((100, 100, 3), dtype=np.uint8)
        encodings = get_face_embeddings(blank_img)
        self.assertEqual(len(encodings), 0, "Blank image should have 0 face encodings")
        print("[PASS] Face pipeline models loaded and inference pipeline functional.")

    def test_05_voice_pipeline_models(self):
        from src.pipelines.voice_pipeline import load_voice_encoder, identify_speaker

        encoder = load_voice_encoder()
        self.assertIsNotNone(encoder)

        # Test speaker identification with synthetic embeddings
        emb1 = np.ones(256) / np.linalg.norm(np.ones(256))
        emb2 = np.ones(256) / np.linalg.norm(np.ones(256)) # exact match
        emb3 = -np.ones(256) / np.linalg.norm(np.ones(256)) # opposite

        candidates = {
            1: emb2.tolist(),
            2: emb3.tolist()
        }
        matched_id, score = identify_speaker(emb1, candidates, threshold=0.65)
        self.assertEqual(matched_id, 1)
        self.assertAlmostEqual(score, 1.0, places=2)
        print("[PASS] Voice encoder loaded and speaker cosine comparison verified.")

    def test_06_ui_module_imports(self):
        from src.screens.home_screen import home_screen
        from src.screens.teacher_screen import teacher_screen
        from src.screens.student_screen import student_screen
        from src.screens.ui.base_layout import style_base_layout, style_background_home, style_background_dashboard
        from src.components.header import header_home, header_dashboard
        from src.components.footer import footer_home, footer_dashboard
        from src.components.subject_card import subject_card
        from src.components.dialog_create_subject import create_subject_dialog
        from src.components.dialog_share_subject import share_subject_dialog
        from src.components.dialog_enroll import enroll_dialog
        from src.components.dialog_auto_enroll import auto_enroll_dialog
        from src.components.dialog_add_photo import add_photos_dialog
        from src.components.dialog_attendance_results import attendance_result_dialog, show_attendance_result
        from src.components.dialog_voice_attendance import voice_attendance_dialog

        print("[PASS] All screen and dialog UI modules import cleanly without error.")

    def test_07_subject_card_renders_clean_html(self):
        import streamlit as st
        from src.components.subject_card import subject_card
        rendered = []
        original_md = st.markdown
        try:
            st.markdown = lambda content, unsafe_allow_html=False: rendered.append(content)
            subject_card(
                name="English",
                code="CS12",
                section="B25",
                stats=[('📅', 'Classes Total', 0), ('✅', 'Attended', 0)]
            )
            self.assertEqual(len(rendered), 1)
            output = rendered[0]
            # Ensure no raw multiline indentation that triggers Markdown code blocks
            for line in output.split("\n"):
                self.assertFalse(line.startswith("    "), f"Indented line detected in HTML: {line}")
            self.assertIn("English", output)
            self.assertIn("CS12", output)
            self.assertIn("Classes Total", output)
            self.assertIn("Attended", output)
            print("[PASS] Subject card renders clean HTML without code-block indentation triggers.")
        finally:
            st.markdown = original_md


if __name__ == '__main__':
    unittest.main()
