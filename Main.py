from Dog import Dog
# Import the RLAgent
from RLAgent import QLearningAgent


import time
def main():
    my_dog = Dog()
    last_time = time.time()

    # Create an instance of QLearningAgent
    rl_agent = QLearningAgent(state_space=["normal", "vet_visit", "sudden_illness", "flea_event"],
                              action_space=["feed", "walk", "play", "sleep", "groom", "socialise", "flea treatment", "yes", "no"], 
                            dog_instance=my_dog  # Pass the my_dog instance to the QLearningAgent constructor)
    )
    #my_dog = Dog(rl_agent=rl_agent)
    my_dog.rl_agent = rl_agent
    # Initial print of the dog's status before any updates
    my_dog.print_status()

    # Inside the while loop, replace user input with RL agent's action selection
    while True:
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time

        health_decay = 2.0  # Set a default health decay, you can adjust this based on your simulation

        # Use RL agent to select action
        action = rl_agent.select_action(my_dog.get_state())

        print(f"RL Agent selected action: {action}")

        # Check if the current state involves a decision
        decision_state = my_dog.handle_event()

        # If it does, update the RL agent's Q-values with the decision state
        if decision_state:
            next_state = my_dog.get_state()
            rl_agent.update_q_values(my_dog.get_state(), action, next_state)

        #action = input("What would you like to do? (feed, walk, play, sleep, groom, socialise, flea treatment, quit): ")
        if action == 'feed':
            my_dog.feed(health_decay)
        elif action == 'walk':
            my_dog.walk()
        elif action == 'play':
            my_dog.play()
        elif action == 'sleep':
            my_dog.sleep()
        elif action == 'groom':
            my_dog.groom()
        elif action == 'socialise':
            my_dog.socialise()
        elif action == 'flea treatment':
            my_dog.administer_flea_treatment()
        elif action == 'quit':
            break
        else:
            print("Invalid action. Please choose again.")

        # Print a new line for readability
        print("\n")

        my_dog.print_status()

        # Get the next state after the action
        next_state = my_dog.get_state()
        
        # Update Q-values based on the RL agent
        rl_agent.update_q_values(my_dog.get_state(), action, next_state)

        dog_status = my_dog.update_status(elapsed_time)

        # Print Q-values after each iteration
        rl_agent.print_q_values()

        if dog_status == 'old_age':
            print("Congratulations! Your dog lived a long and happy life.")
            break
        elif dog_status == 'neglect':
            print("Unfortunately, your dog has passed away due to neglect.")
            break

if __name__ == "__main__":
    main()
