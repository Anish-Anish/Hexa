from src.pet import Pet, Dog, Cat
from src.pet_shelter import PetShelter
from src.donation import CashDonation, ItemDonation
from src.exceptions import InvalidPetAgeError, NullReferenceError, InsufficientFundsError, FileHandlingError, AdoptionException
from src.adoption_event import AdoptionEvent, Shelter, Adopter

def main():

    pet1 = Pet("Bloo", 5, "Golden Retriever")
    dog1 = Dog("Bloo", 3, "Labrador", "Golden Retriever")
    cat1 = Cat("Sheero", 2, "Siamese", "Grey")


    shelter = PetShelter()


    try:
        shelter.add_pet(pet1)
        shelter.add_pet(dog1)
        shelter.add_pet(cat1)
    except NullReferenceError as e:
        print(f"Error: {e}")


    try:
        shelter.list_available_pets()
    except NullReferenceError as e:
        print(f"Error: {e}")


    shelter.remove_pet(dog1)


    try:
        print("After removing Bloo:")
        shelter.list_available_pets()
    except NullReferenceError as e:
        print(f"Error: {e}")


    try:
        cash_donation = CashDonation("Ilakiya", 5430)
        cash_donation.record_donation()
        item_donation = ItemDonation("Rangaraju", 10786, "Food")
        item_donation.record_donation()
    except InsufficientFundsError as e:
        print(f"Error: {e}")


    event = AdoptionEvent()
    shelter = Shelter()
    adopter = Adopter()
    event.register_participant(shelter)
    event.register_participant(adopter)
    event.host_event()


    shelter = PetShelter()
    try:
        shelter.add_pet(Pet("Juno", 3, "Labrador"))
        shelter.add_pet(Pet("Sheero", 2, "Siamese"))
        shelter.adopt_pet("Juno")
        shelter.adopt_pet("Raju")
        shelter.adopt_pet("Sheero")
    except AdoptionException as e:
        print(f"Adoption Error: {e}")

if __name__ == "__main__":
    main()
