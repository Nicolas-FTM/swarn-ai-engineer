# Example Schemas for no duplication between frontend and backend services

from pydantic import BaseModel, Field

class ExampleResponse(BaseModel):
    id: int
    name: str
    email: str

class ExampleRequest(BaseModel):
    name: str
    email: str