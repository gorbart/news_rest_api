from fastapi import FastAPI

from app.server.routes.article import router as article_router
from app.server.routes.author import router as author_router

app = FastAPI()

app.include_router(article_router, tags=['article'], prefix="/article")
app.include_router(author_router, tags=['author'], prefix="/author")


@app.get("/", tags=['root'])
async def read_root():
    return {'message': 'Welcome to this fantastic app!'}