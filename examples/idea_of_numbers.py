# _*_ coding: utf_8 _*_
"""
Created on 3/17/2017

@author: Tozier

This problem evolves a program (using the full Push instruction set) to fit the
symbolic regression problem `9x^2-11x + 1964`. But it is given no numeric
constants at all to work with, and has to "MacGuyver" a mechanism to build
large-enough constants to fit the training cases.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instructions import all_instructions
from pyshgp.gp.variation import (UniformMutation, Alternation,
                                 VariationOperatorPipeline)
from pyshgp.gp.evolvers import SimplePushGPEvolver


def target_function(x):
    return 9 * x**2 - 11 * x + 1964


def error_func(program):
    errors = []
    for x in range(10):
        # Create the push interpreter and run program
        interpreter = PushInterpreter()
        y_hat = interpreter.run(program, inputs=[x], output_types=['_integer'])[0]
        # Get output
        if y_hat is not None:
            # compare to target output
            target_int = target_function(x)
            # calculate error
            errors.append((y_hat - target_int)**2)
        else:
            errors.append(1e5)
    return errors


# Genetic operators
mut = UniformMutation()
alt = Alternation()
ops = [
    (Alternation(), 0.6),
    (UniformMutation(), 0.2),
    (VariationOperatorPipeline((alt, mut)), 0.2)
]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              selection_method='epsilon_lexicase',
                              atom_generators=list(all_instructions))
    evo.fit(error_func, 1, ['_integer'])
