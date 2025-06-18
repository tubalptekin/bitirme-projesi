from fastapi import FastAPI
from database import engine
import models
from routes import router  # <- bunu ekle

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(router)  # <- bunu ekle

@app.get("/")
def read_root():
    return {"message": "API çalışıyor!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

