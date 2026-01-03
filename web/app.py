from flask import Flask, request, jsonify
from supabase import create_client
import config

app = Flask(__name__)
supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

@app.route("/pay", methods=["POST"])
def pay():
    data = request.json
    user_id = data["user_id"]
    amount = data["amount"]
    
    user = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    
    if not user.data:
        supabase.table("users").insert({"user_id": user_id, "credits":0, "premium":False}).execute()
        user = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    
    credits_added = amount * 30  # 1 RS = 30 credits
    supabase.table("users").update({"credits": user.data['credits']+credits_added, "premium": True}).eq("user_id", user_id).execute()
    
    return jsonify({"status":"success", "credits_added": credits_added})

if __name__ == "__main__":
    app.run(port=5000)
