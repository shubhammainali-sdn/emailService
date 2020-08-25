from pydantic import BaseModel,validator,ValidationError,EmailStr
from typing import List, Optional
from email_validator import validate_email, EmailNotValidError
from fastapi import FastAPI, File, UploadFile,Form



class send_email(BaseModel):
    sender:EmailStr
    content:str

    @validator('sender')
    def check_email_address(cls, v):
        try:
            # Validate.
            valid = validate_email(v)

            # Update with the normalized form.
            v = valid.email
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            raise ValueError(str(e))
        return v

class email(BaseModel):
    sender:str
    recipient:List[str]
    content:str
    status:Optional[str]=None


class emailsOut(email):
    id: int
