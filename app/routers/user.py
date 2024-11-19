from fastapi import status, HTTPException, Depends, APIRouter # type: ignore
from .. import utils, models, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router  = APIRouter(
    prefix="/users",
    tags=['Users']
)

# Create a new user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    #Hash the pwd - user.password

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Get a user by ID
@router.get("/{id}", response_model=schemas.UserOut)
def get_usr(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist!")
    
    return user