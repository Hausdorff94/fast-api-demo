# 1. Introduction
!["Uvicorn, Starlette and Pydantic"]("images/uvi-starlette.png")

* __Uvicorn:__ es una librería de Python que funciona de servidor, es decir, permite que cualquier computadora se convierta en un servidor

* __Starlette:__ es un framework de desarrollo web de bajo nivel, para desarrollar aplicaciones con este requieres un amplio conocimiento de Python, entonces FastAPI se encarga de añadirle funcionalidades por encima para que se pueda usar mas fácilmente

* __Pydantic:__ Es un framework que permite trabajar con datos similar a pandas, pero este te permite usar modelos los cuales aprovechara FastAPI para crear la API

- - - -

## Install the environment and libraries

1. `virtualenv .env_fastapi_hw`

2. `source .env_fastapi_hw`

3. `pip install fastapi uvicorn`

- - - -

## Hello World!

1. Create script  ::`main.py`::

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello World"}
```

2. Run the script :

`uvicorn main:app --reload`

- - - -

## Documentation
`domain/docs`

`domain/redoc`

- - - -