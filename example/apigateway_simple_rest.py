from typing import List, Optional

from pydantic import BaseModel, Schema

from lambdantic.apigateway import Handler

handler = Handler()


class Pet(BaseModel):
    pet_id: Optional[int] = Schema(..., alias='id')
    name: str
    age: int


# database
pets = [
        Pet(id=1, name='dog', age=3),
        Pet(id=2, name='cat', age=2)
    ]


@handler.get('/pets')
def get_pets() -> List[Pet]:
    return pets


@handler.get('/pets/<pet_id>')
def get_pet(pet_id: int) -> Pet:
    for pet in pets:
        if pet.pet_id == pet_id:
            return pet


@handler.post('/pets', body_model=Pet, status_code=201)
def crate_pet(pet: Pet) -> Pet:
    pet.pet_id = max(p.pet_id for p in pets)
    pets.append(pet)

    return pet
