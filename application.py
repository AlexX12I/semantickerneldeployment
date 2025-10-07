from fastapi import FastAPI
import semantic_kernel as sk

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Semantic Kernel on Azure!"}

# Kernel básico (por si quieres usarlo luego)
kernel = sk.Kernel()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
