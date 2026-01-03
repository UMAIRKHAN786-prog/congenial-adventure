from transformers import pipeline
import random
from supabase import create_client, Client
from datetime import datetime, timedelta
import config

# ---------------- AI Model ----------------
generator = pipeline("text-generation", model="gpt2-medium")
fancy_symbols = ["✨", "🔥", "💫", "🪄", "😎", "🎮", "🧸"]

# ---------------- Supabase ----------------
supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

# ---------- Roast generator -------------
def generate_roast(prompt, user):
    result = generator(
        f"Reply in savage, funny, shin-style roast to user {user}: {prompt}",
        max_length=50,
        do_sample=True,
        temperature=0.9
    )
    return result[0]['generated_text']

# ---------- Credits check ----------------
def has_credits(user_id, cost=1):
    user = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    if user.data and user.data['credits'] >= cost:
        return True
    return False

# ---------- Deduct credits ---------------
def deduct_credits(user_id, amount=1):
    user = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    if user.data:
        new_credits = max(user.data['credits'] - amount, 0)
        supabase.table("users").update({"credits": new_credits}).eq("user_id", user_id).execute()

# ---------- Daily credits ----------------
def add_daily(user_id):
    user = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    now = datetime.utcnow()
    if not user.data:
        supabase.table("users").insert({
            "user_id": user_id,
            "credits": 1000,
            "premium": False,
            "last_daily": now
        }).execute()
        return True
    last_daily = user.data.get("last_daily")
    if not last_daily or (now - last_daily).total_seconds() > 86400:
        supabase.table("users").update({
            "credits": user.data['credits'] + 1000,
            "last_daily": now
        }).eq("user_id", user_id).execute()
        return True
    return False

# ---------- Top users -------------------
def get_top_users(limit=10):
    users = supabase.table("users").select("*").order("credits", desc=True).limit(limit).execute()
    return users.data

# ---------- My rank ---------------------
def get_my_rank(user_id):
    users = supabase.table("users").select("*").order("credits", desc=True).execute()
    for i, user in enumerate(users.data, 1):
        if user['user_id'] == user_id:
            return i
    return None
