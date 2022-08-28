from fastapi import FastAPI, HTTPException
import pydantic as pyd
from typing import Optional, Any
import json
import uuid

app = FastAPI()
#this is just a comment for test

class Animal(pyd.BaseModel):
    """Data Validation needs be implemented"""
    name: str
    limbs: str
    torso: str
    head: str
    tail: Optional[str]


class OptionalAnimal(Animal):
    name: Optional[str]
    limbs: Optional[str]
    torso: Optional[str]
    head:  Optional[str]


def create_id() -> str:
    """
    Create a universal unique identifier for the data.
    The UUID.uuid4() function is used for the ID creation.\n
    Returns the UUID in a string format.
    """

    u_id: uuid.UUID = uuid.uuid4()
    return str(u_id)


@app.post("/create-animal")
def create_animal(new_animal: Animal) -> dict[str, dict[str, str]] | HTTPException:
    """
    Create a new animal with the "Animal" class the model.
    Returns a dict of the new animal created with a UUID as the key.
    """

    try:
        with open("data.json", "r") as fr:
            database: dict = json.load(fr)

        animal_body = new_animal.dict()
        animal_id = create_id()
        full_animal = {animal_id: animal_body}

        database.update(full_animal)

        with open("data.json", "w") as fw:
            json.dump(database, fw)

        return {"new animal": {animal_id: animal_body}}

    except FileNotFoundError:
        return HTTPException(404, "Unable to access database")


@app.get("/get-animal/{u_id}/")
def get_animal(u_id: str) -> HTTPException | dict[str, str] | None:
    """
    Get the animal based on the ID given.
    """

    try:
        with open("data.json", "r") as f:
            database: dict = json.load(f)

        if u_id not in database:
            return HTTPException(404, "ID not found.")

        return database.get(u_id)

    except FileNotFoundError:
        return HTTPException(404, "Unable to access database")


@app.get("/get-animal/")
def get_animal(name: Optional[str] = None, part: Optional[str] = None) -> dict[str, list] | HTTPException:
    """
    Get the animal based on the name given to it.
    The 'part' parameter is just there. It doesn't do anything.
    """

    try:
        with open("data.json", "r") as f:
            database: dict = json.load(f)

        animal_list = database.values()

        if name or (name and part):
            striped_name = name[1: len(name)-1]
            out_result = [animal for animal in animal_list
                          if striped_name == animal["name"]]

        return {"result": out_result} if out_result else HTTPException(404, "Name not found")

    except FileNotFoundError:
        return HTTPException(404, "Unable to access database")


@app.put("/edit-animal/{u_id}")
def edit_animal(u_id: str, new_animal: OptionalAnimal) -> HTTPException | dict[str, dict[str, str]]:
    """
    Modifier the animal based on the ID given. 
    Any of the animal's characteristics can be modified, aside from its ID.\n
    Function returns the updated animal.
    """

    try:
        with open("data.json", "r") as fr:
            database: dict = json.load(fr)

        if u_id not in database:
            return HTTPException(404, "ID not found")

        # do the updation-->
        old_animal = database.get(u_id)       # the old values of the animal
        new_animal_dict = new_animal.dict()   # the new values of the animal

        for key in old_animal:
            if new_animal_dict[key] and (new_animal_dict[key] != old_animal[key]):
                old_animal[key] = new_animal_dict[key]

        database[u_id] = old_animal

        with open("data.json", "w") as fw:
            json.dump(database, fw)

        return {"updated animal": old_animal}

    except FileNotFoundError:
        return HTTPException(404, "Unable to access database")


@app.delete("/delete-animal/{u_id}")
def delete_animal(u_id: str) -> HTTPException | dict[str, Any]:
    """
    Deletes the animal based on its ID.\n
    Function returns the animal deleted.
    """

    try:
        with open("data.json", "r") as fr:
            database: dict = json.load(fr)

            if u_id not in database:
                return HTTPException(404, "ID not found")

            animal_deleted = database.pop(u_id)

        with open("data.json", "w") as fw:
            json.dump(database, fw)

        return {"animal deleted": animal_deleted}

    except FileNotFoundError:
        return HTTPException(404, "Unable to access database")
