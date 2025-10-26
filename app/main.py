from fastapi import FastAPI
from app.database import engine
from app import models
from app.controller import user_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="JobTracker API")
app.include_router(user_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


