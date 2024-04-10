from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Header, status
from fastapi.exceptions import HTTPException

from schema.jwt import JWTPayload, JWTResponsePayload
from setttings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY


class JWTHandler:
    @staticmethod
    def generate(username: str, exp_timestamp: int | None = None) -> JWTResponsePayload:
        expire_time = ACCESS_TOKEN_EXPIRE_MINUTES

        secret_key = SECRET_KEY

        expires_delta = datetime.utcnow() + timedelta(minutes=expire_time)

        to_encode = {
            "exp": exp_timestamp if exp_timestamp else expires_delta,
            "username": username,
        }
        encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)

        return JWTResponsePayload(access=encoded_jwt)

    @staticmethod
    def verify_token(auth_token: Annotated[str, Header()]) -> JWTPayload:
        jwt_token = auth_token
        if not jwt_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="auth header not found.",
            )
        try:
            token_data = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])

            if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except jwt.exceptions.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return JWTPayload(**token_data)