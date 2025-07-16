from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

app = FastAPI()

@app.post("/whatsapp")
async def whatsapp_reply(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    # Create Twilio response
    response = MessagingResponse()
    msg = response.message()

    # Basic chatbot logic
    if "buy" in Body.lower():
        msg.body("Thanks for your interest! What city are you looking in?")
    elif "sell" in Body.lower():
        msg.body("Great! Please share the location of your property.")
    else:
        msg.body("Welcome to Real Estate Bot! Type 'Buy' or 'Sell' to begin.")

    # Return proper XML response
    return Response(content=str(response), media_type="application/xml")
