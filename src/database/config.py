import os
import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = None
SUPABASE_KEY = None

# 1. Try reading from Streamlit secrets
try:
    if hasattr(st, "secrets"):
        SUPABASE_URL = st.secrets.get("SUPABASE_URL")
        SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")
except Exception:
    pass

# 2. Fallback to environment variables
if not SUPABASE_URL:
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
if not SUPABASE_KEY:
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: SUPABASE_URL or SUPABASE_KEY not configured. Please set them in .streamlit/secrets.toml")
    # Provide harmless placeholders to prevent import-time crashes
    SUPABASE_URL = SUPABASE_URL or "https://placeholder-project.supabase.co"
    SUPABASE_KEY = SUPABASE_KEY or "placeholder-key"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    print(f"WARNING: Failed to initialize Supabase client: {e}")
    supabase = None