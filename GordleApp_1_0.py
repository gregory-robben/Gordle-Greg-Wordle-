"""
Gordle is a python clone of the popular 'Wordle' game, now owned by the NYT. 
Rules of the game:
    Guess the WORDLE in 6 tries.

    Each guess must be a valid 5 letter word. Hit the enter button to submit.

    After each guess, the color of the tiles will change to show how close your guess was to the word.

    Green = Correct letter and location, Yellow = Correct letter wrong location, Grey = Letter not in word

Package requirements: PyDictionary

TODO: figure out how to print the board and print over it each time.
      - Could fill in the game board dictionary and reprint each time
      - Could not print the whole thing and just print as you go.
TODO: inset debugging print statements EVERYWHERE and a global variable to turn it on
"""

import random
import GordleDictionary
import sys
import time

GreySquare = "⬛"
YellowSquare = "🟨"
GreenSquare = "🟩"
EmptySquare = "⬜"

debugging = False

def gameDifficulty():
  if debugging: print('gameDifficulty function called')
  print("Choose your desired difficulty: Beginner (5 letters) | Intermediate (9 letters | Expert (13 letters)")
  valid = False
  while valid != True:
    choice = input().capitalize()
    #TODO: rework this where the difficulty and the length is a dictionary so that its simpler
    if choice == 'Beginner':
      valid = True
      if debugging: print('Difficulty set to Beginner, length of 5')
      return 5
      
    elif choice == 'Intermediate':
      valid = True
      if debugging: print('Difficulty set to Intermediate, length of 9')
      return 9
      
    elif choice == 'Expert':
      valid = True
      if debugging: print('Difficulty set to Expert, length of 13')
      return 13
      
    if choice == 'End':
      if debugging: print('User chose End. Program will exit')
      sys.exit
    else:
      print("Please enter a valid choice, or write 'End' to terminate the game")

def userID():
    '''
    userID Function will check the current user, and open an existing user or make a new uesr
    parameter 1: ipAddress - optional
    parameter 2: emailAddress
    '''
    #TODO: 'create user database and streak tracking'
    #TODO: userID debugging


#define target word
def set_target(difficulty = 5):
    '''
    set_target chooses a word of specified dificulty length from GordleDictionary.py at random
    Parameter: difficulty (default is 5)
    Returns: targetWord
    '''
    GameDictionary = GordleDictionary.allowed_word_list()

    targetWord = GameDictionary[random.randint(0,len(GameDictionary))]

    return targetWord

#create target_dictionary 0-5 for each letter
def Set_target_dictionary(targetWord):
    '''
    Set_target_dictionary builds the target word dictionary to use when checking a guess
    Parameter: the target word
    Returns: a dictionary with each letter and a matched flag
    '''
    target_dictionary = {}
    position = 0
    for letter in targetWord:
        target_dictionary[position]['LETTER'] = letter
        target_dictionary[position]['MATCHED'] = 0
        position += 1
    
    return target_dictionary

#ask the user to guess a 5 letter word
def user_guess(difficulty = 5):
    '''
    Prompts the user for their guess and ensures that it meets the difficulty criteria
    Parameter 1: difficulty setting
    Returns: guess as string
    '''
    while True:
        guess = input("Guess a " + str(difficulty) + " letter word: ").lower()
        if len(guess) != difficulty:
            print('Invalid length',end="\r")
            time.sleep(1)
            continue
        if not GordleDictionary.word_in_list(guess,GordleDictionary.allowed_word_list()):
            print('Invalid word',end='\r')
            time.sleep(1)
            continue
        else:
            break
    
    return guess

def set_guess_dictionary(guess):
    '''
    sets up the guess dictionary to relay the reults back to the user
    returns: a set up guess dictionary letter : color
    '''

    guess_dictionary = {}
    i = 0
    while i < 5:
      guess_dictionary[i]['LETTER'] = guess[i]
      guess_dictionary[i]['COLOR'] = EmptySquare
      i += 1
    return guess_dictionary


def correct_word(guess,targetWord):
    '''
    Is the guess the target word?
    Return True if valid or False if invalid
    ''' 
    if guess == targetWord:
        return True
    else:
        return False


#define letter-lookup function
#then going letter by letter, if letter is in target_dictionary then if the position matches return GreenSquare, else return YellowSquare. If not return EmptySquare


def word_to_array(word):
  list = []
  
  for letters in word:
    list.append(letters)
    
  return list

def blank_list(string):
  result = []
  #TODO: learn how to us numpy zeros for this
  for i in range(len(string)):
    result.append(0)
  return result

def length_list(word):
  result = []
  for i in range(len(word)):
    result.append(i)
  return result

