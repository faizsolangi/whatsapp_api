from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from datetime import datetime

app = FastAPI()

# Replace with your Zapier Webhook URL
ZAPIER_WEBHOOK_URL = "https://hooks.zapier.com/hooks/catch/23715689/u2zbs7y/"

# In-memory session tracker
user_sessions = {}

@app.post("/whatsapp")
async def whatsapp_reply(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    response = MessagingResponse()
    msg = response.message()
    user_id = From

    step = user_sessions.get(user_id, {}).get("step", "start")

    if step == "start":
        msg.body("👋 Welcome to Real Estate Bot!\nAre you looking to *Buy* or *Sell*?")
        user_sessions[user_id] = {"step": "intent"}

    elif step == "intent":
        intent = Body.strip().lower()
        if intent in ["buy", "sell"]:
            user_sessions[user_id]["intent"] = intent.capitalize()
            user_sessions[user_id]["step"] = "city"
            msg.body("🏙️ Great! Which *city* are you interested in?")
        else:
            msg.body("❗ Please reply with either *Buy* or *Sell*.")

    elif step == "city":
        user_sessions[user_id]["city"] = Body.strip().title()
        user_sessions[user_id]["step"] = "budget"
        msg.body("💰 Got it! What’s your *budget range*?")

    elif step == "budget":
        user_sessions[user_id]["budget"] = Body.strip()
        user_sessions[user_id]["step"] = "done"

        # Gather data
        data = user_sessions[user_id]
        payload = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Phone": user_id,
            "Intent": data.get("intent"),
            "City": data.get("city"),
            "Budget": data.get("budget")
        }

        # Send to Zapier webhook
        try:
            requests.post(ZAPIER_WEBHOOK_URL, json=payload)
        except Exception as e:
            print(f"Failed to send to Zapier: {e}")

        msg.body("✅ Thank you! Your request has been recorded. An agent will contact you soon.")

        # End session
        del user_sessions[user_id]

    else:
        msg.body("Hi again! Type *Buy* or *Sell* to begin.")

    return Response(content=str(response), media_type="application/xml")
