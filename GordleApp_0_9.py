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
"""
#from PyDictionary import PyDictionary
#import json
#import sqlite3
#from ssl import Options
import random
#from turtle import clear
import GordleDictionary
#import emoji
#from os import system
import sys
import time
#from turtle import position
#import psycopg2
#from psycopg2 import Error
#from psycopg2 import extras



#Define the hex keys for the letters
#GreenSquare = emoji.emojize(':green_square:')#'#538d4e'
#YellowSquare = emoji.emojize(':yellow_square:')#'#b59f3b'
#GreySquare =  emoji.emojize(':black_large_square:')#'#3a3a3c'
#EmptySquare = emoji.emojize(':white_large_square:')#'#121213'
GreySquare = "⬛"
YellowSquare = "🟨"
GreenSquare = "🟩"
EmptySquare = "⬜"

def gameDifficulty():
  print("Choose your desired difficulty: Beginner (5 letters) | Intermediate (9 letters | Expert (13 letters)")
  valid = False
  while valid != True:
    choice = input().capitalize()
    if choice == 'Beginner':
      valid = True
      return 5
      
    elif choice == 'Intermediate':
      valid = True
      return 9
      
    elif choice == 'Expert':
      valid = True
      return 13
      
    if choice == 'End':
      sys.exit
    else:
      print("Please enter a valid choice, or write 'End' to terminate the game")


  #define word length limit
  Beginner_Difficulty = 5
  Intermediate_Difficulty = 9 #we should see what the next most frequent length is
  Expert_Difficulty = 13

def userID():
    '''
    userID Function will check the current user, and open an existing user or make a new uesr
    parameter 1: ipAddress - optional
    parameter 2: emailAddress
    '''
    #TODO: 'create user database and streak tracking'


#define target word
#choose 5 letter word from dictionary at random
def set_target(difficulty = 5):
    '''
    set_target chooses a word of specified dificulty length from the GordleDictionary at random
    Parameter: difficulty
    Returns: targetWord
    '''
    GameDictionary = GordleDictionary.allowed_word_list()
    targetWord = GameDictionary[random.randint(0,len(GameDictionary))]
    #targetWord = "apple"
    #print("Target:",targetWord)
    return targetWord

#create target_dictionary 0-5 for each letter
def Set_target_dictionary(targetWord):
    '''
    Set_target_dictionary builds the target word dictionary to use when checking a guess
    Parameter: the target word
    Returns: a dictionary with each letter and a matched flag
    '''
    target_dictionary={0:{'LETTER':"",'MATCHED':0},
                       1:{'LETTER':"",'MATCHED':0},
                       2:{'LETTER':"",'MATCHED':0},
                       3:{'LETTER':"",'MATCHED':0},
                       4:{'LETTER':"",'MATCHED':0}}
    position = 0
    for letter in targetWord:
        target_dictionary[position]['LETTER'] = letter
        position += 1
    #print("Target dict:",target_dictionary) 
    return target_dictionary

#ask the user to guess a 5 letter word
def user_guess(difficulty = 5):
    '''
    Asks the user for their guess and ensures that it meets the difficulty criteria
    Returns the user's guess
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
        elif len(guess) == difficulty:
            break
    
    return guess

def set_guess_dictionary(guess):
    '''
    sets up the guess dictionary to relay the reults back to the user
    returns: a set up guess dictionary letter : color
    '''
    '''
    guess_dictionary = {0:{'LETTER':'','COLOR':'#538d4e'},
                        1:{'LETTER':'','COLOR':'#538d4e'},
                        2:{'LETTER':'','COLOR':'#538d4e'},
                        3:{'LETTER':'','COLOR':'#538d4e'},
                        4:{'LETTER':'','COLOR':'#538d4e'}}
    '''

    guess_dictionary = {0:{'LETTER':'','COLOR':EmptySquare}
                       ,1:{'LETTER':'','COLOR':EmptySquare}
                       ,2:{'LETTER':'','COLOR':EmptySquare}
                       ,3:{'LETTER':'','COLOR':EmptySquare}
                       ,4:{'LETTER':'','COLOR':EmptySquare}
                        }
    i = 0
    while i < 5:
      guess_dictionary[i]['LETTER'] = guess[i]
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
def letter_by_letter(guess,targetWord):
  '''
  Checks the guess against the target word letter by letter. Marking its progress as it goes, and providing the colors for feedback.
  Returns: a filled in guess dictionary with feedback (letter : color)
  '''
  guess_dictionary = set_guess_dictionary(guess)
  target_dictionary = Set_target_dictionary(targetWord)
  position = 0
  while position < len(targetWord):
    #guessletter = guess[position]
    for letters in guess:#targetWord:
      
      #if target_dictionary[position]['MATCHED'] == 0:
        #for i in range(len(targetWord)):

        #x = guessletter.find(target_dictionary[i]['LETTER'])
        x = targetWord.find(letters,position) #location of guessed letter in target
        if x >= 0 and x < position: #if the location is less than where we are in checking the target, look ahead of current position
          x = targetWord.find(letters)
        if x < 0:
          x = targetWord.find(letters)  

        if x == position: #the guessed letter and target have the same locations        
          target_dictionary[x]['MATCHED'] = 1
          guess_dictionary[position]['COLOR'] = GreenSquare
          position +=1
          continue
        if x >= 0 and x != position: #the guessed is misplaced          
#BUG: figure out how to deal with target = aahed and guess = ahead. The second a isn't turning yellow
          
          if target_dictionary[x]['MATCHED'] == 1: #if this position has already been matched don't double count the guess
            guess_dictionary[position]['COLOR'] = GreySquare
          else: #if this target position hasn't been matched then the guess is misplaced
            target_dictionary[x]['MATCHED'] = 1
            guess_dictionary[position]['COLOR'] = YellowSquare
          position +=1
          continue
        if x < 0: #the guessed letter does not exist
          guess_dictionary[position]['COLOR'] = GreySquare
          position +=1
          continue
        #else:
          guess_dictionary[position]['COLOR'] = GreySquare
          position +=1
          continue
      #elif target_dictionary[position]['MATCHED'] == 1:
        #guess_dictionary[position]['COLOR'] = GreySquare
        #position +=1
        #continue
  return guess_dictionary

def word_to_array(word):
  list = []
  
  for letters in word:
    list.append(letters)
    
  return list

def result_list(guess):
  result = []
  for i in range(len(guess)):
    result.append(0)
  return result

def length_list(word):
  result = []
  for i in range(len(guess)):
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
  result_guess = result_list(guess)
  result_target = result_list(target)

  full_pattern_matrix = [(guess_list,target_list,len(guess)),result_guess,result_target]
  matching_matrix = [guess_list,target_list,length_list(guess),length_list(target)]


  #Green if guess[i][letter] == target[i][letter]
  #greens
  for i in matching_matrix[2]:

      if matching_matrix[0][i] == matching_matrix[1][i]:
        full_pattern_matrix[1][i] = 2 
        full_pattern_matrix[2][i] = 2

  #yellows
  for i in matching_matrix[2]:

    for j in matching_matrix[3]:

      if full_pattern_matrix[1][i] == 0 and full_pattern_matrix[2][j] ==0:
        if matching_matrix[0][i] == matching_matrix[1][j] and full_pattern_matrix[1][j] != 2 and full_pattern_matrix[1][i] == 0: #and full_pattern_matrix[1][i] != 2:
            full_pattern_matrix[1][i] = 1
            full_pattern_matrix[2][j]  = 1
      

  return full_pattern_matrix[1]
def gameBoard(difficulty = 5):
  '''
  Sets up the game board for the player
  returns a blank board
  board example = 
  {
     0: {0:'',1:'',2:'',3:'',4:''}
    ,1: {0:'',1:'',2:'',3:'',4:''}
    ,2: {0:'',1:'',2:'',3:'',4:''}
    ,3: {0:'',1:'',2:'',3:'',4:''}
    ,4: {0:'',1:'',2:'',3:'',4:''}
    ,5: {0:'',1:'',2:'',3:'',4:''}
  }
  '''
  if difficulty == 5:
    tryLimit = 6
  elif difficulty == 9:
    tryLimit = 11
  elif difficulty == 13:
    tryLimit = 15
  else:
    tryLimit = 6

  theBoard = {}
  for row in range(tryLimit):
    theBoard[row] = {0:''}
    for column in range(difficulty):
      theBoard[row][column]= EmptySquare
  return theBoard
##############################################
#def pattern_to_int_list(pattern): #from 3b1b
#    result = []
#    curr = pattern
#    for x in range(5):
#        result.append(curr % 3)
#       curr = curr // 3
#    return result
##############################################
##############################################
def guess_result_to_color_string(result_list):#from 3b1b
  '''
  Parameters: a list of the guess results
  Returns: a string of colored squares ⬜⬛🟨🟩
  '''
  d = {0: "⬛", 1: "🟨", 2: "🟩"}
  #return d[result_list]
  return "".join(d[x] for x in result_list)
##############################################
def all_results_to_color_string(results):
  printout = ""
  #for x in results:
  #  printout += "\n".join(guess_result_to_color_string(x))
  #return printout
  return "\n".join(map(guess_result_to_color_string, results))
##############################################
def printGameBoard(guess,answer,result = None,total_guesses = None,quiet = False):
  '''
  Prints the result of the user's guess against the targetWord. If it is the first round, it also prints a blank board.
  Returns nothing

  '''
  board = gameBoard()

  if total_guesses == None:
    for row in range(len(board)):
      for column in range(len(board[row])):
        item = board.get(row,{}).get(column)
        print(item,end=' ')
      print()
  else:
    for column in range(len(board[total_guesses])):
      board[total_guesses][column] = result[column]['COLOR']
      item = board.get(total_guesses,{}).get(column)
      print(item, end=' ')
    print()


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

def print_result1(guess,targetWord,round):
  #print(f'Round {round+1}: ',end='')
  #print(pattern_matching(guess,targetWord))
      full_message = "\n".join([
          "",
          f"Answer: {targetWord}",
          f"Guesses: {guess}",
          *answer_check(guess,targetWord),
          #*" " * (6 - len(patterns)),
          f"Total guesses: {round}",
          *" " * 2,
      ])
      
          # Move cursor back up to the top of the message
      #n = len(full_message.split("\n")) + 1
      print(("\033[F\033[K") * 2)

      print(full_message)

def print_result2(round,results):

      full_message = "\n".join([
          "",
          #*pattern_matching(guess,targetWord).split("\n"),
          *all_results_to_color_string(*results).split("\n"),
          #*" " * (6 - round),
          f"Total guesses: {round}",
          *" ",
      ])
      
      # Move cursor back up to the top of the message
      n = len(full_message.split("\n"))
      print("\r\033[K\n" * n)

      print(full_message)

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



