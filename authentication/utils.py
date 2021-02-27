
from aiofile import AIOFile,async_open,LineReader, Writer
import ast
from models.user import User
from authentication.security import verify_password


async def authenticate_user(username: str, password: str, db = None):
    async with AIOFile("Credentials.txt", 'r') as doc:
        async for line in LineReader(doc):
            line = line.replace('\n','')
            user_dict = ast.literal_eval(line)
            if username == user_dict["username"] and verify_password(password, user_dict['Password']):
                return User(**user_dict)
        return False