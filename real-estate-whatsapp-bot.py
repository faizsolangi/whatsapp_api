from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.messaging_response import MessagingResponse
import uvicorn

app = FastAPI()


@app.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_reply(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    print(f"Incoming message from {From}: {Body}")

    response = MessagingResponse()
    msg = response.message()

    # Simple keyword logic
    if "buy" in Body.lower():
        msg.body("Thanks for your interest! What city are you looking in?")
    elif "sell" in Body.lower():
        msg.body("Great! What kind of property are you selling?")
    else:
        msg.body("Welcome to Real Estate Bot! Type 'Buy' or 'Sell' to begin.")

    return str(response)
