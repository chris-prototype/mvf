import hashlib
import hmac
import os
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()
SECRET = os.getenv("LINEARHOOK", "").encode("utf-8")


@app.post("/webhook/linear")
async def webhook(request: Request, signature: str = Header(None, alias="Linear-Signature")):
    print("Endpoint /webhook/linear was hit")
    body = await request.body()

    # Verify signature
    if not signature or not hmac.compare_digest(
        signature, hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    ):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    return {"status": "ok", "received": data}