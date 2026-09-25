from pydantic import BaseModel , Field


class SignUp(BaseModel):

    email:str = Field(min_length=1, strip_whitespace=True)
    password:str = Field(min_length=6, strip_whitespace=True)