#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int#Optional[int] = None
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

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