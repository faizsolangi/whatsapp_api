from fastapi import FastAPI, Request, Form
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import requests

app = FastAPI()

# 🔗 Replace with your actual Zapier webhook URL
ZAP_URL = "https://hooks.zapier.com/hooks/catch/23715689/u2zbs7y/"

@app.post("/whatsapp")
async def whatsapp_reply(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    # 🧠 Bot response logic
    response = MessagingResponse()
    msg = response.message()

    if "buy" in Body.lower():
        msg.body("Thanks for your interest! What city are you looking in?")
    else:
        msg.body("Welcome to Real Estate Bot! Type 'Buy' or 'Sell' to begin.")

    # 📤 Send data to Zapier
    lead = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "From": From,
        "Message": Body
    }
    try:
        requests.post(ZAP_URL, json=lead)
    except Exception as e:
        print("Failed to send to Zapier:", e)

    return str(response)
