TEMPLATE = """
from pydantic.utils import Obj

class ResponseModelSchema:
     data:list
     message:str
     status:bool
     code:int
     error:Obj 
     

def  ResponseModel(data , message, status,code , error ):
	return  {
	"data": data ,
	"message":message,
	"status":status,
    "code":code,
	"error":error
	}
"""