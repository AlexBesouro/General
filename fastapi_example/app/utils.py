from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hashing(password_to_hash: str):
    return pwd_context.hash(password_to_hash)


def pass_verifying(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
