#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# author: Quartoxuna <info@quartoxuna.de>
# summary: Simple Brainfuck interpreter
#

# IMPORTS
import sys

def show(stack,sp,program,pc,stdout,stdin):
	# Print our code along with the current position
	sys.stdout.write("\nCODE   : %s\n(%3d)%s\n"%(program,pc,((pc+4)*" ") + "^"))

	# Print contents of stack with current position
	sys.stdout.write("STACK  : ")
	sys.stdout.write(" ".join(["[%3d]" % _ for _ in stack]))
	sys.stdout.write("\n")
	stack_pos = ["     " for _ in xrange(len(stack))]
	stack_pos[sp] = "  ^  "
	sys.stdout.write("(%3d)  " % sp + 2*" " + " ".join(["%s" % _ for _ in stack_pos]))

	# STDOUT and STDIN
	sys.stdout.write("\nSTDOUT : '%s'\nSTDIN  : '%s'\n" % (stdout,stdin))
	raw_input("\n--- Press <RETURN> for next instruction ---")

def brainz(program,*args):
	stack = [0] # Our stack
	sp = 0 # Stack Pointer
	pc = 0 # Program Counter
	stdout = "" # STDOUT cache
	stdin = "" # STDIN cache

	# Remove invalid characters from program
	program = filter(lambda char: char in (">","<","+","-",".",",","[","]"), program)

	# Show initial state
	show(stack,sp,program,pc-1,stdout,stdin)

	while True:
		# Get next command
		current = program[pc]

		if current == ">":
			# Increment StackPointer
			# Append new element if needed
			sp += 1
			if sp >= len(stack):
				stack.append(0)
		elif current == "<":
			# Decrement StackPointer
			# Check for Memory Limit
			sp -= 1
			if sp < 0:
				raise MemoryError("Moved beyond Stack!")
		elif current == "+":
			# Increase current value
			stack[sp] += 1
		elif current == "-":
			# Decrease current value
			stack[sp] -= 1
		elif current == ".":
			# Print current value as ASCII to STDOUT
			stdout += chr(stack[sp])
			sys.stdout.write(stdout[-1])
		elif current == ",":
			# Read current valud from STDIN as ASCII
			stdin += ord((input())[0])
			stack[sp] = stdin[-1]
		elif current == "[":
			# Jump after closing ']' if current
			# value is zero
			if stack[sp] == 0:
				pc = program.find("]",pc)
		elif current == "]":
			# Jump back to starting '[' if
			# current value is not zero
			if stack[sp] != 0:
				pc = program.rfind("[",0,pc)

		# Show state
		show(stack,sp,program,pc,stdout,stdin)

		# Increase ProgramCounter
		pc += 1

		if pc >= len(program):
			# Check if we are at the end of the program
			break

if __name__ == "__main__":
	if len(sys.argv)<2:
		sys.stderr.write("Please enter Brainfuck code!\n")
		sys.exit(1)
	else:
		try:
			brainz(sys.argv[1])
		except KeyboardInterrupt:
			sys.stdout.write("\nBye!\n")
