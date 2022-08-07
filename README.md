# apis
A simple implementation of an animal creation api based on FASTAPI.
Each animal is given an unique identifier. This is done through python's core 'uuid' package.
The idea was to create animals using parts of different animals. The parts categories are: [head, tail, torso, limbes].

POST-> /create-animal
Create an animal by giving it parts of other animals of the provided categories.

GET-> /get-animal/{u_id}
Get the animal base on the ID.

GET -> /get-animal/?name={name}&part={part}
Get the animal given the query parameter: [name, part]
The name parameter can be used the get the animal given its name. The part parameter is just there.

PUT -> /edit-animal/{uid}
Modify the characteristics of an existing animal based on its ID. Any newly defined property gets changed while preserving the other ones.

DELETE -> /delete-animal/{u_id}
Delete the existing animal based on its ID.
