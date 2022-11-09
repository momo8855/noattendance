from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from typing import Optional
from sqlalchemy import func



router = APIRouter(prefix="/lectures", tags=['Lectures'])



@router.get("/", response_model=List[schemas.PostOut], include_in_schema=False)
def get_lecs(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    lecs = db.query(models.Post, func.count(models.Vote.lec_id).label("attend_num")).join(models.Vote, models.Vote.lec_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.course_name.contains(search)).limit(limit).offset(skip).all()

    return lecs





@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Resp)
def create_lecs(lecture: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    print(current_user.type)
    
    if current_user.type != "B":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="only doctors can perform this action")

    new_lec = models.Post(owner_id = current_user.id, **lecture.dict())
    db.add(new_lec)
    db.commit()
    db.refresh(new_lec)

    return new_lec



@router.get("/{id}", response_model=schemas.PostOut, include_in_schema=False)
def get_lec(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    lec = db.query(models.Post, func.count(models.Vote.lec_id).label("votes")).join(models.Vote, models.Vote.lec_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not lec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return lec

   
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_lec(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  
    lec_query = db.query(models.Post).filter(models.Post.id == id)
    lec = lec_query.first()

    if lec == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if lec.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    lec_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Resp, include_in_schema=False)
def update_lec(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    lec_query = db.query(models.Post).filter(models.Post.id == id)
    lec = lec_query.first()

    if lec == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if lec.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    lec_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return  lec_query.first()


