import logging

# import redis
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer

from model.diet_language_identifier import Interpreter

logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBearer()

async def get_interpreter():
    model_path = "C:\\Users\\Ishara\\Desktop\\Projects\\diet-language-identifier\\rasa\\models\\nlu-20230430-210832-quantum-dimension.tar.gz"
    interpreter = Interpreter(model_path=model_path)
    await interpreter.load_agent()
    logger.debug("Agent loaded")
    return interpreter

# Define a dependency to get the interpreter instance
@app.on_event("startup")
async def startup_event():
    app.dependency_overrides[get_interpreter] = await get_interpreter()

# # Create a Redis client instance
# redis_client = redis.Redis(host='localhost', port=6379, db=0)

# # Define a decorator to cache the function results in Redis
# def redis_cache(func):
#     def wrapper(*args, **kwargs):
#         # Build the Redis key from the function arguments
#         redis_key = str(args) + str(kwargs)

#         # Check if the Redis key exists and return the cached result if it does
#         if redis_client.exists(redis_key):
#             result = redis_client.get(redis_key)
#             return result

#         # Call the function and store the result in Redis
#         result = func(*args, **kwargs)
#         redis_client.set(redis_key, result)
#         return result

#     return wrapper

# # Define a function to predict language probabilities for a given text
# @redis_cache
# async def _parse(text: str, ):
#     return interpreter.parse(text=text)

# # Define a function to get the current user from the JWT token
# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
#         return payload['username']
#     except:
#         raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Define the API endpoint to predict the language probabilities
@app.post("/parse")
async def parse(payload: dict, interpreter: Interpreter = Depends(get_interpreter)):
    if 'text' in payload:
        return await interpreter.parse(text=payload['text'])
    else:
        raise HTTPException(status_code=400, detail="Missing 'text' field in input JSON")


if __name__ == "__main__":
    import uvicorn    
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
