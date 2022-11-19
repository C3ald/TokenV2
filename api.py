from blockchain import *
from fastapi import FastAPI

APP = FastAPI()
blockchain = Blockchain()

@APP.route('/')
def index():
    return '/docs for routes'

