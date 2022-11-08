from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from typing import Optional


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
    

