from importlib import import_module
import GordleApp_0_9
from GordleApp_0_9 import gameBoard, letter_by_letter
import GordleApp_1_0
import emoji
import numpy as np
GreenSquare = emoji.emojize(':green_square:')#'#538d4e'
YellowSquare = emoji.emojize(':yellow_square:')#'#b59f3b'
GreySquare =  emoji.emojize(':black_large_square:')#'#3a3a3c'
EmptySquare = emoji.emojize(':white_large_square:')#'#121213'
Fail = emoji.emojize(':warning:')

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

def pattern_matching(guess,target):
  guess_list = word_to_array(guess)
  target_list = word_to_array(target)
  result_guess = result_list(guess)
  result_target = result_list(target)

  length_guess = len(guess_list)
  length_target = len(target_list)
  current_guess = ''
  current_target = ''
  full_pattern_matrix = [(guess_list,target_list,len(guess)),result_guess,result_target]
  matching_matrix = [guess_list,target_list,length_list(guess),length_list(target)]


  #Green if guess[i][letter] == target[i][letter]
  #greens
  for i in matching_matrix[2]:
    #for j in matching_matrix[3]:
      if matching_matrix[0][i] == matching_matrix[1][i]:
        full_pattern_matrix[1][i] = 2 
        full_pattern_matrix[2][i] = 2

  #yellows
  for i in matching_matrix[2]:
    current_guess = matching_matrix[0][i]
    for j in matching_matrix[3]:
      current_target = matching_matrix[1][j]
      if full_pattern_matrix[1][i] == 0 and full_pattern_matrix[2][j] ==0:
        if matching_matrix[0][i] == matching_matrix[1][j] and full_pattern_matrix[1][j] != 2 and full_pattern_matrix[1][i] == 0: #and full_pattern_matrix[1][i] != 2:
       #if guess_list[i] == target_list[j] and result_guess[]   
          #if full_pattern_matrix[1][matching_matrix[0].index(matching_matrix[0][i])] != 2:
            full_pattern_matrix[1][i] = 1
            full_pattern_matrix[2][j]  = 1
      

  return full_pattern_matrix
#MISS = np.uint8(0)
#MISPLACED = np.uint8(1)
#EXACT = np.uint8(2)
def pattern_to_string(pattern):#from 3b1b
    d = {0: "⬛", 1: "🟨", 2: "🟩"}
    return "".join(d[x] for x in pattern)


def test_pattern_matching():

  testCases ={
   0:{'GUESS':'ahead','TARGET':'aahed','RESULT':[2,1,1,1,2]}
  ,1:{'GUESS':'floor','TARGET':'thorn','RESULT':[0,0,2,0,1]}
  ,2:{'GUESS':'minis','TARGET':'inner','RESULT':[0,1,2,0,0]}
  ,3:{'GUESS':'train','TARGET':'track','RESULT':[2,2,2,0,0]}
  ,4:{'GUESS':'steam','TARGET':'meats','RESULT':[1,1,1,1,1]}
  ,5:{'GUESS':'lucid','TARGET':'vivid','RESULT':[0,0,0,2,2]}
  ,6:{'GUESS':'cuthu','TARGET':'futus','RESULT':[0,2,2,0,1]}
  ,7:{'GUESS':'solid','TARGET':'spill','RESULT':[2,0,1,1,0]}
  ,8:{'GUESS':'slimy','TARGET':'spill','RESULT':[2,1,2,0,0]}
  ,9:{'GUESS':'picks','TARGET':'spill','RESULT':[1,1,0,0,1]}
  ,10:{'GUESS':'spilt','TARGET':'spill','RESULT':[2,2,2,2,0]}
  ,11:{'GUESS':'match','TARGET':'chant','RESULT':[0,1,1,1,1]}
  ,12:{'GUESS':'chats','TARGET':'chant','RESULT':[2,2,2,1,0]}
  ,13:{'GUESS':'talks','TARGET':'chant','RESULT':[1,1,0,0,0]}
  ,14:{'GUESS':'petal','TARGET':'chant','RESULT':[0,0,1,1,0]}
  }
  
  print(f'Test case # DEMO: guess           vs. target')
  for i in range(len(testCases)):
    target = testCases[i]['TARGET']
    guess = testCases[i]['GUESS']
    correct_result = testCases[i]['RESULT']
  
    attempt = GordleApp_1_0.answer_check(guess,target)
    
    if attempt[1]==correct_result:
      #print(f'Test case {i:02d} PASS: {pattern_to_string(attempt[1])} vs. {pattern_to_string(correct_result)}')
      print(f'Test case {i:02d} PASS: {pattern_to_string(attempt)} vs. {pattern_to_string(correct_result)}')
    else:
      #print(f'Test case {i:02d} FAIL:  {pattern_to_string(attempt[1])} vs. {pattern_to_string(correct_result)}')
      print(f'Test case {i:02d} PASS: {pattern_to_string(attempt)} vs. {pattern_to_string(correct_result)}')
    print(f'_________________: {guess}           vs. {target}',end="\n\n")

#test_pattern_matching()
all_guesses = ['ahead','floor','cuthu','solid','match','slimy','petal']

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
  print(first_row)
  #second row to indicate matches and missmatches
  for letter in range(97, 123):
    if chr(letter) in matched_letters_set:
      second_row = ' '.join((second_row,'🟩'))
    elif chr(letter) in missmatched_letters_set:
      second_row = ' '.join((second_row,'🟨'))
    else:
      second_row = ' '.join((second_row,'⬛'))
  print(second_row)
#keyboard(all_guesses)
#answer = 'spill'
#guesses = ['solid','slimy','picks']
#results = [[2,0,1,1,0],[2,1,2,0,0],[1,1,0,0,1]]
#keyboard(guesses,results,answer)

from datetime import date, datetime, timedelta

today = date.today()
todays_wordle = 255

if date.today() != today:
  diff = timedelta()
  diff = date.today() - today
  print(diff.days)
  todays_wordle += diff.days
print(todays_wordle)

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