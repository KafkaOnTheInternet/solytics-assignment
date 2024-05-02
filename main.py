from fastapi import FastAPI, Depends
from graphene import ObjectType
from schemas import schema
from mutations import Mutation
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import os
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp
from fastapi_jwt_auth import AuthJWT, AuthJWTSettings
from fastapi.responses import JSONResponse

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return AuthJWTSettings(
        secret_key=SECRET_KEY,
        algorithm="HS256",
        authjwt_token_location={"headers", "cookies"},
    )

@app.exception_handler(AuthJWTException)
def auth_jwt_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

class Query(ObjectType):
    pass

app.add_route("/graphql", GraphQLApp(schema=schema, mutation=Mutation))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)