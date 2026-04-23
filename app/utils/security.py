import logging
from fastapi import Request, HTTPException
from app.utils.schema import Users
from app.utils.settings import settings
import requests



logging.basicConfig(level=settings.log_level, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

def validate_user(request: Request):
    # Here you can implement your logic to extract user information from the request
    url = f"http://{settings.jwt_host}:{settings.jwt_port}/jwt/v1/users/me/"
    user_data: Users
    response : requests.Response = None
    try:
        response = requests.get(headers=request.headers, url=url)
        if response.status_code == 200:
            user_data = Users(**response.json()[0])
            print(user_data.username)
        
    except Exception as e:
        logger.error(f"Error occurred while fetching user data: {e}")
        raise HTTPException(status_code=response.status_code, detail="Error occurred while fetching user data")
    
    if response.status_code != 200:
            logger.error(f"Error occurred while fetching user data: {response.status_code} - {response.text}")
            raise HTTPException(status_code=response.status_code, detail=response.json())
    else:
        logger.info(f"User {user_data.username} validated successfully")
    
    return user_data

