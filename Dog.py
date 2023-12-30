import random


class Dog:
    def __init__ (self, gui_callback = None): 
        self.gui_callback = gui_callback
    #def __init__(self):
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.tiredness = 0
        self.age = 0
        self.age_thresholds = {'puppy': 2, 'adult': 5, 'senior': 8}  # Age thresholds for different life stages
        self.money = 100  # Initial money
        self.available_tricks = {'sit': 0.1, 'roll over': 0.2, 'fetch': 0.15, 'stay': 0.05, 'dance': 0.25}
        self.learned_tricks = {}
        self.tricks = []  # List of learned tricks
        self.food_cost = 5  # Cost of food per feeding
        self.action_count = 0

        # Hidden Attributes
        self._cleanliness = 100
        self._social_need = 100
        self.lifespan = random.uniform(17, 25)
        self.flea_treatment_count = 0  # Tracks the number of flea treatments

        self.state = "normal"  # Possible states: "normal", "vet_visit", "sudden_illness", "flea_event"

    def get_state(self):
        return self.state

    def trigger_event(self):
        # Randomly decide whether to trigger an event
        if random.random() < 0.1:  # 10% chance for an event to occur
            self.handle_event()

    def handle_event(self):
        events = {
            self.vet_visit: "vet_visit",
            self.sudden_illness: "sudden_illness",
            self.flea_event: "flea_event"
        }
        chosen_event, event_state = random.choice(list(events.items()))
        self.state = event_state  # Update the state to reflect the current event
        chosen_event()

    def vet_visit(self):
        # print("Your dog seems to be feeling unwell. Do you take it to the vet? (yes/no)")
        # choice = input().lower()
        if self.gui_callback:
            choice = self.gui_callback("Your dog seems to be feeling unwell. Do you take it to the vet?")
        actual_condition = random.choice(['needs_care', 'fine'])  # Randomize the actual condition of the dog

        if choice == 'yes':
            if actual_condition == 'needs_care':
                self.health = min(100, self.health + 20)  # Significant health improvement
                self.happiness = max(0, self.happiness - 5)  # Slight decrease in happiness due to vet visit stress
                if self.gui_callback:
                    self.gui_callback ("The vet visit was necessary! Your dog's health improves, but the visit was a bit stressful.")
                #print("The vet visit was necessary! Your dog's health improves, but the visit was a bit stressful.")
            else:
                self.happiness = max(0, self.happiness - 10)  # Larger decrease in happiness
                if self.gui_callback:
                    self.gui_callback ("The vet found nothing wrong. Your dog is healthy but didn't enjoy the unnecessary visit.")
                #print("The vet found nothing wrong. Your dog is healthy but didn't enjoy the unnecessary visit.")
        else:
            if actual_condition == 'needs_care':
                self.health = max(0, self.health - 25)  # Significant health decrease
                self.happiness = max(0, self.happiness - 15)  # Decrease in happiness
                if self.gui_callback:
                    self.gui_callback ("Unfortunately, your dog needed medical attention and its condition has worsened significantly.")
                #print("Unfortunately, your dog needed medical attention and its condition has worsened significantly.")
            else:
                self.happiness = min(100, self.happiness + 5)  # Increase in happiness
                if self.gui_callback:
                    self.gui_callback("Your dog was actually fine and is happy to have avoided a stressful vet visit.")
                #print("Your dog was actually fine and is happy to have avoided a stressful vet visit.")
        self.state = "normal"

    def sudden_illness(self):
        # print(
        #     "Your dog has gotten into a bad accident. The dog looks okay, but would you like the vet to check? (yes/no)")
        # choice = input().lower()
        if self.gui_callback:
            choice = self.gui_callback("Your dog has gotten into a bad accident. Would you like the vet to check?")
        actual_condition = random.choice(['needs_care', 'fine'])

        if choice == 'yes':
            if actual_condition == 'needs_care':
                self.health = min(100, self.health + 25)  # The dog needed care and gets better

                if self.gui_callback:
                    self.gui_callback("It was a good decision to visit the vet. Your dog needed medical attention and is now feeling better")
                #print(
                    #"It was a good decision to visit the vet. Your dog needed medical attention and is now feeling better.")
            else:
                self.happiness = max(0, self.happiness - 10)  # The dog was fine and the visit stressed it
               
                if self.gui_callback:
                    self.gui_callback("The vet found nothing wrong. Your dog is a bit stressed from the visit.")
                #print("The vet found nothing wrong. Your dog is a bit stressed from the visit.")
        else:
            if actual_condition == 'needs_care':
                self.health = max(0, self.health - 30)  # The dog needed care and didn't get it
                self.happiness = max(0, self.happiness - 20)
               
                if self.gui_callback:
                    self.gui_callback("Unfortunately, your dog needed medical attention and its condition has worsened.")
                #print("Unfortunately, your dog needed medical attention and its condition has worsened.")
            else:
           
                if self.gui_callback:
                    self.gui_callback("Yiour dog seems to be doing finewithout the vet's help.")
                #print("Your dog seems to be doing fine without the vet's help.")
        self.state = "normal"


    def flea_event(self):
        if self.flea_treatment_count > 0:
            
            if self.gui_callback:
                    self.gui_callback("Your dog is already undergoing flea treatment.")
            #print("Your dog is already undergoing flea treatment.")
            return  # Skip initiating the flea event if treatment is ongoing

        
        if self.gui_callback:
                    self.gui_callback("Your dog has fleas! The treatment needs to be administered three times.")
        #print("Your dog has fleas! The treatment needs to be administered three times.")
        self.flea_treatment_count = 0  # Reset the treatment count
        self.administer_flea_treatment()  # Start the first treatment

    def administer_flea_treatment(self):
        if self.flea_treatment_count < 3:
            self.flea_treatment_count += 1
            self.happiness = max(0, self.happiness - 10)  # Decrease happiness due to the unpleasant treatment
            if self.gui_callback:
                    self.gui_callback (f"Flea treatment administered ({self.flea_treatment_count}/3). Your dog is not happy about it.")
            #print(f"Flea treatment administered ({self.flea_treatment_count}/3). Your dog is not happy about it.")

            if self.flea_treatment_count == 3:
                
                if self.gui_callback:
                    self.gui_callback("The fleas are gone!")
                #print("The fleas are gone! Your dog's happiness will now gradually improve.")
                self.happiness = min(100, self.happiness + 20)  # Increase happiness as the fleas are gone
                self.state = "normal"

        else:
            
            if self.gui_callback:
                    self.gui_callback("Flea treatment is already complete.")
            #print("Flea treatment is already complete.")
            self.state = "normal"


    def teach_trick(self, get_trick_name_callback=None):
        self.state = "teaching_trick"
        #print("Available tricks to teach: " + ", ".join(self.available_tricks.keys()))
        #trick_name = input("Enter the name of the trick you want to teach: ")
        trick_name = get_trick_name_callback() if get_trick_name_callback else input("Enter the name of the trick you want to teach: ")

        if trick_name in self.available_tricks and trick_name not in self.learned_tricks:
            learning_chance = self.available_tricks[trick_name] * (2 if self.age < self.age_thresholds['adult'] else 1)
            if random.random() < learning_chance:
                self.learned_tricks[trick_name] = self.available_tricks[trick_name]
                #print(f"{trick_name} trick learned!")
                if self.gui_callback:
                    self.gui_callback (f"{trick_name} trick learned!")
            else:
                #print("Failed to learn the trick this time.")
                if self.gui_callback:
                    self.gui_callback ("Failed to learn the trick this time.")
        else:
            #print("Invalid trick name or already learned.")
            if self.gui_callback:
                    self.gui_callback ("Invalid trick name or already learned.")

        self.state = "normal"

    def participate_in_show(self):
        if not self.learned_tricks:
            #print("The dog needs to know at least one trick to compete.")
            if self.gui_callback:
                    self.gui_callback ("The dog needs to know at least one trick to compete.")
            return False

        success_chance = sum(self.learned_tricks.values())
        if random.random() < success_chance:
            prize_money = 20
            self.money += prize_money
            #print(f"Congratulations! You won the show and earned ${prize_money}.")
            if self.gui_callback:
                    self.gui_callback (f"Congratulations! You won the show and earned ${prize_money}.")
            return True
        else:
            if self.gui_callback:
                    self.gui_callback ("Better luck next time in the show.")
            #print("Better luck next time in the show.")
            return False


    def get_life_stage(self):
        if self.age >= self.lifespan:
            return 'old_age'
        elif self.age < self.age_thresholds['puppy']:
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
            hunger_rate = 6.0
            tiredness_rate = 4.0
            happiness_decay = 0.5
            health_improvement = 5.0
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
        self._cleanliness = max(0, self._cleanliness - 3)
        self._social_need = max(0, self._social_need - 2)
        self.age = self.action_count / 12 # Aging rate
        self.hunger = min(100, self.hunger + hunger_rate)
        self.tiredness = min(100, self.tiredness + tiredness_rate)

        # Update happiness and health based on needs
        if self.hunger > 50 or self.tiredness > 50:
            self.happiness = max(0, self.happiness - happiness_decay)
        if self._cleanliness < 50 or self._social_need < 50:
            self.happiness = max(0, self.happiness - 1)

        # Adjust health based on needs
        good_conditions = 0
        if self.hunger < 50:
            good_conditions += 1
        if self.tiredness < 50:
            good_conditions += 1
        if self.happiness > 50:
            good_conditions += 1
        if self._cleanliness > 50:
            good_conditions += 1
        if self._social_need > 50:
            good_conditions += 1

        # Apply health improvement or decay based on conditions
        if good_conditions >= 4:  # Improve health if at least 3 out of 4 conditions are met
            self.health = min(100, self.health + health_improvement)
        else:
            # Apply decay rate if conditions for improvement are not met
            if self.hunger > 70 or self.tiredness > 70 or self._cleanliness < 30 or self._social_need < 30:
                health_decay *= 2  # Double the health decay rate if needs are neglected
            self.health = max(0, self.health - health_decay)

        self.trigger_event()

        self.action_count += 1

        if life_stage == 'old_age':
            return 'old_age'

        if self.health <= 0:
            return 'neglect'

        return 'alive'

    def feed(self):
        if self.money < self.food_cost:
            if self.gui_callback:
                    self.gui_callback("Not enough money to buy food.")
            return False

        if self.hunger >= 30:  # Only allow feeding if the dog is somewhat hungry
            self.happiness = max(0, self.happiness - 5)
            self._cleanliness = max(0, self._cleanliness - 5)
            self.hunger = max(0, self.hunger - 30)
            self.money -= self.food_cost
            if self.gui_callback:
                    self.gui_callback("You fed the dog.")
            return True
        else:
            if self.gui_callback:
                    self.gui_callback("The dog is not hungry enough to eat.")
            self.hunger = min(0, self.hunger + 10)  # The dog still becomes a bit less hungry over time
            self.tiredness = min(100, self.tiredness + 5)  # The dog gets slightly more tired
            return False

    def walk(self):
        # Walking the dog decreases tiredness, increases happiness, makes it hungry, affects cleanliness,
        # but slightly decreases health (due to exertion)
        if self.tiredness <= 70:  # Only allow walking if the dog is not too tired
            self.tiredness = min(100, self.tiredness + 20)
            self.happiness = min(100, self.happiness + 10)
            self.hunger = min(100, self.hunger + 10)
            self._cleanliness = max(0, self._cleanliness - 10)
            self.health = max(0, self.health - 2)

            # Random chance to improve socialization need
            if random.random() < 0.5:  # 50% chance
                self._social_need = min(100, self._social_need + 10)

            
            if self.gui_callback:
                    self.gui_callback("You took the dog for a walk.")
            #print("You took the dog for a walk.")
            return True
        else:
            if self.gui_callback:
                    self.gui_callback("The dog is too tired to go for a walk.")
            #print("The dog is too tired to go for a walk.")
            self.tiredness = min(100, self.tiredness + 10)  # The dog gets more tired regardless
            self.hunger = min(100, self.hunger + 5)  # The dog gets slightly hungrier
            return False

    def play(self):
        # Playing with the dog increases happiness but also increases tiredness, hunger, decreases cleanliness,
        # and slightly reduces health (due to potential rough play)
        if self.tiredness <= 70 and self.hunger <= 70:  # Check if the dog is not too tired or hungry to play
            self.happiness = min(100, self.happiness + 15)
            self.tiredness = min(100, self.tiredness + 20)
            self.hunger = min(100, self.hunger + 15)
            self._cleanliness = max(0, self._cleanliness - 15)
            self.health = max(0, self.health - 3)
           
            if self.gui_callback:
                    self.gui_callback("You played with the dog.")
            #print("You played with the dog.")
            return True
        else:
           
            if self.gui_callback:
                    self.gui_callback("The dog is too tired or hungry to play.")
            #print("The dog is too tired or hungry to play.")
            self.tiredness = min(100, self.tiredness + 10)  # The dog gets more tired regardless
            self.hunger = min(100, self.hunger + 5)  # The dog gets slightly hungrier
            return False

    def sleep(self):
        # Sleeping decreases tiredness, increases hunger, slightly decreases happiness (due to inactivity),
        # and slightly improves health
        self.tiredness = 0
        self.hunger = min(100, self.hunger + 10)
        self.happiness = max(0, self.happiness - 5)
        self._cleanliness = min(100, self._cleanliness + 5)
        #self.health = min(100, self.health + 2)
        if self.gui_callback:
                    self.gui_callback ("You've put your dog to bed.")
        return True

    def groom(self):
        # Grooming the dog increases cleanliness, slightly improves health, but reduces happiness (as many dogs do
        # not enjoy grooming)
        self._cleanliness = 100
        self.health = min(100, self.health + 1)
        self.happiness = max(0, self.happiness - 10)
        #self.health = max(0, self.health - 4)
        if self.gui_callback:
                    self.gui_callback ("You've groomed the dog.")
        return True

    def socialise(self):
        # Socializing increases social needs and happiness, but increases tiredness and hunger, and slightly reduces
        # health (due to potential overexcitement)
        if self.happiness >= 50:  # Only allow socializing if the dog is in a good mood
            self._social_need = 100
            self.happiness = min(100, self.happiness + 15)
            self.tiredness = min(100, self.tiredness + 20)
            self.hunger = min(100, self.hunger + 10)
            #self.health = max(0, self.health - 2)
            
            if self.gui_callback:
                    self.gui_callback("You socialised the dog.")
            #print("You socialized the dog.")
            return True
        else:
            
            if self.gui_callback:
                    self.gui_callback("The dog is not in the mood to socialise.")
            #print("The dog is not in the mood to socialize.")
            self.happiness = max(0, self.happiness - 10)
            return False

    def print_status(self):
        life_stage = self.get_life_stage()
        print(f"Health: {self.health:.1f}, Hunger: {self.hunger:.1f}, Happiness: {self.happiness:.1f}, "
              f"Tiredness: {self.tiredness:.1f}, Age: {self.age:.1f}, Life stage: {life_stage}, "f" Money left: {self.money}")
