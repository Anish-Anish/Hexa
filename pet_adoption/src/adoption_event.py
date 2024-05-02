from abc import ABC, abstractmethod

class IAdoptable(ABC):
    @abstractmethod
    def adopt(self):
        pass

class AdoptionEvent:
    def __init__(self):
        self.participants = []

    def host_event(self):
        print("Adoption event is being hosted.")
        print("Participants who are in the event:")
        for participant in self.participants:
            print(participant.__class__.__name__)

    def register_participant(self, participant):
        self.participants.append(participant)

class Shelter(IAdoptable):
    def adopt(self):
        print("Adoption process handled by the shelter.")

class Adopter(IAdoptable):
    def adopt(self):
        print("Adoption process handled by the adopter.")
