#Python
from email.policy import default
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#Enum
from enum import Enum

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
    BLONDE = "blonde"
    BROWN = "brown"
    BLACK = "black"
    RED = "red"
    GREY = "grey"
    WHITE = "white"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(
        ...,
        title="First Name",
        description="The person's first name",
        max_length=50,
        min_length=2
        )
    last_name: str = Field(
        ...,
        title="Last Name",
        description="The person's last name",
        max_length=50,
        min_length=2
        )
    age: int = Field(
        ...,
        title="Age",
        description="The person's age",
        gt=0,
        lt=115
        )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(
        default=None
        )

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Facundo",
                "last_name": "Gonzalez",
                "age": 25,
                "hair_color": HairColor.BLONDE,
                "is_married": True
            }
        }

@app.get("/")
def home():
    return {"message": "Hello World"}

# Request and Response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validations: Query parameters

@app.get("/person/detail/")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description='This is the name of the person you are looking for. Its length must be between 1 and 50 characters.',
        ),
    age: str = Query(
        ...,
        title= 'Person Age',
        description='This is the age of the person you are looking for. Its required.',
        ),
):
    return {"name": name, "age": age}

# Validations: Path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person ID',
        description='This is the ID of the person you are looking for. Its required and must be greater than 0.',
        ),
):
    return {"person_id": person_id}

# Validations: Request body

@app.put("/person/{person_id}")
def update_person(
   person_id: int = Path(
       ...,
       gt=0,
       title='Person ID',
       description='This is the ID of the person you are looking for. Its required and must be greater than 0.',
    ),
   person: Person = Body(
       ...,
       title='Person',
       description='This is the person you are looking for. Its required.',
    ),
    Location: Location = Body(
        ...,
        title='Location',
        description='This is the location you are looking for. Its required.',)
):
    results = person.dict()
    results.update(Location.dict())
    return results