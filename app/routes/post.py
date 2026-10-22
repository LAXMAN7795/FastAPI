from .. import models,schemas,utils, oauth2
from fastapi import FastAPI, Body, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,
              skip:int=0,search:Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()

    # left outer join
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    return results

@router.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.CreatePost,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published)) # to overcome sql attack
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)

    new_post = models.Post(owner_id=current_user.id,**post.dict())# unpack the dictionay, if we add the field in model it will automatically reflect.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}")
def get_post(id:int,db:Session=Depends(get_db)): 
    # cursor.execute("""SELECT * FROM posts WHERE id=(%s)""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id: {id} details does not exist")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id=(%s) RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id: {id} details does not exist")

    if post.owner_id!=current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")
    

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)# no need to get data back
    
@router.put("/{id}")
def update_post(id:int,post:schemas.CreatePost,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,
    #                                                                     post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    posts = db.query(models.Post).filter(models.Post.id==id)
    if posts.first() ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"id: {id} details does not exist")

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform requested action")

    updated_post= posts.update(post.dict(),synchronize_session=False)
    db.commit()
    return updated_post