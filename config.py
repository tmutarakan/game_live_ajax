import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '84da5b8a39a6d06bf8bc7a60cedcac93'
