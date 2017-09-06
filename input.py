import RPi.GPIO as GPIO
import time, sys

# GPIO Pin Setup
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)


def light(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    return

# Global Vars
goal_wait_timeout = 1

game_in_play = True

A_goals = 0
B_goals = 0

## Pin Config
reset_button_in   = 1

team_A_trigger_in = 1
team_A_light_out  = 1
team_B_trigger_in = 1
team_B_light_out  = 1

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

def reset_play():
    global game_in_play
    global B_goals
    global A_goals

    B_goals = 0
    A_goals = 0

    print("game was reset")
    game_in_play = False

# Game Loop
while True:

    game_reset = GPIO.input(4)
    if (game_reset == False and game_in_play == False):
        time.sleep(1)
        game_in_play = True

    if (game_in_play == True):
        print("Game Started")

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
                print("Team A Scored")
                light(22)
                goal("A")
                time.sleep(goal_wait_timeout)

            if (B_input_state == False):
                print("Team B Scored")
                light(23)
                goal("B")
                time.sleep(goal_wait_timeout)

	# Handle SIGINT
        except KeyboardInterrupt:

            GPIO.cleanup()
            print("Bye")
            sys.exit()



