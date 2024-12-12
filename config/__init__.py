from decouple import config

POSTGRES_URL = config('POSTGRES_URL')
SECRET_KEY= config('SECRET_KEY')
ALGORITHM = config('HASH_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES= config('ACCESS_TOKEN_EXPIRE_MINUTES')
INVITATION_EXPIRATION_DAYS= config('INVITATION_EXPIRATION_DAYS')
SENDINBLUE_API_KEY=config('SENDINBLUE_API_KEY')
SENDINBLUE_EMAIL=config('SENDINBLUE_EMAIL')
SENDINBLUE_NAME=config('SENDINBLUE_NAME')
REPLY_TO_EMAIL=config('REPLY_TO_EMAIL')

FRONTEND_URL = config('FRONTEND_URL')
CORS_ORIGINS = config('CORS_ORIGINS').split(',')
ALLOWED_METHODS= config('ALLOWED_METHODS').split(',')
ALLOWED_HEADERS= config('ALLOWED_HEADERS').split(',')