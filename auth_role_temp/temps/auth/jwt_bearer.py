from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from global_schemas import ResponseModel , ResponseModelSchema
from .jwt_handler import decodeJWT


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        print("Credentials :", credentials)
        if credentials:
            if not credentials.scheme == "Bearer":
                print("Failed here.")
                raise HTTPException(status_code=403, detail= ResponseModel([] , "Invalid authentication token" , False , 403 , {}) )

            if not self.verify_jwt(credentials.credentials):
                print("Failed here two")
                raise HTTPException(status_code=403, detail= ResponseModel([] , "Invalid token or expired token" , False , 403 , {}) )
  

            return credentials.credentials
        else:
            print("Failed here three")
            raise HTTPException(status_code=403, detail= ResponseModel([] , "Invalid authorization token" , False , 403 , {}) )


    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
