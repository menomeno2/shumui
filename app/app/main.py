from fastapi import FastAPI
from .db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="نظام ميثاق الشمول",
    version="1.0.0",
    description="نظام تشغيل أولي جاهز للنشر"
)


@app.get("/")
def root():
    return {
        "message": "النظام يعمل بنجاح",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
