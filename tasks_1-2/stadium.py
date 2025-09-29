class Stadium:
    def __init__(self, name='', opening_date='', country='', city='', capacity=0):
        self.name = name
        self.opening_date = opening_date
        self.country = country
        self.city = city
        self.capacity = capacity

    def input_data(self):
        self.name = input("Enter the name of the stadium: ")
        self.opening_date = input("Enter the opening date (e.g., 01.01.2000): ")
        self.country = input("Enter the country: ")
        self.city = input("Enter the city: ")
        self.capacity = int(input("Enter the capacity: "))

    def display_data(self):
        print(f"Stadium Name: {self.name}")
        print(f"Opening Date: {self.opening_date}")
        print(f"Country: {self.country}")
        print(f"City: {self.city}")
        print(f"Capacity: {self.capacity} people")

    def __str__(self):
        return (f"{self.name} in {self.city}, {self.country}, opened on {self.opening_date}, "
                f"Capacity: {self.capacity}")

    def __eq__(self, other):
        return self.name == other.name and self.city == other.city and self.country == other.country

    def __lt__(self, other):
        return self.capacity < other.capacity

    def __add__(self, other):
        return self.capacity + other.capacity