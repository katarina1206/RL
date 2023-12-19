from Dog import *
import time
def main():
    my_dog = Dog()
    last_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - last_time
        last_time = current_time

        my_dog.update_status(elapsed_time)
        my_dog.print_status()

        action = input("What would you like to do? (feed, walk, play, sleep, quit): ")
        if action == 'feed':
            my_dog.feed()
        elif action == 'walk':
            my_dog.walk()
        elif action == 'play':
            my_dog.play()
        elif action == 'sleep':
            my_dog.sleep()
        elif action == 'quit':
            break
        else:
            print("Invalid action. Please choose again.")

        my_dog.print_status()

if __name__ == "__main__":
    main()
