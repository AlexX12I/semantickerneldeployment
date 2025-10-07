from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os

app = FastAPI(title="Semantic Kernel API")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Semantic Kernel API running"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    # Aquí luego se integrará Semantic Kernel. Por ahora devolvemos algo simple.
    return JSONResponse({"response": f"recibido: {user_input}"})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 80))
    uvicorn.run(app, host="0.0.0.0", port=port)

