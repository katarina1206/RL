from Dog import *
import time
def main():
    my_dog = Dog()

    # Initial print of the dog's status before any updates
    my_dog.print_status()

    while True:

        action = input("What would you like to do? (feed, walk, play, sleep, groom, socialise, flea treatment, "
                       "teach trick, participate in show, quit): ")
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
        elif action == 'teach trick':
            my_dog.teach_trick()
        elif action == 'participate in show':
            my_dog.participate_in_show()
        elif action == 'quit':
            break
        else:
            print("Invalid action. Please choose again.")

        dog_status = my_dog.update_status()
        my_dog.print_status()

        if dog_status == 'old_age':
            print("Congratulations! Your dog lived a long and happy life.")
            break
        elif dog_status == 'neglect':
            print("Unfortunately, your dog has passed away due to neglect.")
            break

if __name__ == "__main__":
    main()
