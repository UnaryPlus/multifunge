#!/usr/bin/env python3

import copy
import sys
import getch

class Pointer:
  printing = False
  waiting = False

  def __init__(self, row, column, value, direction, intMode):
    self.row = row
    self.column = column
    self.value = value
    self.direction = direction
    self.intMode = intMode

  def move(self):
    if self.waiting: return
    if self.direction == 'up': self.row -= 1
    if self.direction == 'down': self.row += 1
    if self.direction == 'left': self.column -= 1
    if self.direction == 'right': self.column += 1

  def horizontal(self):
    return self.direction in ['left', 'right']

def toMatrix(file):
  # Split file into 2d list of characters
  program = [[char for char in line] for line in file.split('\n')]

  # Calculate max line length
  lengths = [len(line) for line in program]
  lengths.sort()
  maxLength = lengths[-1]

  # Make all lines the same length by adding spaces to the end
  newProgram = []
  for line in program:
    while len(line) < maxLength:
      line.append(' ')
    newProgram.append(line)
  return newProgram

def createPointers(program):
  # Add pointer every time the '@' character appears and return list of pointers
  pointers = []
  for row, line in enumerate(program):
    for column, command in enumerate(line):
      if command == '@':
        pointers.append(Pointer(row, column, 0, 'right', True))
  return pointers

def step(program, pointers):
  newPointers = []
  for pointer in pointers:
    # Copy pointer and call it 'p' so that 'pointers' doesn't change mid-loop
    p = copy.copy(pointer)
    p.move()

    # Delete pointer if it is outside of file
    if p.row < 0 or p.row >= len(program) or p.column < 0 or p.column >= len(program[p.row]):
      continue

    c = program[p.row][p.column]
    bracketed = program[p.row][p.column - 1] == '[' and program[p.row][p.column + 1] == ']'

    # Set this to true to delete pointer
    deleted = False

    # If the pointer is in print mode, print the character unless it is a quote
    if p.printing:
      if c == '"': p.printing = False
      else: print(c, end = '')

    # If the pointer is waiting, search for other waiting pointers and do the operation
    elif p.waiting:
      for ptr in pointers:
        # Continue searching if the other pointer isn't on the same space
        if ptr.row != p.row or ptr.column != p.column or ptr.horizontal() == p.horizontal(): continue

        # If the pointer is horizontal, execute the command
        if p.horizontal():
          p.waiting = False
          if c == '+': p.value += ptr.value
          elif c == '-': p.value -= ptr.value
          elif c == '*': p.value *= ptr.value
          elif c == '/': p.value //= ptr.value
          elif c == '%': p.value %= ptr.value
          elif c == '^': p.value **= ptr.value
          elif c == '&': p.value = 1 if p.value and ptr.value != 0 else 0
          elif c == '|': p.value = 1 if p.value or ptr.value != 0 else 0
          elif c == '<': p.value = 1 if p.value < ptr.value else 0
          elif c == '>': p.value = 1 if p.value > ptr.value else 0
          elif c == '=': p.value = 1 if p.value == ptr.value else 0
          elif c == '?' and ptr.value != 0: p.direction = ptr.direction

        # If the pointer is vertical it gets deleted
        else: deleted = True
        break

    # If the command is bracketed, wait for other pointer
    elif bracketed: p.waiting = True

    # Otherwise, execute the command
    elif c == 'x': deleted = True
    elif c == ';': return []
    elif c == '^': p.direction = 'up'
    elif c == 'v': p.direction = 'down'
    elif c == '<': p.direction = 'left'
    elif c == '>': p.direction = 'right'
    elif c == '*':
      directions = ['up', 'down'] if p.horizontal() else ['left', 'right']
      newPointers.append(Pointer(p.row, p.column, p.value, directions[0], p.intMode))
      newPointers.append(Pointer(p.row, p.column, p.value, directions[1], p.intMode))
    elif c == '/':
      direction = {
        'up' : 'right',
        'right' : 'up',
        'down' : 'left',
        'left' : 'down'
      } [p.direction]
      newPointers.append(Pointer(p.row, p.column, p.value, direction, p.intMode))
    elif c == '\\':
      direction = {
        'up' : 'left',
        'left' : 'up',
        'down' : 'right',
        'right' : 'down'
      } [p.direction]
      newPointers.append(Pointer(p.row, p.column, p.value, direction, p.intMode))
    elif c == '+': p.value += 1
    elif c == '-': p.value -= 1
    elif c == '~': p.value *= -1
    elif c == 'i': p.intMode = True
    elif c == 'c': p.intMode = False
    elif c == '?':
      if p.intMode: p.value = int(input())
      else: p.value = ord(getch.getche())
    elif c == '!':
      if p.intMode: print(p.value, end = '')
      else: print(chr(p.value), end = '')
    elif c == '"': p.printing = True
    elif c == '.': print()
    elif c == '#': p.value = 0
    elif c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
      p.value = p.value * 10 + int(c)

    # Append pointer to new list of pointers if it hasn't been deleted
    if not deleted: newPointers.append(p)
  return newPointers

def run(file):
  program = toMatrix(file)
  pointers = createPointers(program)
  while len(pointers) > 0:
    pointers = step(program, pointers)

def main():
  if len(sys.argv) == 2:
    with open(sys.argv[1], 'r') as file:
      run(file.read())

  else:
    print('incorrect number of arguments')
    print('example: ' + sys.argv[0] + ' program.mfg')

if __name__ == '__main__': main()
