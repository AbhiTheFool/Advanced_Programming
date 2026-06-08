from abc import ABC, abstractmethod

# Abstract base class — every library item must have title & year
class LibraryItem(ABC):
    total_items = 0  # shared counter across ALL items

    def __init__(self, title, year):
        self.title = title
        self.year  = year
        LibraryItem.total_items += 1  # tick up every time

    @abstractmethod
    def displayInfo(self):
        pass  # child classes MUST implement this


# Book subclass — adds author, year has a default value
class Book(LibraryItem):
    def __init__(self, title, year=2024, author="Unknown"):
        super().__init__(title, year)
        self.author = author

    def displayInfo(self):
        print("[Book]", self.title)
        print("  Year  :", self.year)
        print("  Author:", self.author)


# DVD subclass — adds duration and genre
class DVD(LibraryItem):
    def __init__(self, title, year, duration, genre):
        super().__init__(title, year)
        self.duration = duration
        self.genre    = genre

    def displayInfo(self):
        print("[DVD] ", self.title)
        print("  Year    :", self.year)
        print("  Duration:", self.duration, "min")
        print("  Genre   :", self.genre)


# Driver — mix of Books and DVDs in one list (polymorphism)
items = [
    Book("Wings of Fire",   1999, "A.P.J. Abdul Kalam"),
    Book("The Alchemist",   author="Paulo Coelho"),  # year defaults to 2024
    DVD("Dangal",          2016, 161, "Sports Drama"),
]

for item in items:
    item.displayInfo()  # Python picks the right version automatically

print("Total items:", LibraryItem.total_items)  # → 3
