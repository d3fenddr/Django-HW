class Book:
    def __init__(self, title='', year=0, publisher='', genre='', author='', price=0):
        self.title = title
        self.year = year
        self.publisher = publisher
        self.genre = genre
        self.author = author
        self.price = price

    def input_data(self):
        self.title = input("Enter the book title: ")
        self.year = int(input("Enter the year of publication: "))
        self.publisher = input("Enter the publisher: ")
        self.genre = input("Enter the genre: ")
        self.author = input("Enter the author: ")
        self.price = int(input("Enter the price of the book: "))

    def display_data(self):
        print(f"Title: {self.title}")
        print(f"Year: {self.year}")
        print(f"Publisher: {self.publisher}")
        print(f"Genre: {self.genre}")
        print(f"Author: {self.author}")
        print(f"Price: ${self.price}")

    def __str__(self):
        return (f"'{self.title}' by {self.author}, {self.year} ({self.publisher}), "
                f"Genre: {self.genre}, Price: ${self.price}")

    def __eq__(self, other):
        return (self.title == other.title and
                self.author == other.author and
                self.year == other.year)

    def __lt__(self, other):
        return self.price < other.price

    def __add__(self, other):
        return self.price + other.price