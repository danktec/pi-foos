import RPi.GPIO as GPIO
import time, sys

# Global Vars
goal_wait_timeout = 1
game_in_play = True
A_goals = 0
B_goals = 0
## Pin Config
reset_button_in   = 4
team_A_trigger_in = 27
team_A_light_out  = 22
team_B_trigger_in = 18
team_B_light_out  = 23

# GPIO Pin Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(reset_button_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(team_A_trigger_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(team_B_trigger_in, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(team_A_light_out, GPIO.OUT)
GPIO.setup(team_B_light_out, GPIO.OUT)

# Light an LED for 1 second
def light(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    return

# Register a goal for a team
def goal(team):
    global game_in_play
    global A_goals
    global B_goals

    if (team == "A"):
        A_goals += 1
        print("Team A has {} goals".format(A_goals))
    if (team == "B"):
        B_goals += 1
        print("Team B has {} goals".format(B_goals))

    if (A_goals == 5):
        print("Team A wins")
        reset_play()
        return
    if (B_goals == 5):
        print("Team B wins")
        reset_play()
        return
    return

# Reset game play mode
def reset_play():
    global game_in_play
    global B_goals
    global A_goals

    B_goals = 0
    A_goals = 0

    print("Current Game Was Reset")
    game_in_play = False

# Global Game Loop
while True:

    game_reset = GPIO.input(4)
    if (game_reset == False and game_in_play == False):
        time.sleep(1)
        game_in_play = True

    if (game_in_play == True):
        print("New Game Started...")

    while game_in_play:
        try:
            # Game Reset Button
            game_reset = GPIO.input(4)
            if (game_reset == False):
                reset_play()
                continue

            A_input_state = GPIO.input(27)
            B_input_state = GPIO.input(18)

            if (A_input_state == False):
                print("Team A Scored!")
                light(team_A_light_out)
                goal("A")
                time.sleep(goal_wait_timeout)

            if (B_input_state == False):
                print("Team B Scored!")
                light(team_B_light_out)
                goal("B")
                time.sleep(goal_wait_timeout)

	# Handle SIGINT
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Bye")
            sys.exit()
