class Dog:
    def __init__(self):
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.tiredness = 0

    def update_status(self):
        # This method will update the dog's status over time
        # Increase hunger and tiredness, decrease happiness if hunger or tiredness is high
        self.hunger = min(100, self.hunger + 1)
        self.tiredness = min(100, self.tiredness + 1)
        if self.hunger > 50 or self.tiredness > 50:
            self.happiness = max(0, self.happiness - 1)

    def feed(self):
        # Feeding the dog decreases hunger
        self.hunger = max(0, self.hunger - 30)
        self.happiness = min(100, self.happiness + 5)

    def walk(self):
        # Walking the dog decreases tiredness and increases happiness
        self.tiredness = max(0, self.tiredness - 20)
        self.happiness = min(100, self.happiness + 10)

    def play(self):
        # Playing with the dog increases happiness but also increases tiredness
        self.happiness = min(100, self.happiness + 15)
        self.tiredness = min(100, self.tiredness + 10)

    def sleep(self):
        # Sleeping decreases tiredness and hunger
        self.tiredness = 0
        self.hunger = max(0, self.hunger - 10)

    def print_status(self):
        print(f"Health: {self.health}, Hunger: {self.hunger}, Happiness: {self.happiness}, Tiredness: {self.tiredness}")