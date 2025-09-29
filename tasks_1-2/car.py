class Car:
    def __init__(self, model='', year=0, manufacturer='', engine_volume=0.0, color='', price=0):
        self.model = model
        self.year = year
        self.manufacturer = manufacturer
        self.engine_volume = engine_volume
        self.color = color
        self.price = price

    def input_data(self):
        self.model = input("Enter the car model: ")
        self.year = int(input("Enter the year of manufacture: "))
        self.manufacturer = input("Enter the manufacturer: ")
        self.engine_volume = float(input("Enter the engine volume (liters): "))
        self.color = input("Enter the color of the car: ")
        self.price = int(input("Enter the price of the car: "))

    def display_data(self):
        print(f"Model: {self.model}")
        print(f"Year: {self.year}")
        print(f"Manufacturer: {self.manufacturer}")
        print(f"Engine Volume: {self.engine_volume} L")
        print(f"Color: {self.color}")
        print(f"Price: ${self.price}")

    def __str__(self):
        return (f"{self.manufacturer} {self.model} ({self.year}), "
                f"Engine: {self.engine_volume}L, Color: {self.color}, Price: ${self.price}")

    def __eq__(self, other):
        return (self.model == other.model and
                self.year == other.year and
                self.manufacturer == other.manufacturer)

    def __lt__(self, other):
        return self.price < other.price

    def __add__(self, other):
        return self.price + other.price