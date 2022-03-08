"""
Gordle is a python clone of the popular 'Wordle' game, now owned by the NYT. 
Rules of the base game:
    Guess the GORDLE in 6 tries.

    Each guess must be a valid 5 letter word. Hit the enter button to submit.

    After each guess, the color of the tiles will change to show how close your guess was to the word.

    Green = Correct letter and location, Yellow = Correct letter wrong location, Grey = Letter not in word

In Gordle the user can choose harder modes which make the Gordle longer. The number of tries goes up accordingly

TODO: figure out how to print the board and print over it each time.
      - Could fill in the game board dictionary and reprint each time
      - Could not print the whole thing and just print as you go.
#TODO: Proper logging
"""

import random
import GordleDictionary
import time
from datetime import date
#import logging 
from datetime import date, datetime, timedelta


GreySquare = "⬛"
YellowSquare = "🟨"
GreenSquare = "🟩"
EmptySquare = "⬜"



def gameDifficulty():
  print("Choose your desired difficulty: Beginner (5 letters) | Intermediate (9 letters | Expert (13 letters)")
  valid = False
  while valid != True:
    choice = input().capitalize()
    #TODO: rework this where the difficulty and the length is a dictionary so that its simpler
    if choice == 'Beginner':
      valid = True
      return 5,choice
      
    elif choice == 'Intermediate':
      valid = True
      return 9,choice
      
    elif choice == 'Expert':
      valid = True
     
      return 13,choice
      
    if choice == 'End':
      valid = True
      exit()
    

def userID():
    '''
    userID Function will check the current user, and open an existing user or make a new uesr
    parameter 1: ipAddress - optional
    parameter 2: emailAddress
    '''
    #TODO: 'create user database and streak tracking'
    pass

def set_target(difficulty = 5):
    '''
    set_target chooses a word of specified dificulty length from GordleDictionary.py at random
    Parameter: difficulty (default is 5)
    Returns: targetWord
    '''
    GameDictionary = GordleDictionary.allowed_word_list()
    targetWord = GameDictionary[random.randint(0,len(GameDictionary))]
    return targetWord

#TODO: combine these and return both the word and the dictionary?
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

def user_guess(difficulty = 5):
    '''
    Prompts the user for their guess and ensures that it meets the difficulty criteria
    Parameter 1: difficulty setting
    Returns: guess as string
    '''
    while True:
        guess = input("Guess a " + str(difficulty) + " letter word: ").lower()
        if guess == 'end':
          exit()
        if len(guess) != difficulty:
            print("\033[1A\033[K\033[1A")
            print('Invalid length',end="\r")
            time.sleep(1)
            continue
        if not GordleDictionary.word_in_list(guess,GordleDictionary.allowed_word_list()):
            print("\033[1A\033[K\033[1A")
            print('Not in word list',end='\r')
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

def word_to_array(word):
  list = []
  
  for letters in word:
    list.append(letters)
    
  return list

def blank_list(string):
  '''
  Returns a blank list with length of the passed string
  '''
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
  Returns: list of 0s, 1s, and 2s based on the accuracy of the guess ex. [2,1,0,0,0]
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

def guess_result_to_color_string(result_list):
  '''
  Parameters: a list of the guess results
  Returns: a string of colored squares ⬜⬛🟨🟩
  Adapted from code from 3b1b
  '''
  d = {0: "⬛", 1: "🟨", 2: "🟩"}
  
  return "".join(d[x] for x in result_list)+'         '


def all_results_to_color_string(results):
  '''
  Parameter: list of number representing the guess accuracy
  Returns a string of colored squares
  Copied from 3b1b
  '''
  return "\n".join(map(guess_result_to_color_string, results))


