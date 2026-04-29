from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import bcrypt


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
    bcrypt__ident="2b"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except TypeError:
        plain_bytes = plain_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hash_bytes)

def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except TypeError:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')
