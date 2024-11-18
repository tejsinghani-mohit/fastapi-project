from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func # type: ignore
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Get Posts
@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)

    return posts

# Create new Posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Find post by ID
@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int, response: Response, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",(str(id)))
    # post=cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found!")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post

#Delete post by ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts where id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post_by_id(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning *""",
    #                 (post.title, post.content, post.published, str(id)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_result = post_query.first()

    if post_result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist!")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()