def print_result(guess,answer,round,guesses,results,gameMode,difficulty):
  seperated_guess_string = '' #we seperate each letter so that they align with the result sqaures
  for letter in guess:
    seperated_guess_string += letter + ' '
  
  statement = "\n".join([
    "Gordle - Greg Wordle",
    f"Game mode: {gameMode} | Difficulty: {difficulty}",
    "",
    *all_results_to_color_string(results[:]).split("\n"),
    *" " * (6 - len(results)),
    *" " * 2,
    f"Round {round+1}: {guess_result_to_color_string(answer_check(guess,answer))}",
    f"         {seperated_guess_string}",
    f"Your guesses: {guesses}",
  ])
  
  # Move cursor back up to the top
  n = len(statement.split("\n")) + 3
  print(("\033[F\033[K") * (n))
            
  print(statement)

def keyboard(guesses,results,answer):
  used_letters = set("".join(all_guesses))
  matched_letters = []
  missmatched_letters = []
  first_row = ''
  second_row = ''

  for x in range(len(guesses)):
      guess = guesses[x]
      result = results[x]

      for i in range(len(guess)):
        if result[i] == 2:
          matched_letters.append(guess[i])
        if result[i] == 1:
          missmatched_letters.append(guess[i])
  matched_letters_set = set(matched_letters)
  missmatched_letters_set = set(missmatched_letters)
  #firt row with blanked out used letters except those in the answer
  for letter in range(97, 123):
    if (chr(letter) not in used_letters) or (chr(letter) in answer):
      first_row = '  '.join((first_row,chr(letter)))
    else:
      first_row = ' '.join((first_row,'⬛'))

  #second row to indicate matches and missmatches
  for letter in range(97, 123):
    if chr(letter) in matched_letters_set:
      second_row = ' '.join((second_row,'🟩'))
    elif chr(letter) in missmatched_letters_set:
      second_row = ' '.join((second_row,'🟨'))
    else:
      second_row = ' '.join((second_row,'⬛'))
  print(f'\n{first_row}\n{second_row}')

def todays_wordle(chosenDifficulty = 5,difficulty="Beginner"):
  while True:
    play_today = input("Play today's Wordle? (Yes/No/End): ").capitalize()
    if play_today == "End":
      exit()
    elif play_today == 'Yes':
      print("\033[0A\033[KPlaying today's Wordle")
      start_date = date(2022,3,1)
      todays_wordle = 255

      if date.today() != start_date:
        diff = timedelta()
        diff = date.today() - start_date
        todays_wordle += diff.days
      play_today = "Wordle"
      #return GordleDictionary.dictionary[0][todays_wordle],play_today
      return GordleDictionary.dictionary[todays_wordle],play_today
    elif play_today == 'No':
      print(f"\033[0A\033[KPlaying random {difficulty.lower()} Wordle")
      play_today = "Random"

      return set_target(chosenDifficulty),play_today


if __name__ == "__main__":
  print("Gordle - Greg wordle")
  #UserID = userID()
  chosenDifficulty,game_difficulty = 5,"Beginner"#gameDifficulty()
  round = 0
  all_guesses=[] #list object to store all of the users guesses
  results = [] #list object to store the results of the rounds, this helps up when reprinting the game board each time.
  solved = False
  targetWord, gameMode = todays_wordle(chosenDifficulty,game_difficulty) 
  
  while round < chosenDifficulty + 1:
    keyboard(all_guesses,results,targetWord)
    guess = user_guess(chosenDifficulty)
    print("\r\033[1A\033[K\r\033[1A\033[K\r\033[1A\033[K\r\033[1A\033[K")
    
    results.append(answer_check(guess,targetWord))
    all_guesses.append(guess)

    if min(results[-1]) ==2: #if all values in the latest result are 2 then that means all have exact matches and the game is over
      print_result(guess,targetWord,round,all_guesses,results,gameMode,game_difficulty)
      #TODO: print the result as a full board with the rounds printed over top
      if round == 0:
        print('Genious!')
      elif round == 1:
        print('Awesome!')
      elif round == 2:
        print('Well done!')
      elif round == 3:
        print('Great!')
      elif round == 4:
        print('You got it!')
      elif round == 5:
        print('Phew!')
      
      solved = True
      break
    else:
      print_result(guess,targetWord,round,all_guesses,results,gameMode,game_difficulty)
    round += 1

  if not solved:
    print(f"The answer was {targetWord}")



