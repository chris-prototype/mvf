import hashlib
import hmac
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()
SECRET = b"my_secret_key"

@app.post("/webhook")
async def webhook(
    request: Request, signature: str = Header(None, alias="X-Signature")
):
  body = await request.body()

  # Verify signature
  if not signature or not hmac.compare_digest(
      signature, hmac.new(SECRET, body, hashlib.sha256).hexdigest()
  ):
    raise HTTPException(status_code=403, detail="Invalid signature")

  data = await request.json()
  return {"status": "ok", "received": data}