def answer_check(guess,target):
  '''
  Input: the guess and answer
  Returns: list of 0s, 1s, and 2s based on the accuracy of the guess
          [2,1,0,0,0]
  '''
  guess_list = word_to_array(guess)
  target_list = word_to_array(target)
  result_guess = blank_list(guess)
  result_target = blank_list(target)

  full_pattern_matrix = [(guess_list,target_list,len(guess)),result_guess,result_target]
  matching_matrix = [guess_list,target_list,length_list(guess),length_list(target)]


  #Green if guess[i][letter] == target[i][letter]
  for i in matching_matrix[2]:

      if matching_matrix[0][i] == matching_matrix[1][i]:
        full_pattern_matrix[1][i] = 2 
        full_pattern_matrix[2][i] = 2

  #yellow if guess[i] is in answer but is not the same position and hasn't been checked yet
  for i in matching_matrix[2]: #loop through the letters in the guess
    for j in matching_matrix[3]: #for each letter in the guess loop through the answer's letters to check against them
      if full_pattern_matrix[1][i] == 0 and full_pattern_matrix[2][j] ==0: #if true the guess and target locations are unmatched
        if matching_matrix[0][i] == matching_matrix[1][j]: #the guess letter matches a target letter
          if full_pattern_matrix[1][i] == 0: #the guess letter hasn't been matched yet for either green or yellow
            full_pattern_matrix[1][i] = 1 #mark the result_guess at this position as matched
            full_pattern_matrix[2][j]  = 1 #mark the result_target at the corresponding position as matched
  return full_pattern_matrix[1]

def gameBoard(difficulty = 5):
  '''
  Sets up the game board for the player
  returns a blank board
  '''

  theBoard = {}
  for row in range(difficulty + 2):
    theBoard[row] = {0:''}
    for column in range(difficulty):
      theBoard[row][column]= EmptySquare
  return theBoard

def guess_result_to_color_string(result_list):#from 3b1b
  '''
  Parameters: a list of the guess results
  Returns: a string of colored squares ⬜⬛🟨🟩
  '''
  d = {0: "⬛", 1: "🟨", 2: "🟩"}
  #return d[result_list]
  return "".join(d[x] for x in result_list)

##############################################
#3b1b's
def all_results_to_color_string(results):
  return "\n".join(map(guess_result_to_color_string, results))

##############################################


  ##############################################
   # Print outcome #from 3b1b
  
  #if not quiet:
  #    message = "\n".join([
  #        "",
  #        f"Answer: {answer}",
  #        f"Guesses: {guess}",
  #        *patterns_to_string((*patterns, 3**5 - 1)).split("\n"),
  #        *" " * (6 - len(patterns)),
  #        f"Total guesses: {total_guesses}",
  #        *" " * 2,
  #    ])
  #    if answer is not test_set[0]:
  #        # Move cursor back up to the top of the message
  #        n = len(message.split("\n")) + 1
  #        print(("\033[F\033[K") * n)
  #    else:
  #        print("\r\033[K\n")
  #    print(message)

  ############################################
def print_result(guess,targetWord,round):
  #print("\033[K")
  print(f'Round {round+1}: ',end='')
  print(guess_result_to_color_string(answer_check(guess,targetWord)),end='')
  print(guess) 


if __name__ == "__main__":
  print("Gordle - Greg wordle")
  #printGameBoard(gameBoard(),None,None)
  UserID = userID()
  chosenDifficulty = 5 #gameDifficulty()
  #if chosenDifficulty > 5:
    #system(clear())
    #print("Gordle - Greg wordle")
    #printGameBoard(gameBoard(chosenDifficulty),None,None)
  round = 0
  all_guesses=[]
  results = []
  solved = False
  targetWord = set_target(chosenDifficulty)
  #targetWord = 'aahed'
  while round < chosenDifficulty + 1:
    guess = user_guess(chosenDifficulty)
    #guess = 'media'
    #past_guesses.append(guess)
    results.append(answer_check(guess,targetWord))
    all_guesses.append(guess)

    if min(results[-1]) ==2: #correct_word(guess,targetWord):
      
      
      #print_result2(round,results)
      print_result(guess,targetWord,round)
      #TODO: print the result as a full board with the rounds printed over top
      #printGameBoard(letter_by_letter(guess,targetWord),round)
      
      print('Well done!')
      solved = True
      break
    else:
      #print_result2(round,results)
      print_result(guess,targetWord,round)
      #printGameBoard(letter_by_letter(guess,targetWord),round)
    round += 1
  if not solved:
    print("Answer:",targetWord)



