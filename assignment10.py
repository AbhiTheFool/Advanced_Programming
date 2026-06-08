class Location:
    def __init__(self, road, town, postal_code):
        self.road = road
        self.town = town
        self.postal_code = postal_code

    def show(self):
        return f"{self.road}, {self.town} - {self.postal_code}"


class Learner:
    def __init__(self, full_name, age, location):
        self.full_name = full_name
        self._age = None  # protected attribute
        self.age = age    # setter validation
        self.location = location   # HAS-A relationship (composition)
        self.subjects = []  # mutable list

    # Property for age
    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value <= 0 or value > 100:
            raise ValueError("Age must be between 1 and 100")
        self._age = value

    def add_subject(self, subject):
        if not subject:
            raise ValueError("Subject cannot be empty")
        self.subjects.append(subject)

    def display(self):
        print(f"Name: {self.full_name}")
        print(f"Age: {self.age}")
        print(f"Location: {self.location.show()}")
        print(f"Subjects: {self.subjects}")


class MeritLearner(Learner):
    def __init__(self, full_name, age, location, reward_amount):
        super().__init__(full_name, age, location)
        self.reward_amount = reward_amount

    @property
    def reward_amount(self):
        return self._reward_amount

    @reward_amount.setter
    def reward_amount(self, value):
        if value < 0:
            raise ValueError("Reward cannot be negative")
        self._reward_amount = value

    def display(self):
        super().display()
        print(f"Reward Amount: {self.reward_amount}")


# Driver code
if __name__ == "__main__":

    loc = Location("Beltola Main Rd", "Guwahati", "781028")

    student1 = Learner("Neeraj", 19, loc)
    student1.add_subject("Chemistry")
    student1.add_subject("Biology")

    print("\n--- Learner Details ---")
    student1.display()

    student2 = MeritLearner("Sneha", 21, loc, 7000)
    student2.add_subject("Data Science")
    student2.add_subject("Statistics")

    print("\n--- Merit Learner Details ---")
    student2.display()

    # Testing validation
    try:
        student1.age = 150
    except ValueError as e:
        print("\nError:", e)
