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

        action = input("What would you like to do? (feed, walk, play, sleep, groom, socialise, flea treatment, quit): ")
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
        elif action == 'socialise':
            my_dog.socialise()
        elif action == 'flea treatment':
            my_dog.administer_flea_treatment()
        elif action == 'quit':
            break
        else:
            print("Invalid action. Please choose again.")

        dog_status = my_dog.update_status(elapsed_time)
        my_dog.print_status()

        if dog_status == 'old_age':
            print("Congratulations! Your dog lived a long and happy life.")
            break
        elif dog_status == 'neglect':
            print("Unfortunately, your dog has passed away due to neglect.")
            break

if __name__ == "__main__":
    main()
