import graphene
from graphene import relay, Int, String
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField, ObjectType, Field
from .models import Account as AccountModel
from .db import get_db

class Account(SQLAlchemyObjectType):
    class Meta:
        model = AccountModel
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    accounts = SQLAlchemyConnectionField(Account.connection)


class Mutation(graphene.ObjectType):    
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)