class Pet:
    def __init__(self, name, age, ownerId, petId, breed, species, weight):
        self.name = name
        self.age = age
        self.ownerId = ownerId
        self.petId = petId
        self.breed = breed
        self.species = species
        self.weight = weight

    def toJson(self):
        return {'name': self.name,
                'age': self.age,
                'ownerId': self.ownerId,
                'petId': self.petId,
                'breed': self.breed,
                'species': self.species,
                'weight': self.weight
            }

    def toDict(self):
        return {'petId': self.petId,
            'userId': self.ownerId,
            'PetName': self.name,
            'PetAge': self.age,
            'PetBreed': self.breed,
            'PetSpecies': self.species,
            'PetWeight': self.weight
        }