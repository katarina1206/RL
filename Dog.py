import random


class Dog:
    def __init__ (self, gui_callback = None, rl_agent = None):
        # self.rl_agent = rl_agent
        self.gui_callback = gui_callback
    #def __init__(self):
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.tiredness = 0
        self.age = 0
        self.rl_agent = rl_agent
        self.age_thresholds = {'puppy': 2, 'adult': 5, 'senior': 8}  # Age thresholds for different life stages

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

        # Return the decision state if the event involves a decision
        if event_state in ['vet_visit', 'sudden_illness']:
            return event_state
        else:
            return None

    def vet_visit(self):
        print("Your dog seems to be feeling unwell. Do you take it to the vet? (yes/no)")
        choice = self.rl_agent.select_action(self.get_current_state())[1]
        print(f"RL Agent selected choice: {choice}")
        actual_condition = random.choice(['needs_care', 'fine'])  # Randomize the actual condition of the dog

        if choice == 'yes':
            if actual_condition == 'needs_care':
                self.health = min(100, self.health + 20)  # Significant health improvement
                #print("vet_visit health value" , self.health)
                self.happiness = max(0, self.happiness - 5)  # Slight decrease in happiness due to vet visit stress
                print("The vet visit was necessary! Your dog's health improves, but the visit was a bit stressful.")
            else:
                self.happiness = max(0, self.happiness - 10)  # Larger decrease in happiness
                #print("vet_visit happines value" , self.happiness)
                print("The vet found nothing wrong. Your dog is healthy but didn't enjoy the unnecessary visit.")
        else:
            if actual_condition == 'needs_care':
                self.health = max(0, self.health - 25)  # Significant health decrease
                self.happiness = max(0, self.happiness - 15)  # Decrease in happiness
                print("Unfortunately, your dog needed medical attention and its condition has worsened significantly.")
            else:
                self.happiness = min(100, self.happiness + 5)  # Increase in happiness
                print("Your dog was actually fine and is happy to have avoided a stressful vet visit.")

        # Call update_q_values to update Q-values for vet_visit state
        self.rl_agent.update_q_values(self.get_current_state(), choice, self.get_current_state())

        self.state = "normal"

    def sudden_illness(self):
        print("Your dog has gotten into a bad accident. The dog looks okay, but would you like the vet to check? (yes/no)")
        choice = self.rl_agent.select_action(self.get_current_state())[1]
        print(f"RL Agent selected choice: {choice}")
        actual_condition = random.choice(['needs_care', 'fine'])
        
        # Update the Q-value using the RL agent's choice
        self.rl_agent.update_q_values(self.get_current_state(), choice, self.get_current_state())

        if choice == 'yes':
            if actual_condition == 'needs_care':
                self.health = min(100, self.health + 25)  # The dog needed care and gets better
                print("It was a good decision to visit the vet. Your dog needed medical attention and is now feeling better.")
            else:
                self.happiness = max(0, self.happiness - 10)  # The dog was fine and the visit stressed it
                print("sudden illness happines value", self.happiness)
                print("The vet found nothing wrong. Your dog is a bit stressed from the visit.")
        else:
            if actual_condition == 'needs_care':
                self.health = max(0, self.health - 30)  # The dog needed care and didn't get it
                self.happiness = max(0, self.happiness - 20)
                print("Unfortunately, your dog needed medical attention and its condition has worsened.")
            else:
                print("Your dog seems to be doing fine without the vet's help.")
        self.state = "normal"



    def flea_event(self):
        if self.flea_treatment_count > 0:
            print("Your dog is already undergoing flea treatment.")
            return  # Skip initiating the flea event if treatment is ongoing

        print("Your dog has fleas! The treatment needs to be administered three times.")
        self.flea_treatment_count = 0  # Reset the treatment count
        self.administer_flea_treatment()  # Start the first treatment

    def administer_flea_treatment(self):
        if self.flea_treatment_count < 3:
            self.flea_treatment_count += 1
            self.happiness = max(0, self.happiness - 10)  # Decrease happiness due to the unpleasant treatment
            print(f"Flea treatment administered ({self.flea_treatment_count}/3). Your dog is not happy about it.")

            if self.flea_treatment_count == 3:
                print("The fleas are gone! Your dog's happiness will now gradually improve.")
                self.happiness = min(100, self.happiness + 20)  # Increase happiness as the fleas are gone
                self.state = "normal"

        else:
            print("Flea treatment is already complete.")
            self.state = "normal"


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
        self._cleanliness = max(0, self._cleanliness - 0.5)
        self._social_need = max(0, self._social_need - 0.2)
        #print(f"Elapsed Time: {elapsed_time}, Previous Age: {self.age}")
        self.age += elapsed_time / 2 # Aging rate
        # Adjust aging rate based on life stage
        #aging_rate = 100  # Adjust this value based on your simulation
        #self.age += elapsed_time * aging_rate  # Aging rate
        #print(f"Updated Age: {self.age}")
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

        if life_stage == 'old_age':
            return 'old_age'

        if self.health <= 0:
            return 'neglect'

        return 'alive'

    def feed(self, health_decay):
        if self.hunger >= 30:  # Only allow feeding if the dog is somewhat hungry
            self.happiness = max(0, self.happiness - 5)
            self._cleanliness = max(0, self._cleanliness - 5)
            self.hunger = max(0, self.hunger - 30)
            print("You fed the dog.")
            return True
        else:
            print("The dog is not hungry enough to eat.")
            self.hunger = max(0, self.hunger - 10)  # The dog still becomes a bit less hungry over time
            self.tiredness = min(100, self.tiredness + 5)  # The dog gets slightly more tired
            self.health = max(0, self.health - health_decay)
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
            print("You took the dog for a walk.")
            return True
        else:
            print("The dog is too tired to go for a walk.")
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
            print("You played with the dog.")
            return True
        else:
            print("The dog is too tired or hungry to play.")
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
        self.health = min(100, self.health + 2)
        return True

    def groom(self):
        # Grooming the dog increases cleanliness, slightly improves health, but reduces happiness (as many dogs do
        # not enjoy grooming)
        self._cleanliness = 100
        self.health = min(100, self.health + 1)
        self.happiness = max(0, self.happiness - 10)
        self.health = max(0, self.health - 4)
        return True

    def socialise(self):
        # Socializing increases social needs and happiness, but increases tiredness and hunger, and slightly reduces
        # health (due to potential overexcitement)
        if self.happiness >= 50:  # Only allow socializing if the dog is in a good mood
            self._social_need = 100
            self.happiness = min(100, self.happiness + 15)
            self.tiredness = min(100, self.tiredness + 20)
            self.hunger = min(100, self.hunger + 10)
            self.health = max(0, self.health - 2)
            print("You socialized the dog.")
            return True
        else:
            print("The dog is not in the mood to socialize.")
            self.happiness = max(0, self.happiness - 10)
            return False

    def print_status(self):
        life_stage = self.get_life_stage()
        print(f"Health: {self.health:.1f}, Hunger: {self.hunger:.1f}, Happiness: {self.happiness:.1f}, "
              f"Tiredness: {self.tiredness:.1f}, Age: {self.age:.1f}, Life stage: {life_stage}")
        
    def calculate_reward(self, action, next_state):
        # Define the base reward for different actions
        base_rewards = {
            'feed': 5,
            'walk': 4,
            'play': 8,
            'sleep': 6,
            'groom': 3,
            'socialise': 7,
            'flea treatment': -5,  # Negative reward for undergoing flea treatment
            'yes': 5,
            'no': -5
        }

        # Calculate additional rewards or penalties based on the dog's state
        additional_rewards = 0
        if self.hunger < 30:
            additional_rewards -= 10
        if self.happiness > 70:
            additional_rewards += 5
        if self.health > 70:
            additional_rewards += 3
        if self.tiredness < 30:
            additional_rewards -= 2
        # Add more conditions based on your simulation's dynamics


        # Add a penalty for feeding when not hungry
        if action == 'feed' and self.hunger < 30:
            additional_rewards -= 5  # Adjust the penalty value as needed

                # Calculate total reward
        total_reward = base_rewards.get(action, 0) + additional_rewards

        # Apply penalties for undesirable states or actions
        if self.state == 'vet_visit' and action != 'flea treatment':
            total_reward -= 10
        elif self.state == 'sudden_illness' and action != 'vet_visit':
            total_reward -= 15
        elif self.state == 'flea_event' and action != 'flea treatment':
            total_reward -= 20
        

        return total_reward
    
    def get_current_state(self):
        if self.state in ['vet_visit', 'sudden_illness', 'flea_event']:
            return self.state
        else:
            return 'normal'

    def reset_attributes(self):
        # Reset the dog's attributes
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.tiredness = 0
        self.age = 0
        self._cleanliness = 100
        self._social_need = 100
        self.flea_treatment_count = 0
        self.state = "normal"
        self.age_thresholds = {'puppy': 2, 'adult': 5, 'senior': 8}  # Age thresholds for different life stages

        # Hidden Attributes
        self.lifespan = random.uniform(17, 25)