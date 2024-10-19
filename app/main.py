from fastapi import FastAPI
from app.routes import paper_routes, extract_routes

app = FastAPI()

app.include_router(paper_routes.router, prefix="/papers", tags=["papers"])
app.include_router(extract_routes, prefix="/extract", tags=["extract"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Paper API"}
