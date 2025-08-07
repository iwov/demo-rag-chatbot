from fastapi import FastAPI

app = FastAPI(title="Test Server")

@app.get("/")
async def root():
    return {"message": "Test server working"}

@app.get("/api/test")
async def test():
    return {"status": "ok"}