import random
class Dog:
    def __init__(self):
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.tiredness = 0
        self.age = 0
        self.age_thresholds = {'puppy': 2, 'adult': 5, 'senior': 8}  # Age thresholds for different life stages

        # Hidden Attributes
        self._cleanliness = 100
        self._social_need = 100

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

        # Set base rates and health decay factor
        hunger_rate = 1
        tiredness_rate = 1
        happiness_decay = 1
        health_decay = 2.0  # Base health decay rate
        health_improvement = 2.0  # Base health improvement rate

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
            health_decay = 2.5
            health_improvement = 2.5
        elif life_stage == 'elderly':
            hunger_rate = 0.6
            tiredness_rate = 2.0
            happiness_decay = 1.5
            health_decay = 3.5
            health_improvement = 1.0

        # Update hidden and visible attributes
        self._cleanliness = max(0, self._cleanliness - 0.5)
        self._social_need = max(0, self._social_need - 0.2)
        self.age += elapsed_time / 10  # Aging rate
        self.hunger = min(100, self.hunger + hunger_rate)
        self.tiredness = min(100, self.tiredness + tiredness_rate)

        # Update happiness and health based on needs
        if self.hunger > 50 or self.tiredness > 50:
            self.happiness = max(0, self.happiness - happiness_decay)
        if self._cleanliness < 50 or self._social_need < 50:
            self.happiness = max(0, self.happiness - 1)

        # Adjust health based on needs
        if self.hunger < 30 and self.tiredness < 30 and self._cleanliness > 70 and self._social_need > 70:
            self.health = min(100, self.health + health_improvement)  # Health improves if all needs are well managed
        elif self.hunger > 70 or self.tiredness > 70 or self._cleanliness < 30 or self._social_need < 30:
            health_decay *= 2  # Double the health decay rate if needs are neglected
        self.health = max(0, self.health - health_decay)

    def feed(self):
        # Feeding the dog decreases hunger but increases tiredness and slightly decreases cleanliness
        self.hunger = max(0, self.hunger - 30)
        self.tiredness = min(100, self.tiredness + 10)
        self.happiness = min(100, self.happiness + 5)
        self._cleanliness = max(0, self._cleanliness - 5)

    def walk(self):
        # Walking the dog decreases tiredness, increases happiness, makes it hungry, and affects cleanliness and
        # social needs
        self.tiredness = max(0, self.tiredness - 20)
        self.happiness = min(100, self.happiness + 10)
        self.hunger = min(100, self.hunger + 10)
        self._cleanliness = max(0, self._cleanliness - 10)

        # Random chance to improve socialization need
        if random.random() < 0.5:  # 50% chance
            self._social_need = min(100, self._social_need + 10)

    def play(self):
        # Playing with the dog increases happiness but also increases tiredness, hunger, and decreases cleanliness
        self.happiness = min(100, self.happiness + 15)
        self.tiredness = min(100, self.tiredness + 20)
        self.hunger = min(100, self.hunger + 15)
        self._cleanliness = max(0, self._cleanliness - 15)

    def sleep(self):
        # Sleeping decreases tiredness, increases hunger, slightly decreases happiness, and slightly improves
        # cleanliness
        self.tiredness = 0
        self.hunger = max(0, self.hunger - 10)
        self.happiness = max(0, self.happiness - 5)
        self._cleanliness = min(100, self._cleanliness + 5)

    def groom(self):
        self._cleanliness = 100

    def socialize(self):
        self._social_need = 100

    def print_status(self):
        life_stage = self.get_life_stage()
        print(f"Health: {self.health:.1f}, Hunger: {self.hunger:.1f}, Happiness: {self.happiness:.1f}, "
              f"Tiredness: {self.tiredness:.1f}, Age: {self.age:.1f}, Life stage: {life_stage}")