import os
import sys
import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class TestEndToEndSimulation(unittest.TestCase):

    def test_01_face_recognition_pipeline_end_to_end(self):
        from src.pipelines.face_pipeline import predict_attendance

        # Generate two synthetic 128-d face encodings
        np.random.seed(42)
        student1_emb = np.random.randn(128)
        student1_emb = student1_emb / np.linalg.norm(student1_emb)

        student2_emb = np.random.randn(128)
        student2_emb = student2_emb / np.linalg.norm(student2_emb)

        mock_students = [
            {"student_id": 101, "name": "Alice Johnson", "face_embedding": student1_emb.tolist()},
            {"student_id": 102, "name": "Bob Smith", "face_embedding": student2_emb.tolist()},
        ]

        with patch("src.pipelines.face_pipeline.get_all_students", return_value=mock_students):
            from src.pipelines.face_pipeline import get_trained_model, train_classifier
            train_classifier()

            # Mock get_face_embeddings to return student 1's embedding (simulating camera capture of Alice)
            with patch("src.pipelines.face_pipeline.get_face_embeddings", return_value=[student1_emb]):
                dummy_img = np.zeros((200, 200, 3), dtype=np.uint8)
                detected, all_students, num_faces = predict_attendance(dummy_img)

                self.assertEqual(num_faces, 1)
                self.assertIn(101, detected)
                self.assertTrue(detected[101])
                self.assertNotIn(102, detected)
                print("[PASS] Face pipeline correctly identified enrolled student from synthetic capture!")

    def test_02_voice_pipeline_matching(self):
        from src.pipelines.voice_pipeline import identify_speaker

        np.random.seed(99)
        spk1 = np.random.randn(256)
        spk1 /= np.linalg.norm(spk1)

        spk2 = np.random.randn(256)
        spk2 /= np.linalg.norm(spk2)

        candidates = {
            201: spk1.tolist(),
            202: spk2.tolist()
        }

        # Query with spk1 plus tiny noise
        query_spk1 = spk1 + np.random.randn(256) * 0.01
        query_spk1 /= np.linalg.norm(query_spk1)

        matched_id, score = identify_speaker(query_spk1, candidates, threshold=0.65)
        self.assertEqual(matched_id, 201)
        self.assertGreater(score, 0.95)
        print("[PASS] Voice pipeline correctly matched speaker identity with high similarity score!")

    def test_03_attendance_log_generation(self):
        enrolled_students = [
            {"students": {"student_id": 101, "name": "Alice Johnson"}},
            {"students": {"student_id": 102, "name": "Bob Smith"}},
            {"students": {"student_id": 103, "name": "Charlie Brown"}},
        ]
        all_detected_ids = {101: ["Photo 1"], 102: ["Photo 1", "Photo 2"]}
        selected_subject_id = "SUB_CS101"
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        results = []
        attendance_to_log = []
        for node in enrolled_students:
            student = node['students']
            sources = all_detected_ids.get(int(student['student_id']), [])
            is_present = len(sources) > 0

            results.append({
                "Name": student['name'],
                "ID": student['student_id'],
                "Source": ", ".join(sources) if is_present else "-",
                "Status": "✅ Present" if is_present else "❌ Absent"
            })
            attendance_to_log.append({
                'student_id': student['student_id'],
                'subject_id': selected_subject_id,
                'timestamp': current_timestamp,
                'is_present': bool(is_present)
            })

        df = pd.DataFrame(results)
        self.assertEqual(len(df), 3)
        self.assertEqual(df.iloc[0]['Status'], "✅ Present")
        self.assertEqual(df.iloc[1]['Status'], "✅ Present")
        self.assertEqual(df.iloc[2]['Status'], "❌ Absent")
        self.assertEqual(len(attendance_to_log), 3)
        self.assertFalse(attendance_to_log[2]['is_present'])
        print("[PASS] Attendance log and review dataframe generated correctly!")

if __name__ == '__main__':
    unittest.main()
