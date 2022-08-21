from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database import crud, models
from database.database import SessionLocal, engine
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Article(BaseModel):
    title: str
    description: str

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def get_main(request: Request, db: Session = Depends(get_db)):
    articles = crud.get_articles(db=db)
    return templates.TemplateResponse("main.html", {"request":request, "articles": articles})

@app.get('/articles')
def get_articles(db: Session = Depends(get_db)):
    articles = crud.get_articles(db=db)
    return articles


@app.post("/article")
async def post_create(article: Article, db: Session = Depends(get_db)):
    db_article = crud.create_article(db, **article.dict())
    if db_article is None:
        raise HTTPException(status_code=500, detail="글 생성에 실패하였습니다")
    return db_article
    

@app.get("/article/{article_id}")
async def get_article(article_id:int, db: Session = Depends(get_db)):
    db_article = crud.get_article(db=db, article_id=article_id)
    return db_article


@app.put("/article/{article_id}")
async def update_article(article_id: int, article: Article,  db: Session = Depends(get_db)):
    db_article = crud.update_article(db=db, article_id=article_id, **article.dict())
    if db_article is None:
        raise HTTPException(status_code=500, detail="글 수정에 실패하였습니다")
    return db_article


@app.delete("/article/{article_id}")
def delete_article(article_id: str, db: Session = Depends(get_db)):
    db_article = crud.delete_article(db=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=500, detail="글 삭제에 실패하였습니다")
    return db_article


@app.get("/sample")
async def get_sample():
    pass
