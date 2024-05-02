from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import User as UserSchema, UserInput, AuthPayload
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import graphene

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class Mutation(graphene.ObjectType):
    register = graphene.Field(UserSchema, user_input=graphene.Argument(UserInput, required=True))
    login = graphene.Field(AuthPayload, user_input=graphene.Argument(UserInput, required=True))

    @staticmethod
    def mutate_register(parent, info, user_input):
        db = next(get_db())
        user = User(
            username=user_input.username,
            password=pwd_context.hash(user_input.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserSchema.from_pydantic(user)

    @staticmethod
    def mutate_login(parent, info, user_input):
        db = next(get_db())
        user = authenticate_user(user_input.username, user_input.password, db)
        if not user:
            raise Exception("Invalid credentials")
        access_token = create_access_token(data={"sub": user.username})
        db.query(User).filter(User.username == user.username).update({"last_login": datetime.utcnow()})
        db.commit()
        return AuthPayload(access_token=access_token, user=UserSchema.from_pydantic(user))