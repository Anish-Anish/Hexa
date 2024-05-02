class PetShelter:
    def __init__(self):
        self.available_pets = []

    def add_pet(self, pet):
        self.available_pets.append(pet)

    def remove_pet(self, pet):
        if pet in self.available_pets:
            self.available_pets.remove(pet)
        else:
            print(f"{pet.name} is not available for adoption.")

    def list_available_pets(self):
        print("Available Pets:")
        for pet in self.available_pets:
            print(pet)
