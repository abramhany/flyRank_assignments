from pydantic import BaseModel , Field


class Item(BaseModel):

    title:str = Field(min_length=1, strip_whitespace=True)

class Update(BaseModel):
    
    title:str = Field(min_length=1, strip_whitespace=True)
    done:bool 
    
