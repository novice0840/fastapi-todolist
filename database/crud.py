from sqlalchemy.orm import Session

from . import models, schemas

def get_articles(db: Session):
    return db.query(models.Article).all()

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def create_article(db: Session, title: str, description: str):
    db_article = models.Article(title=title, description=description)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article_id: int,title: str, description: str):    
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    db_article.title = title
    db_article.description = description
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).delete(synchronize_session=False)
    db.commit()
    return db_article

