from Dog import *
import time
def main():
    my_dog = Dog()
    last_time = time.time()

    # Initial print of the dog's status before any updates
    my_dog.print_status()

    while True:
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time

        action = input("What would you like to do? (feed, walk, play, sleep, groom, socialize, quit): ")
        if action == 'feed':
            my_dog.feed()
        elif action == 'walk':
            my_dog.walk()
        elif action == 'play':
            my_dog.play()
        elif action == 'sleep':
            my_dog.sleep()
        elif action == 'groom':
            my_dog.groom()
        elif action == 'socialize':
            my_dog.socialize()
        elif action == 'quit':
            break
        else:
            print("Invalid action. Please choose again.")

        my_dog.update_status(elapsed_time)  # Update the dog's status after the action
        my_dog.print_status()

if __name__ == "__main__":
    main()
