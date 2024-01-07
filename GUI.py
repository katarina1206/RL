import time
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QProgressBar, QHBoxLayout, QTextEdit, QInputDialog
from PyQt5.QtGui import QPixmap, QImageReader, QPainter, QPalette, QBrush, QIcon, QFont
from PyQt5.QtCore import QTimer, Qt, QSize
from RLAgent import QLearningAgent
from Dog import Dog



class CustomProgressBar(QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.barLabel = ""

        self.setTextVisible (False)

        self.setStyleSheet("QProgressBar {"
                           "border: 1px white;"
                           "border-radius: 5px;"
                           "text-align: center;"
                           "}"
                           "QProgressBar::chunk {"
                           "background-color: #FCBC6A;"
                           "width: 20px;"  # Adjust the width here for horizontal bar
                           "}")


    def setBarLabel(self, text):
        self.barLabel = text
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        #font object set to bold 
        font = QFont()
        font.setBold(True)
        painter.setFont(font)

        painter.setPen(Qt.black)  # Set text color
        # Draw text in the center of the progress bar
        painter.drawText(self.rect(), Qt.AlignCenter, self.barLabel)


class VirtualPetGUI(QWidget):
    def __init__(self, dog):
        super().__init__()
        self.dog = dog  # Assign the dog object that was passed as an argument
        if self.dog:
            self.dog.gui_callback = self.display_message
        self.game_buttons = []
        self.initUI()
        self.last_time = time.time()

        # Initialize the RL agent
        self.rl_agent = QLearningAgent(
            state_space=["normal", "vet_visit", "sudden_illness", "flea_event"],
            action_space=["feed", "walk", "play", "sleep", "groom", "socialise", "flea treatment", "yes", "no"],
            dog_instance=self.dog
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(1000)  # Update every 1 second

    def initUI(self):
        self.setWindowTitle("Virtual Pet")

        #set window size
        self.resize (1200, 600) 

        # vertical main layout
        main_layout = QVBoxLayout(self)

        #layout for the life stage label and progress bars 
        life_stage_layout = QHBoxLayout()

        # Add a stretch to push progress bars to the center
        life_stage_layout.addStretch(1)

        #Layout for progress bars  (vertical)
        self.control_layout = QVBoxLayout()
        self.control_layout.setAlignment(Qt.AlignCenter)
        self.control_layout.setSpacing (5)
        self.control_layout.setContentsMargins(5, 5, 5, 5)

        # Add progress bars and buttons
        self.health_bar = self.createProgressBar("Health", self.control_layout)
        self.control_layout.addWidget (self.health_bar, alignment = Qt.AlignCenter)

        self.hunger_bar = self.createProgressBar("Hunger", self.control_layout)
        self.control_layout.addWidget (self.hunger_bar, alignment = Qt.AlignCenter)

        self.happiness_bar = self.createProgressBar("Happiness", self.control_layout)
        self.control_layout.addWidget (self.happiness_bar, alignment = Qt.AlignCenter)

        self.tiredness_bar = self.createProgressBar("Tiredness", self.control_layout)
        self.control_layout.addWidget (self.tiredness_bar, alignment = Qt.AlignCenter)
        
        #add progress bar layout to life stage 
        life_stage_layout.addLayout(self.control_layout)

        # Life stage and age labels layout (vertical)
        label_layout = QVBoxLayout()
        self.addLabels(label_layout)
        life_stage_layout.addLayout(label_layout)

        self.money_label = QLabel("Money: $0")
        self.formatLabel(self.money_label)
        life_stage_layout.addWidget(self.money_label)

        #add progreess bars to the main layout
        main_layout.addLayout(life_stage_layout)

        #spacer to push the image and buttons down
        main_layout.addStretch(3)

         # Horizontal layout for image and tricks
        image_tricks_layout = QHBoxLayout()

         # Image display area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        image_tricks_layout.addWidget(self.image_label)
       
        # Tricks display area
        # self.tricks_layout = QVBoxLayout()
        # self.tricks_label = QLabel("Tricks")
        # self.formatLabel(self.tricks_label)
        # self.tricks_layout.addWidget(self.tricks_label)

        # self.trick_labels = {}  # Store references to trick labels
        # for trick in self.dog.available_tricks:
        #     label = QLabel(f"{trick}: Not Learned")
        #     self.formatLabel(label)
        #     self.tricks_layout.addWidget(label)
        #     self.trick_labels[trick] = label 
        
        container_widget = QWidget()
        container_widget.setLayout(image_tricks_layout)
        main_layout.addWidget(container_widget)

        main_layout.addLayout(image_tricks_layout)

        #horisontal layout for buttons
        button_layout = QHBoxLayout()
        self.createActionButtons(button_layout)
        
         # Add a button for participating in a show
        # self.show_button = QPushButton("Participate in Show", self)
        # self.show_button.clicked.connect(self.dog.participate_in_show)
        # button_layout.addWidget(self.show_button)

        # # In your button setup section
        # teach_trick_button = QPushButton("Teach Trick", self)
        # teach_trick_button.clicked.connect(lambda: self.dog.teach_trick(self.get_trick_name))
        # button_layout.addWidget(teach_trick_button)

        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.close)
        quit_button.setFixedSize(100, 30)
        button_layout.addWidget(quit_button)

        #add button layout to the main layout 
        main_layout.addLayout(button_layout)

        # Load background image and GIF
        background_image = QPixmap("/Users/ambertong/Downloads/RL-GUI/Images/background-scene-with-tree-white-fence-garden_1639-2581.jpg.avif")
        scaled_background = background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
    
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(scaled_background))
        self.setPalette(palette)

        self.load_gifs()

        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        self.message_display.setFixedHeight(30)
        self.message_display.setStyleSheet(
            "QTextEdit {"
            "background: transparent;"
            "border: none;"  # Removes the border
            "color: black;"  # Text color
            "}"
        )

        #add to thr bottom of the main layout 
        main_layout.addWidget(self.message_display)

        # Timer for updating the GUI
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(1000)

    def display_message (self, message):
        formatted_message = f"<div style = 'text-align: center; font-size: 16pt; font-weight:bold; ' > {message} < /div >"
        self.message_display.clear()
        self.message_display.append (formatted_message)

    def get_trick_name(self):
        tricks = list(self.dog.available_tricks.keys())
        dialog = QInputDialog(self)
        dialog.setComboBoxItems(tricks)
        dialog.setWindowTitle("Teach Trick")
        dialog.setLabelText("Choose a trick to teach:")
        if dialog.exec_() == QInputDialog.Accepted:
            return dialog.textValue()
        return None

    def createProgressBar(self, label, layout):
        progress_bar = CustomProgressBar()
        progress_bar.setBarLabel(label)
        progress_bar.setMaximum(100)
        progress_bar.setFixedWidth(200)
        layout.addWidget(progress_bar)
        return progress_bar

    def addLabels(self, layout):
        # Life Stage Label
        self.life_stage_label = QLabel("Life Stage: Unknown")
        self.formatLabel(self.life_stage_label)
        layout.addWidget(self.life_stage_label)

        # Age Label
        self.age_label = QLabel("Age: 0")
        self.formatLabel(self.age_label)
        layout.addWidget(self.age_label)

    def formatLabel(self, label):
        font = label.font()
        font.setPointSize(15)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)

    def createActionButtons(self, layout):
        actions = [
            ("Feed", self.dog.feed, "/Users/ambertong/Downloads/RL-GUI/Images/meat-on-bone-removebg-preview.png", (50,50)),
            ("Walk", self.dog.walk, "/Users/ambertong/Downloads/RL-GUI/Images/walk-removebg-preview.png", (90, 90)),
            ("Play", self.dog.play, "/Users/ambertong/Downloads/RL-GUI/Images/tennis ball.png", (40, 40)),
            ("Sleep", self.dog.sleep, "/Users/ambertong/Downloads/RL-GUI/Images/sleep-removebg-preview.png", (90, 90)),
            ("Groom", self.dog.groom, "/Users/ambertong/Downloads/RL-GUI/Images/hairbrush-removebg-preview.png", (90, 90)),
            ("Socialise", self.dog.socialise, "/Users/ambertong/Downloads/RL-GUI/Images/socialise.png", (100, 100)),
            ("Flea Treatment", self.dog.administer_flea_treatment, "/Users/ambertong/Downloads/RL-GUI/Images/fleas-removebg-preview.png", (90, 90))
        ]
        for title, action, iconPath, iconSize in actions:
            button = self.createActionButton(title, action, layout, iconPath, iconSize)
            self.game_buttons.append(button) 
        

    def createActionButton(self, title, action, layout, iconPath, iconSize):
        button = QPushButton(self)
        icon = QIcon(iconPath)
        button.setIcon(icon)
        button.setIconSize (QSize (iconSize[0], iconSize[1]))

        button.clicked.connect(action)
        button.setFixedSize(50, 50)
        button.setStyleSheet("""
        QPushButton {
            border: none; 
            background-color: transparent;
        }
    """)
        layout.addWidget(button)

    def update_tricks_display(self):
        for trick, label in self.trick_labels.items():
            learned_status = self.dog.learned_tricks.get(trick, False)
            label.setText(f"{trick}: {'Learned' if learned_status else 'Not Learned'}")

    def load_gifs(self):
        reader = QImageReader("/Users/ambertong/Downloads/RL-GUI/Images/ezgif.com-effects.gif")
        self.gif_frames = []
        while reader.canRead():
            image = reader.read()
            scaled_image = image.scaled (QSize(150, 150), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.gif_frames.append(QPixmap.fromImage(scaled_image))
        self.frame_index = 0

        # Start the GIF animation
        self.start_gif_animation()

    def start_gif_animation(self):
        self.update_image()

    def update_gui(self):
        # Get the current time and calculate elapsed time since the last update
        current_time = time.time()
        #scaling_factor = 0.001  # Adjust this value to control the aging rate
        elapsed_time = (current_time - self.last_time) #* scaling_factor
        self.last_time = current_time

    # RL agent selects an action based on the dog's current state

        # RL agent selects an action based on the dog's current state
        action = self.rl_agent.select_action(self.dog.get_state())
        print(f"Rl agent {action}")

        # # Check if action is a tuple and extract the action part
        # if isinstance(action, tuple):
        #     action = action[1]
        # new_action = action

        decision_state = self.dog.handle_event()

        if decision_state:
            next_state = self.dog.get_state()
            self.rl_agent.update_q_values(self.dog.get_state(), action, next_state)

        # Define the health_decay here or adjust it as needed
        health_decay = 2.0

        # Perform the selected action and pass health_decay where appropriate
        if action == 'feed':
            self.dog.feed(health_decay)
        elif action == 'walk':
            self.dog.walk()
        elif action == 'play':
            self.dog.play()
        elif action == 'sleep':
            self.dog.sleep()
        elif action == 'groom':
            self.dog.groom()
        elif action == 'socialise':
            self.dog.socialise()
        elif action == 'flea treatment':
            self.dog.administer_flea_treatment()  
        else:   
            if action in ['yes', 'no']:
             #Handle 'yes' and 'no' actions separately, as they don't correspond to Dog methods
            #You can add the specific logic for these actions here
                pass
            elif hasattr(self.dog, action):
                getattr(self.dog, action)()  # Execute the action method on the dog
            else:
                print(f"Invalid action: {action}")  # Handle invalid action (e.g., log or ignore)

        self.dog.print_status()
        next_state = self.dog.get_state()
        self.rl_agent.update_q_values(self.dog.get_state(), action, next_state)

        dog_status = self.dog.update_status(elapsed_time)
        #self.rl_agent.print_q_values()


        # # Update the dog's status based on the elapsed time and the performed action
        # dog_status = self.dog.update_status(elapsed_time)

        # # Update RL agent's Q-values with the new state information
        # self.dog.print_status()
        # next_state = self.dog.get_state()
        # self.rl_agent.update_q_values(self.dog.get_current_state(), new_action, next_state)
        # self.rl_agent.print_q_values()

        # Update GUI elements to reflect the new status of the dog
        self.health_bar.setValue(int(self.dog.health))
        self.hunger_bar.setValue(int(self.dog.hunger))
        self.happiness_bar.setValue(int(self.dog.happiness))
        self.tiredness_bar.setValue(int(self.dog.tiredness))
        self.life_stage_label.setText(f"Life Stage: {self.dog.get_life_stage().capitalize()}")
        self.age_label.setText(f"Age: {self.dog.age:.1f}")

        # Update any additional GUI elements as needed

        # Check if the dog has reached a terminal state
        if dog_status == 'old_age':
            self.display_message("Congratulations! Your dog lived a long and happy life.")
            print("Congratulations! Your dog lived a long and happy life.")
            self.timer.stop()
            self.close() #Once the above message reaches, the game is over and it quits
        elif dog_status == 'neglect':
            self.display_message("Unfortunately, your dog has passed away due to neglect.")
            print("Unfortunately, your dog has passed away due to neglect.")
            self.timer.stop()
            self.close() #Once the above message reaches, the game is over and it quits

    def update_image(self):
        if self.gif_frames:
            self.image_label.setPixmap(self.gif_frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.gif_frames)
        QTimer.singleShot(100, self.update_image)
