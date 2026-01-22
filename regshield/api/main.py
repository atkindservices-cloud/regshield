from fastapi import FastAPI

app = FastAPI(title="RegShield AI")

@app.get("/")
def root():
    return {"status": "ok", "message": "RegShield API running"}
    