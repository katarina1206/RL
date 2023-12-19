class Dog:
    def __init__(self):
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.tiredness = 0
        self.age = 0
        self.age_thresholds = {'puppy': 2, 'adult': 5, 'senior': 8}  # Age thresholds for different life stages

    def get_life_stage(self):
        if self.age < self.age_thresholds['puppy']:
            return 'puppy'
        elif self.age < self.age_thresholds['adult']:
            return 'adult'
        elif self.age < self.age_thresholds['senior']:
            return 'senior'
        else:
            return 'elderly'

    def update_status(self, elapsed_time):
        life_stage = self.get_life_stage()

        # Set base rates
        hunger_rate = 1
        tiredness_rate = 1
        happiness_decay = 1

        # Adjust rates based on life stage
        if life_stage == 'puppy':
            hunger_rate = 1.2
            tiredness_rate = 0.5
            happiness_decay = 0.8
        elif life_stage == 'adult':
            # Keeping adult rates as base rates
            pass
        elif life_stage == 'senior':
            hunger_rate = 0.8
            tiredness_rate = 1.5
            happiness_decay = 1.2
        elif life_stage == 'elderly':
            hunger_rate = 0.6
            tiredness_rate = 2.0
            happiness_decay = 1.5

        # Update the dog's status
        self.age += elapsed_time / 10  # Aging rate
        self.hunger = min(100, self.hunger + hunger_rate)
        self.tiredness = min(100, self.tiredness + tiredness_rate)

        if self.hunger > 50 or self.tiredness > 50:
            self.happiness = max(0, self.happiness - happiness_decay)

    def feed(self):
        # Feeding the dog decreases hunger but increases tiredness
        self.hunger = max(0, self.hunger - 30)
        self.tiredness = min(100, self.tiredness + 10)
        self.happiness = min(100, self.happiness + 5)

    def walk(self):
        # Walking the dog decreases tiredness, increases happiness, but also makes it hungry
        self.tiredness = min(100, self.tiredness + 20)
        self.happiness = min(100, self.happiness + 10)
        self.hunger = min(100, self.hunger + 10)

    def play(self):
        # Playing with the dog increases happiness but also increases tiredness and hunger
        self.happiness = min(100, self.happiness + 15)
        self.tiredness = min(100, self.tiredness + 20)
        self.hunger = min(100, self.hunger + 15)

    def sleep(self):
        # Sleeping decreases tiredness, increases hunger, and slightly decreases happiness
        self.tiredness = 0
        self.hunger = max(0, self.hunger - 10)
        self.happiness = max(0, self.happiness - 5)

    def print_status(self):
        life_stage = self.get_life_stage()
        print(f"Health: {self.health}, Hunger: {self.hunger}, Happiness: {self.happiness}, "
              f"Tiredness: {self.tiredness}, Age: {self.age:.1f}, Life stage: {life_stage}")
