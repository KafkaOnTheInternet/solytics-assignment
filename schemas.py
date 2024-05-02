import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import User as UserModel

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class UserInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)

class AuthPayload(graphene.ObjectType):
    access_token = graphene.String()
    user = graphene.Field(User)

class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    register = graphene.Field(User, user_input=graphene.Argument(UserInput, required=True))
    login = graphene.Field(AuthPayload, user_input=graphene.Argument(UserInput, required=True))

schema = graphene.Schema(query=Query, mutation=Mutation)