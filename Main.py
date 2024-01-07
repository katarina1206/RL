from Dog import Dog
from RLAgent import QLearningAgent
import time


from PyQt5.QtWidgets import QApplication
from Dog import Dog
from RLAgent import QLearningAgent
from GUI import VirtualPetGUI  # Importing the GUI from GUI.py
import sys


from PyQt5.QtWidgets import QApplication
from Dog import Dog
from RLAgent import QLearningAgent
from GUI import VirtualPetGUI  # Assuming the provided GUI code is saved in a file named VirtualPetGUI.py
import sys

def main():
    app = QApplication(sys.argv)

    my_dog = Dog()
    rl_agent = QLearningAgent(state_space=["normal", "vet_visit", "sudden_illness", "flea_event"],
                                  action_space=["feed", "walk", "play", "sleep", "groom", "socialise", "flea treatment", "yes", "no"],
                                  dog_instance=my_dog)

    # Setting the RL agent in the Dog instance
    my_dog.rl_agent = rl_agent

    alive_count = 0  # Counter for tracking how many times the dog stays alive


    gui = VirtualPetGUI(my_dog)  # Pass the Dog instance to the GUI

    for _ in range(50):
        
        gui.show()

        # Run the application
        app.exec_()
        #app.processEvents()

        if my_dog.get_life_stage() == 'old_age':
            alive_count += 1

        my_dog.reset_attributes()  # Reset dog's attributes

    print(f"The dog stayed alive {alive_count} times out of 50.")

if __name__ == "__main__":
    main()


# def main():
#     for _ in range(100):
#         my_dog = Dog()
#         last_time = time.time()

#         rl_agent = QLearningAgent(state_space=["normal", "vet_visit", "sudden_illness", "flea_event"],
#                                   action_space=["feed", "walk", "play", "sleep", "groom", "socialise", "flea treatment", "yes", "no"],
#                                   dog_instance=my_dog
#                                   )

#         my_dog.rl_agent = rl_agent
#         my_dog.print_status()

#         while True:
#             current_time = time.time()
#             elapsed_time = current_time - last_time
#             last_time = current_time

#             health_decay = 2.0

#             action = rl_agent.select_action(my_dog.get_state())

#             print(f"RL Agent selected action: {action}")

#             decision_state = my_dog.handle_event()

#             if decision_state:
#                 next_state = my_dog.get_state()
#                 rl_agent.update_q_values(my_dog.get_state(), action, next_state)

#             if action == 'feed':
#                 my_dog.feed(health_decay)
#             elif action == 'walk':
#                 my_dog.walk()
#             elif action == 'play':
#                 my_dog.play()
#             elif action == 'sleep':
#                 my_dog.sleep()
#             elif action == 'groom':
#                 my_dog.groom()
#             elif action == 'socialise':
#                 my_dog.socialise()
#             elif action == 'flea treatment':
#                 my_dog.administer_flea_treatment()
#             elif action == 'quit':
#                 break
#             else:
#                 print("Invalid action. Please choose again.")

#             print("\n")
#             my_dog.print_status()
#             next_state = my_dog.get_state()
#             rl_agent.update_q_values(my_dog.get_state(), action, next_state)

#             dog_status = my_dog.update_status(elapsed_time)
#             rl_agent.print_q_values()

#             if dog_status == 'old_age':
#                 print("Congratulations! Your dog lived a long and happy life.")
#                 break
#             elif dog_status == 'neglect':
#                 print("Unfortunately, your dog has passed away due to neglect.")
#                 break

# if __name__ == "__main__":
#     main()
