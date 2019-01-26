#! usr/bin/env python3
# -*- coding: utf-8 -*-

# IMPORTS
import inquirer # https://pypi.org/project/inquirer/
import sys


# FUNCTION : delete the n last lines printed in the CLI
# n = number of lines to delete (int)
def delete_last_lines(n):
    for _ in range(n):
        sys.stdout.write('\x1b[1A')
        sys.stdout.write('\x1b[2K')


# FUNCTION : display a selection menu and get the result
# m = message (String)
# c = choices (Array)
# return the answer of the question as a dict(question: answer)
def selection_menu(m, c):
    question = [inquirer.List('choice',
                              message = m,
                              choices = c)
                ]

    answer = inquirer.prompt(question)

    return answer


# FUNCTION : display a type answer menu and get the result
# m = message (String)
# reg = regex to filter the result ('None' if it's not necessary)
# return the answer of the question as a dict(question: answer)
def type_answer_menu(m, reg):
    if (reg != 'None'):
        question = [inquirer.Text('answer',
                                  message = m,
                                  validate = lambda _,
                                  x: re.match(reg, x))
                    ]
    else:
        question = [inquirer.Text('answer',
                                  message = m)]

    answer = inquirer.prompt(question)

    return answer
