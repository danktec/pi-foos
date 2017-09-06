import RPi.GPIO as GPIO
import time, sys

# Global Vars
goal_wait_timeout = 0.3 # set this below 1 for testing, 3 for real play
game_in_play = True
A_goals = 0
B_goals = 0
round_1_winners = ""
round_2_winners = ""
round_3_winners = ""
rounds = 3
round = 1

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
    time.sleep(goal_wait_timeout)
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
        end_round("A")
    if (B_goals == 5):
        print("Team B wins")
        end_round("B")

def end_round(winners):

    global round
    global B_goals
    global A_goals

    global round_1_winners
    global round_2_winners
    global round_3_winners

    A_goals = 0     
    B_goals = 0

    # Enforce rounds?
    if (1 == 1):

        if (round == 1):
            round_1_winners = winners
        if (round == 2):
            round_2_winners = winners
        if (round == 3):
            round_3_winners = winners

        # Account for all scenarios
        if (round_1_winners == "A" and round_2_winners == "A"):
            print("GAME WON by Team A!")
            reset_game()
            return
        if (round_1_winners == "B" and round_2_winners == "B"):
            print("GAME WON by Team B!")
            reset_game()
            return
        if (round_1_winners == "A" and round_3_winners == "A"):
            print("GAME WON by Team A!")
            reset_game()
            return
        if (round_1_winners == "B" and round_3_winners == "B"):
            print("GAME WON by Team B!")
            reset_game()
            return
        if (round_2_winners == "B" and round_3_winners == "B"):
            print("GAME WON by Team B!")
            reset_game()
            return
        if (round_2_winners == "A" and round_3_winners == "A"):
            print("GAME WON by Team A!")
            reset_game()        
            return

        #print("Winners::")
        #print(winners)
        #print(round)

        print("Round won by {}".format(winners))
        round += 1
    else:
         print("round limit reached")
         reset_game()

# Reset the game
def reset_game():
    global round
    global round_1_winners
    global round_2_winners
    global round_3_winners
    global game_in_play
    global B_goals
    global A_goals

    B_goals = 0
    A_goals = 0

    print("Current Game Was Reset")
    round = 1
    round_1_winners = ""
    round_2_winners = ""
    round_3_winners = ""
    game_in_play = False
    

# Global Game Loop
while True:
    #print("global Loop")
    #print(game_in_play)

    game_reset = GPIO.input(reset_button_in)
    if (game_reset == False and game_in_play == False):
        time.sleep(1)
        game_in_play = True

    if (game_in_play == True):
        print("New Game Started...")

    while game_in_play:
        try:

            # Game Reset Button
            game_reset = GPIO.input(reset_button_in)
            if (game_reset == False):
                reset_game()
                continue

            A_input_state = GPIO.input(team_A_trigger_in)
            B_input_state = GPIO.input(team_B_trigger_in)

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