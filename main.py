# Python

# Enum
from enum import Enum
from typing import Optional

# FastAPI
from fastapi import Body, Path, Query, Form, Cookie, Header, File, UploadFile
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException

# Pydantic
from pydantic import EmailStr
from pydantic import BaseModel, Field

app = FastAPI()

# Models

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


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        title="First Name",
        description="The person's first name",
        max_length=50,
        min_length=2,
        example='John'
    )
    last_name: str = Field(
        ...,
        title="Last Name",
        description="The person's last name",
        max_length=50,
        min_length=2,
        example='Doe'
    )
    age: int = Field(
        ...,
        title="Age",
        description="The person's age",
        gt=0,
        lt=115,
        example=25
    )
    hair_color: Optional[HairColor] = Field(
        default=None, example=HairColor.BLONDE)
    is_married: Optional[bool] = Field(default=None, example=False)

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Johny",
    #             "last_name": "Vallejo",
    #             "age": 25,
    #             "hair_color": HairColor.BLONDE,
    #             "is_married": True,
    #             "password": "example_password"
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(..., min_length=8, example='example_password')


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=10, example='johndoe')
    messages: str = Field(default='Login successful')


@app.get(
    path="/",
    status_code=status.HTTP_200_OK
)
def home():
    return {"message": "Hello World"}

# Request and Response body


@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create a new person in the application",
    )
def create_person(person: Person = Body(...)):
    """
    Create a new person

    This endpoint will create a new person based on the information provided and save it to the database.

    Parameters:
    - Request body parameters:
        - **person: Person** -> The person model with first name, last name, age, hair color, marital status and password.

    Returns:
    A person model with the person's first name, last name, age, hair color, marital status and password.
    """
    return person

# Validations: Query parameters


@app.get(
    path="/person/detail/",
    status_code=status.HTTP_102_PROCESSING,
    tags=["Persons"],
    deprecated = True,
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Person Name',
        description='This is the name of the person you are looking for. Its length must be between 1 and 50 characters.',
        example='Karla'
    ),
    age: str = Query(
        ...,
        title='Person Age',
        description='This is the age of the person you are looking for. Its required.',
        example=33
    ),
):
    return {"name": name, "age": age}

# Validations: Path parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path = "/person/detail/{person_id}",
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person ID',
        description='This is the ID of the person you are looking for. Its required and must be greater than 0.',
        example=1,
        tags=["Persons"]
    ),
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )
    else:
        return {"person_id": person_id}

# Validations: Request body


@app.put(
    path = "/person/{person_id}",
    tags=["Persons"]
    )
def update_person(
    person_id: int = Path(
        ...,
        gt=0,
        title='Person ID',
        description='This is the ID of the person you are looking for. Its required and must be greater than 0.',
        example=132
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

# Forms


@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    tags=["Forms"]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and Headers Parameters


@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=["Cookies and Headers"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent


# Files

@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...),
):
    return {
        "File name": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read()) / 1024, 2)
    }
