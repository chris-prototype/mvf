"""

 - receives a webhook from linear

"""
import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/webhook/linear")
async def linear_webhook(request: Request):
    payload = await request.json()
    print("Received Linear webhook:", payload)
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)