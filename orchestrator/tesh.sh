# Valid Request (Returns 200)
curl -X POST "http://127.0.0.1:8000/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Signature: 757077813a37209cb8d95190dd280631622f6d6ec5c1a7d65691f61f744c2973" \
  -d '{"msg":"hello"}'

# Invalid Request (Returns 403)
curl -X POST "http://127.0.0.1:8000/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Signature: wrong_signature" \
  -d '{"msg":"hello"}'