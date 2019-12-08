## Mastermind programmed by Kevin Cole. November 2019. First program in python!
# Version 1.1 into December 2019
    #added data collection on game outcomes.

from random import randint
import pickle
import pandas as pd

#In the instance of a new directory picke file should be generated


## Defines games allowable color types
color_list = ["red", "blue", "green", "yellow", "orange", "purple"]


def set_difficulty(game_dataframe):
    ## Sets how many guesses the user has. Returns 8, 10, or 14 based on user input
    ## Want - gamesize control for different size solutions
    print("Type easy, medium, or hard to selcect difficulty.")
    difficulty = input("Difficulty: ")
    if difficulty == "easy":
        guesses_left = 14
        game_dataframe['difficulty'] = 'easy'
    elif difficulty == "medium":
        game_dataframe['difficulty'] = 'medium'
        guesses_left = 10
    elif difficulty == "hard":
        guesses_left = 8
        game_dataframe['difficulty'] = 'hard'
    else:
        print("Input not recognized. Difficulty set to medium")
        guesses_left = 10
        game_dataframe['difficulty'] = 'medium'
    return guesses_left, game_dataframe


def generate_solution():
    ## Generates a random length 4 set of colors
    solution = []
    for i in range(4):
        color_index = randint(0,5)
        solution.append(color_list[color_index])  
    return solution


def user_guess():
    ## Takes user input guess of colors in order. #I can do this calling the string I defined before right?
    print ("Type four colors: red, blue, green, yellow, orange, purple; in order to submit your guess.")
    user_guess = []
    num_guesses = 0
    valid_guess = True
    while num_guesses < 4:
        guess = input("Guess color: ").split()
        for items in guess:
            if items in color_list:
                user_guess.append(items)
                num_guesses += 1
            else:
                user_guess.append(items)
                valid_guess = False
                num_guesses +=1
            if valid_guess == False:
                return user_guess, valid_guess
    if num_guesses > 4:
        valid_guess = False
    return user_guess, valid_guess

def answer_check(guess, solution, feedback_board):
    ## Checks the user guess against the solution and gives user feedback
    key = [0,0,0,0]
    correct = 0
    semi_correct = 0
    guess_copy = guess.copy()
    solution_copy = solution.copy()

    for i in range(4):
        ## Checks for correct color in the correct spot
        if guess[i] == solution[i]:
            current_guess = guess[i]
            key[i] = 1
            correct += 1
            guess_copy.remove(str(current_guess))
            solution_copy.remove(str(current_guess))
        
    ## Checks for correct color in other spots
    for j in range(4):
        if guess[j] in solution_copy and guess[j] in guess_copy:         
            semi_correct += 1
            guess_copy.remove(guess[j])
            solution_copy.remove(guess[j])               

    feedback_board.append([correct, semi_correct])
    print('Guess Results:')
    print("You have " + str(correct) + " perfect and " + str(semi_correct) + " colors in the wrong spot." )                             

    if key == [1, 1, 1, 1]:
        return 1
    else:
        return 0


def start_new_game(): #is this silly to define as a function? 2 lines of code essentially and never repeaded in a game instance. 
    ## Starts a data frame that will be appended to the master game log. 
    #maybe print title code here for organization
    
    ## Title code - style question, can i code this art? realistically fixed with a GUI dataframe?
    print(' ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('% ')
    print('%      Welcome to Mastermind! ')
    print('%           ')
    print('%  ')
    print('%')
    print('%      Guess colors to discover the secret key.')
    print('%')
    print('%')
    print('%                                                      by    Kevin Cole ')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(' ')
    
    player = input('What is your name? ')
    new_game = {'player': [player] , 'difficulty': ['none'], 'result'  : ['none'], 'turns':[0], 'complete':[False]}
    current_game = pd.DataFrame(new_game)
    
    return current_game

###
###
###
### Game Operation
###

## Initializing
win_condition = 0
game_board = []
feedback_board = []
turns = 0

## Load Game Log for data analysis #Test if this can be one line not two
pickle_in = open('Game_Log.pickle','rb')
game_log = pickle.load(pickle_in)

## Starting a new game's dataframe and printing Title code
game_dataframe = start_new_game()

## Generating solution key
solution = generate_solution()

## Setting difficulty sets number of guessess allowed. Future plans to disallow repeating colors in easy mode
guesses_left, game_dataframe = set_difficulty(game_dataframe)

## Game loop
while win_condition == 0:
    
    ## Game Board - better way to do the game board?
    print("--------------------------------------------------------------------")
    print("Game Board: Turn number: " + str(turns+1) + "  Guesses remaining: " + str(guesses_left))
    for line_index in range(turns):
        print(*game_board[line_index],feedback_board[line_index])
    print("--------------------------------------------------------------------")
    print(' ')
    
    #Get a valid user guess
    actual_guess, valid_guess = user_guess()
    while valid_guess == False:
        print(' ')
        print(' ')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('')
        print('')
        print('Colors only. Please try again.')
        print('')
        print('')
        print("Type the colors red, blue, green, yellow, orange, purple to submit your guess.")
        print('')
        print("Game Board: Turn number: " + str(turns+1) + "  Guesses remaining: " + str(guesses_left))
        ## Question: is this easier in a dataframe?
        for line_index in range(turns):
            print(*game_board[line_index],feedback_board[line_index])
        print("-------------------------------------------------")
        print(' ')
        actual_guess, valid_guess = user_guess()
    turns += 1
    #this probably can be done as one step and replace turns
    game_dataframe['turns'] = turns
    print(" ")

    ##debug tool. Prints solution after each round of guesses. 
    #print("solution is:")
    #print(solution)
    #print(" ")

    ## Updating the game board
    string_prep = []
    for element in actual_guess:
        string_prep.append(element.ljust(7))
    game_board.append(string_prep)

    
    win_check = answer_check(actual_guess, solution, feedback_board)
    if win_check == 1:
        game_dataframe['result'] = 'win'
        game_dataframe['complete'] = True
        print(" ")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$") 
        print("$$                                                            $$")
        print("$$                      $$    WINNER   $$                     $$")
        print('$$                                                            $$')
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")      
        print("$$                                                            $$")      
        print("$$                    You are the master mind                 $$")
        print('$$                                                            $$')
        print('$$                    Victory in' , turns , 'turns') #This is going to bother you. Fix right $$ 
        print('$$                                                            $$')      
        print("$$                                                            $$")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #pickle out
        game_log = game_log.append(game_dataframe)
        pickle_out = open('Game_Log.pickle','wb')
        pickle.dump(game_log,pickle_out)
        pickle_out.close()
        break
    guesses_left -= 1
    print("")
    print ("Guesses Remaining: " + str(guesses_left))
    if guesses_left == 0:
        game_dataframe['result'] = 'loss'
        game_dataframe['complete'] = True
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print('X')
        print('X           Game Over. You are out of guesses.')
        print('X')
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print('')
        print("The solution was:")
        print(*solution)
        game_log = game_log.append(game_dataframe, ignore_index = True)
        pickle_out = open('Game_Log.pickle','wb')
        pickle.dump(game_log,pickle_out)
        pickle_out.close()
        break
    else:
        print("Guess again!")
        print(" ")
        
