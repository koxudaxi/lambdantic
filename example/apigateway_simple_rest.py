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


class PathParameter(BaseModel):
    pet_id: int
    name: Optional[str]


@handler.get('/pets')
def get_pets() -> List[Pet]:
    return pets


@handler.get('/pets/<pet_id>')
def get_pet(pet_id: int) -> Pet:
    for pet in pets:
        if pet.pet_id == pet_id:
            return pet


@handler.get('/pets/<pet_id>/<name>', path_parameter_model=PathParameter)
def get_pet(path_parameter: PathParameter) -> Pet:
    for pet in pets:
        if pet.pet_id == path_parameter.pet_id:
            return pet


@handler.post('/pets', body_model=Pet, status_code=201)
def create_pet(pet: Pet) -> Pet:
    pet.pet_id = max(p.pet_id for p in pets)
    pets.append(pet)

    return pet


@handler.delete('/pets/<pet_id>')
def delete_pet(pet_id: int):
    target_pet = None
    for pet in pets:
        if pet.pet_id == pet_id:
            target_pet = pet
            break
    if target_pet:
        pets.remove(target_pet)
