import unittest
import io
import soundfile as sf
import numpy as np
import uuid
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class TestVoiceAndRegistration(unittest.TestCase):

    def test_01_voice_embedding_success(self):
        from src.pipelines.voice_pipeline import get_voice_embedding
        sr = 16000
        t = np.linspace(0, 1.5, int(sr * 1.5), endpoint=False)
        # Multi-frequency audio mimicking voice harmonics
        audio = 0.3 * np.sin(2 * np.pi * 220 * t) + 0.2 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.sin(2 * np.pi * 880 * t)
        buf = io.BytesIO()
        sf.write(buf, audio, sr, format='WAV')

        emb = get_voice_embedding(buf.getvalue())
        self.assertIsNotNone(emb, "Voice embedding should succeed on valid audio signal")
        self.assertEqual(len(emb), 256, "Resemblyzer embedding should have 256 dimensions")
        print("[PASS] Voice embedding successfully extracted 256-d vector.")

    def test_02_voice_embedding_silence_graceful(self):
        from src.pipelines.voice_pipeline import get_voice_embedding
        sr = 16000
        silence = np.zeros(sr * 2)
        buf = io.BytesIO()
        sf.write(buf, silence, sr, format='WAV')

        emb = get_voice_embedding(buf.getvalue())
        self.assertIsNone(emb, "Silence should return None gracefully without throwing exceptions")
        print("[PASS] Silence handled gracefully without crash.")

    def test_03_student_registration_with_and_without_voice(self):
        from src.database.db import create_student, get_all_students

        dummy_face = np.random.randn(128).tolist()
        dummy_voice = np.random.randn(256).tolist()

        # Registration WITH voice
        res1 = create_student("Test Student Alpha", face_embedding=dummy_face, voice_embedding=dummy_voice)
        self.assertIsNotNone(res1)
        self.assertEqual(res1[0]['name'], "Test Student Alpha")
        self.assertIsNotNone(res1[0]['voice_embedding'])

        # Registration WITHOUT voice (Optional voice enrollment)
        res2 = create_student("Test Student Beta", face_embedding=dummy_face, voice_embedding=None)
        self.assertIsNotNone(res2)
        self.assertEqual(res2[0]['name'], "Test Student Beta")
        self.assertIsNone(res2[0]['voice_embedding'])

        all_students = get_all_students()
        names = [s['name'] for s in all_students]
        self.assertIn("Test Student Alpha", names)
        self.assertIn("Test Student Beta", names)
        print("[PASS] Student registration succeeds both with voice and without voice.")

    def test_04_teacher_auth_workflow(self):
        from src.database.db import create_teacher, teacher_login, check_teacher_exists

        username = "prof_audit_test"
        pwd = "AuditTeacherPass123!"
        name = "Prof. Audit Tester"

        create_teacher(username, pwd, name)
        self.assertTrue(check_teacher_exists(username))

        # Test valid login
        teacher = teacher_login(username, pwd)
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher['name'], name)

        # Test invalid password
        wrong = teacher_login(username, "WrongPassword")
        self.assertIsNone(wrong)
        print("[PASS] Teacher registration and login workflow fully verified.")

    def test_05_header_single_line_title(self):
        from src.screens.components import header
        import inspect
        src = inspect.getsource(header.header_home)
        self.assertNotIn("SNAP<br>CLASS", src, "Title must not contain <br> tag")
        self.assertIn("SNAP CLASS", src, "Title must contain SNAP CLASS on single line")
        self.assertIn("white-space: nowrap", src, "CSS must prevent word wrapping")
        print("[PASS] SNAP CLASS header verified on a single line with whitespace nowrap.")

    def test_06_enrollment_workflow(self):
        from src.database.db import (
            create_subject,
            get_subject_by_code,
            is_student_enrolled,
            enroll_student_to_subject,
            get_enrolled_students
        )

        code = f"CS_{uuid.uuid4().hex[:6].upper()}"
        sub_res = create_subject(code, "Intro to CS", "A", 1)
        self.assertIsNotNone(sub_res)
        sub = get_subject_by_code(code)
        self.assertIsNotNone(sub)
        self.assertEqual(sub['subject_code'], code)

        sid = sub['subject_id']
        st_id = 1
        # Initially not enrolled
        self.assertFalse(is_student_enrolled(st_id, sid))

        # Enroll
        enroll_res = enroll_student_to_subject(st_id, sid)
        self.assertIsNotNone(enroll_res)
        self.assertTrue(is_student_enrolled(st_id, sid))

        enrolled_list = get_enrolled_students(sid)
        self.assertTrue(any(e.get('student_id') == st_id for e in enrolled_list))
        print("[PASS] Resilient subject enrollment workflow verified without unhandled network exceptions.")

if __name__ == '__main__':
    unittest.main()
