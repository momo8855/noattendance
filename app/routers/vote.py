from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from typing import Optional
import pandas as pd
import json


router = APIRouter(prefix='/attend', tags=['Attend'])



@router.post('/', status_code=status.HTTP_201_CREATED)
def attend(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.lec_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lcetrue with id {vote.lec_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.lec_id == vote.lec_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} is already registered in lec with id {vote.lec_id}")

        new_vote = models.Vote(lec_id = vote.lec_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message":"successfully added student"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student on lecture with id {vote.lec_id} does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted"}
    




#@router.get('/', response_model= schemas.All)
@router.get('/')
def get_attendance(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    studs = db.query(models.Post, models.Vote, models.User).join(models.Vote, models.Vote.lec_id == models.Post.id, isouter=True).join(
        models.User, models.User.id == models.Vote.user_id, isouter=True).filter(models.Post.course_name.contains(search)).limit(limit).offset(skip).all()
    
    hquery = db.query(models.User.full_name, models.Post.course_name,models.Post.lecture_num, ).filter(models.Vote.lec_id == models.Post.id).filter(
        models.Vote.user_id == models.User.id).filter(models.Post.course_name.contains(search)).limit(limit).offset(skip).all()

    
    df = pd.DataFrame(hquery, columns=['full_name', 'course_name', 'lec_num'])
    df = pd.get_dummies(df, columns= ['lec_num'])

    #studs = db.query(models.Post).join(models.Vote, models.Vote.lec_id == models.Post.id, isouter=True).join(models.Vote.user_id == models.Post.id, isouter=True)
    #.filter(models.Post.course_name.contains(search)).limit(limit).offset(skip).all()
    
    return df.to_dict(orient='records')




@router.post('/doctor', status_code=status.HTTP_201_CREATED)
def attend(vote: schemas.VoteDoc, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.lec_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lcetrue with id {vote.lec_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.lec_id == vote.lec_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} is already registered in lec with id {vote.lec_id}")

        new_vote = models.Vote(lec_id = vote.lec_id, user_id = vote.user_id)
        db.add(new_vote)
        db.commit()

        return {"message":"successfully added student"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student on lecture with id {vote.lec_id} does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message":"successfully deleted"}