import os
import json
import bcrypt
from pathlib import Path
from src.database.config import supabase

# Local fallback persistent JSON store
LOCAL_DB_PATH = Path(__file__).resolve().parent / "local_db.json"

def _load_local_db():
    if not LOCAL_DB_PATH.exists():
        default_db = {
            "teachers": [],
            "students": [],
            "subjects": [],
            "subject_students": [],
            "attendance_logs": []
        }
        _save_local_db(default_db)
        return default_db
    try:
        with open(LOCAL_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "teachers": [],
            "students": [],
            "subjects": [],
            "subject_students": [],
            "attendance_logs": []
        }

def _save_local_db(data):
    try:
        with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save local db: {e}")


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    try:
        return bcrypt.checkpw(pwd.encode(), hashed.encode())
    except Exception:
        return False

# Backward compatibility alias
cheack_pass = check_pass


def check_teacher_exists(username):
    # Try Supabase first
    if supabase is not None:
        try:
            response = supabase.from_("teachers").select("*").eq("username", username).execute()
            if response and response.data:
                return len(response.data) > 0
        except Exception:
            pass

    # Fallback to local store
    local_db = _load_local_db()
    return any(t.get("username") == username for t in local_db.get("teachers", []))


def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.from_("teachers").insert(data).execute()
            if response and response.data:
                # Also mirror into local store
                local_db = _load_local_db()
                local_db.setdefault("teachers", []).append(response.data[0])
                _save_local_db(local_db)
                return response.data
        except Exception as e:
            print(f"Supabase create_teacher note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    teachers = local_db.setdefault("teachers", [])
    new_id = len(teachers) + 1
    record = {
        "teacher_id": new_id,
        "username": username,
        "password": data["password"],
        "name": name
    }
    teachers.append(record)
    _save_local_db(local_db)
    return [record]


def teacher_login(username, password):
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.from_("teachers").select("*").eq("username", username).execute()
            if response and response.data:
                teacher = response.data[0]
                if check_pass(password, teacher.get("password", "")):
                    return teacher
        except Exception as e:
            print(f"Supabase teacher_login note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    for teacher in local_db.get("teachers", []):
        if teacher.get("username") == username:
            if check_pass(password, teacher.get("password", "")):
                return teacher
    return None


def get_all_students():
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.table("students").select("*").execute()
            if response and response.data:
                # Cache students locally
                local_db = _load_local_db()
                local_db["students"] = response.data
                _save_local_db(local_db)
                return response.data
        except Exception as e:
            print(f"Supabase get_all_students note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    return local_db.get("students", [])


def create_student(new_name, face_embedding=None, voice_embedding=None):
    data = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.table("students").insert(data).execute()
            if response and response.data:
                local_db = _load_local_db()
                local_db.setdefault("students", []).append(response.data[0])
                _save_local_db(local_db)
                return response.data
        except Exception as e:
            print(f"Supabase create_student note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    students = local_db.setdefault("students", [])
    new_id = len(students) + 1
    record = {
        "student_id": new_id,
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding
    }
    students.append(record)
    _save_local_db(local_db)
    return [record]


def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.table("subjects").insert(data).execute()
            if response and response.data:
                local_db = _load_local_db()
                local_db.setdefault("subjects", []).append(response.data[0])
                _save_local_db(local_db)
                return response.data
        except Exception as e:
            print(f"Supabase create_subject note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    subjects = local_db.setdefault("subjects", [])
    new_id = len(subjects) + 1
    record = {
        "subject_id": new_id,
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }
    subjects.append(record)
    _save_local_db(local_db)
    return [record]


def get_teacher_subjects(teacher_id):
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.table("subjects").select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()
            subjects = response.data or []
            for sub in subjects:
                sub_students = sub.get("subject_students", [])
                if isinstance(sub_students, list) and sub_students:
                    sub["total_students"] = sub_students[0].get("count", 0)
                elif isinstance(sub_students, dict):
                    sub["total_students"] = sub_students.get("count", 0)
                else:
                    sub["total_students"] = 0

                attendance = sub.get("attendance_logs") or sub.get("attendence_logs") or []
                if isinstance(attendance, list):
                    unique_sessions = len(set(log.get("timestamp") for log in attendance if isinstance(log, dict) and "timestamp" in log))
                else:
                    unique_sessions = 0
                sub["total_classes"] = unique_sessions

                sub.pop("subject_students", None)
                sub.pop("attendance_logs", None)
                sub.pop("attendence_logs", None)
            return subjects
        except Exception as e:
            print(f"Supabase get_teacher_subjects note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    teacher_subs = [s for s in local_db.get("subjects", []) if str(s.get("teacher_id")) == str(teacher_id)]
    all_enrollments = local_db.get("subject_students", [])
    all_attendance = local_db.get("attendance_logs", [])

    results = []
    for s in teacher_subs:
        sid = s.get("subject_id")
        total_students = sum(1 for e in all_enrollments if str(e.get("subject_id")) == str(sid))
        timestamps = set(a.get("timestamp") for a in all_attendance if str(a.get("subject_id")) == str(sid) and a.get("timestamp"))
        res = dict(s)
        res["total_students"] = total_students
        res["total_classes"] = len(timestamps)
        results.append(res)
    return results


def get_attendance_for_teacher(teacher_id):
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.table("attendance_logs").select("*, subjects!inner(*)").eq("subjects.teacher_id", teacher_id).execute()
            if response and response.data is not None:
                return response.data
        except Exception:
            try:
                response = supabase.table("attendence_logs").select("*, subjects!inner(*)").eq("subjects.teacher_id", teacher_id).execute()
                if response and response.data is not None:
                    return response.data
            except Exception as e:
                print(f"Supabase get_attendance_for_teacher note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    teacher_sub_ids = {s.get("subject_id"): s for s in local_db.get("subjects", []) if str(s.get("teacher_id")) == str(teacher_id)}
    logs = []
    for a in local_db.get("attendance_logs", []):
        sid = a.get("subject_id")
        if sid in teacher_sub_ids:
            item = dict(a)
            item["subjects"] = teacher_sub_ids[sid]
            logs.append(item)
    return logs


def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }
    # Try Supabase
    if supabase is not None:
        try:
            response = supabase.table("subject_students").insert(data).execute()
            if response and response.data:
                local_db = _load_local_db()
                local_db.setdefault("subject_students", []).append(response.data[0])
                _save_local_db(local_db)
                return response.data
        except Exception as e:
            print(f"Supabase enroll note: {e}")

    # Fallback to local store
    local_db = _load_local_db()
    enrollments = local_db.setdefault("subject_students", [])
    if not any(e.get("student_id") == student_id and e.get("subject_id") == subject_id for e in enrollments):
        enrollments.append(data)
        _save_local_db(local_db)
    return [data]


def unenroll_student_to_subject(student_id, subject_id):
    if supabase is not None:
        try:
            response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
            if response and response.data:
                return response.data
        except Exception as e:
            print(f"Supabase unenroll note: {e}")

    local_db = _load_local_db()
    enrollments = local_db.get("subject_students", [])
    local_db["subject_students"] = [e for e in enrollments if not (e.get("student_id") == student_id and e.get("subject_id") == subject_id)]
    _save_local_db(local_db)
    return [{"student_id": student_id, "subject_id": subject_id}]

unroll_student_to_subject = unenroll_student_to_subject


def get_student_subjects(student_id):
    if supabase is not None:
        try:
            response = supabase.table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
            if response and response.data is not None:
                return response.data
        except Exception as e:
            print(f"Supabase get_student_subjects note: {e}")

    local_db = _load_local_db()
    subs_map = {s.get("subject_id"): s for s in local_db.get("subjects", [])}
    my_enrollments = [e for e in local_db.get("subject_students", []) if str(e.get("student_id")) == str(student_id)]
    results = []
    for e in my_enrollments:
        sid = e.get("subject_id")
        if sid in subs_map:
            results.append({
                "student_id": student_id,
                "subject_id": sid,
                "subjects": subs_map[sid]
            })
    return results


def get_student_attendance(student_id):
    if supabase is not None:
        try:
            response = supabase.table("attendance_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
            if response and response.data is not None:
                return response.data
        except Exception:
            try:
                response = supabase.table("attendence_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
                if response and response.data is not None:
                    return response.data
            except Exception as e:
                print(f"Supabase get_student_attendance note: {e}")

    local_db = _load_local_db()
    subs_map = {s.get("subject_id"): s for s in local_db.get("subjects", [])}
    my_logs = [a for a in local_db.get("attendance_logs", []) if str(a.get("student_id")) == str(student_id)]
    for item in my_logs:
        sid = item.get("subject_id")
        if sid in subs_map:
            item["subjects"] = subs_map[sid]
    return my_logs


def create_attendance(logs):
    if supabase is not None:
        try:
            response = supabase.table("attendance_logs").insert(logs).execute()
            if response and response.data:
                local_db = _load_local_db()
                local_db.setdefault("attendance_logs", []).extend(response.data)
                _save_local_db(local_db)
                return response.data
        except Exception:
            try:
                response = supabase.table("attendence_logs").insert(logs).execute()
                if response and response.data:
                    local_db = _load_local_db()
                    local_db.setdefault("attendance_logs", []).extend(response.data)
                    _save_local_db(local_db)
                    return response.data
            except Exception as e:
                print(f"Supabase create_attendance note: {e}")

    local_db = _load_local_db()
    stored_logs = local_db.setdefault("attendance_logs", [])
    if isinstance(logs, list):
        stored_logs.extend(logs)
    elif isinstance(logs, dict):
        stored_logs.append(logs)
    _save_local_db(local_db)
    return logs


def get_subject_by_code(subject_code):
    if supabase is not None:
        try:
            res = supabase.table('subjects').select('subject_id, name, subject_code, section').eq('subject_code', subject_code).execute()
            if res and res.data:
                return res.data[0]
        except Exception as e:
            print(f"Supabase get_subject_by_code note: {e}")

    local_db = _load_local_db()
    for s in local_db.get("subjects", []):
        if str(s.get("subject_code", "")).strip().lower() == str(subject_code).strip().lower():
            return s
    return None


def is_student_enrolled(student_id, subject_id):
    if supabase is not None:
        try:
            check = supabase.table('subject_students').select('*').eq('subject_id', subject_id).eq('student_id', student_id).execute()
            if check and check.data:
                return len(check.data) > 0
        except Exception as e:
            print(f"Supabase is_student_enrolled note: {e}")

    local_db = _load_local_db()
    return any(
        str(e.get("student_id")) == str(student_id) and str(e.get("subject_id")) == str(subject_id)
        for e in local_db.get("subject_students", [])
    )


def get_enrolled_students(subject_id):
    if supabase is not None:
        try:
            enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id', subject_id).execute()
            if enrolled_res and enrolled_res.data:
                return enrolled_res.data
        except Exception as e:
            print(f"Supabase get_enrolled_students note: {e}")

    local_db = _load_local_db()
    students_map = {str(s.get("student_id")): s for s in local_db.get("students", [])}
    enrollments = [e for e in local_db.get("subject_students", []) if str(e.get("subject_id")) == str(subject_id)]
    results = []
    for e in enrollments:
        sid_str = str(e.get("student_id"))
        if sid_str in students_map:
            results.append({
                "student_id": e.get("student_id"),
                "subject_id": subject_id,
                "students": students_map[sid_str]
            })
    return results
