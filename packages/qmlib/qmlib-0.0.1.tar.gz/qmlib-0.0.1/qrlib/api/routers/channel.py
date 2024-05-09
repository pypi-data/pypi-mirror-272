import datetime
# from typing import List, Optional
from fastapi import APIRouter
from prisma.models import Channel
from pydantic import BaseModel

router = APIRouter()


class SignIn(BaseModel):
    email: str
    password: str


class SignInOut(BaseModel):
    token: str
    user: Channel


@router.get("/channel/item")
def findManyChannel():
    channel = Channel.prisma().find_many()
    return channel