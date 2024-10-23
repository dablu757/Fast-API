from fastapi import status,HTTPException,Depends, APIRouter
import schemas, models
from router.oauth2 import get_current_user
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_to_the_post(
    vote : schemas.Vote,
    db : Session = Depends(get_db),
    current_user : int = Depends(get_current_user)
):
    vote_query = db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id
        )
    
    vote_found = vote_query.first()
    if vote.dir == 1 :
        if vote_found:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail= f'user {current_user.id} has already vote on post {vote.post_id}'
            )
        else:
            new_vote = models.Vote(
                user_id = current_user.id,
                post_id = vote.post_id
            )
            db.add(new_vote)
            db.commit()
            return {'message' : 'successfully added'}
    else:
        if not vote_found:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "vote does not exist"
            )
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {'message' : 'successsfully deleted'}