"""
User management endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from shared.schemas.example import ExampleRequest, ExampleResponse

router = APIRouter()

# Simulación de una "base de datos"
fake_db = {
            1: {
                "id": 1,
                "name": "Ana",
                "email": "ana@mail.com"
                },
            2: {
                "id": 2,
                "name": "Juan",
                "email": "juan@mail2.com"
            },
            3: {
                "id": 3,
                "name": "María",
                "email": "maria@mail.com"
            }
        }

@router.post("/retrieve/{id}", response_model=ExampleResponse)
async def retrieve_user(id: int):
    """
    Retrieve an example.
    """
    example = fake_db.get(id)
    if not example:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found")
    
    return example

@router.get("/retrieve", response_model=ExampleResponse)
async def retrieve_all():
    """
    Retrieve all examples.
    """
    examples = list(fake_db.values())

    if len(examples) == 0:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Examples List Empty",
        )
    return list(fake_db.values())
