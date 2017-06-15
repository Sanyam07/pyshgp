# -*- coding: utf-8 -*-
"""
Created on July 24, 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from ... import constants as c
from ... import exceptions as e

from .. import instruction as instr

from . import registered_instructions as ri

def print_newline(state):
    """Appends a newline to the stdout string in the output field.
    """
    if not 'stdout' in state['_output'].keys():
        state['_output']['stdout'] = ''
    if len(state['_output']['stdout'])+1 > c.max_string_length:
        return
    state['_output']['stdout'] += '\n'
print_newline_instruction = instr.PyshInstruction('_print_newline',
                                                  print_newline,
                                                  stack_types = ['_print'])
ri.register_instruction(print_newline_instruction)

def printer(pysh_type):
    """Returns a function that takes a state and prints the top item of the
    appropriate stack of the state.
    """
    def prnt(state):
        if len(state[pysh_type]) < 1:
            return
        top_thing = state[pysh_type].ref(0)
        top_thing_str = str(top_thing)
        if not 'stdout' in state['_output'].keys():
            # stdout is not an output yet, create it.
            state['_output']['stdout'] = ''
        if len(state['_output']['stdout'])+len(top_thing_str) > c.max_string_length:
            return
        state[pysh_type].pop()
        state['_output']['stdout'] += top_thing_str
    instruction = instr.PyshInstruction('_print' + pysh_type, prnt,
                                        stack_types = ['_print', pysh_type])
    if pysh_type == '_exec':
        instruction.parentheses = 1
    return instruction
ri.register_instruction(printer('_exec'))
#<instr_open>
#<instr_name>print_exec
#<instr_desc>Prints the top item of the exec stack to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_integer'))
#<instr_open>
#<instr_name>print_integer
#<instr_desc>Prints the top integer to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_float'))
#<instr_open>
#<instr_name>print_float
#<instr_desc>Prints the top float to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_code'))
#<instr_open>
#<instr_name>print_code
#<instr_desc>Prints the top item on the code code stack to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_boolean'))
#<instr_open>
#<instr_name>print_boolean
#<instr_desc>Prints the top boolean to the string on the output stack.
#<instr_close>
ri.register_instruction(printer('_string'))
#<instr_open>
#<instr_name>print_string
#<instr_desc>Prints the top string to the string on the output stack.
#<instr_close>