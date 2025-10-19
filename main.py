from fastapi import FastAPI
from app.database import engine
from app import Models

Models.Base.metadata.drop_all(bind=engine)
Models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobTracker API")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


