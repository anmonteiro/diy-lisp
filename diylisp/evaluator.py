# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    math_operators = ["+", "-", "*", "/", "mod", ">", "<"]
    exprs = {
    	"quote" : lambda ast: ast[1],
    	"atom" : lambda ast: is_atom(evaluate(ast[1], env)),
    	"eq" : lambda ast: evaluate(["atom", ast[1]], env) \
    		and evaluate(["atom", ast[2]], env) \
    		and evaluate(ast[1], env) == evaluate(ast[2], env),
    	"if" : lambda ast: eval_if_statement(ast, env)
    }
    exprs.update(exprs.fromkeys(math_operators, lambda ast: eval_math_operators(ast, env)))

    if is_atom(ast):
    	return ast
    elif is_list(ast):
    	return exprs.get(ast[0], err_syntax)(ast)

def err_syntax(ast, second=None):
	raise LispError("Invalid syntax!")

def eval_math_operators(ast, env):
	exprs = {
		"+" : lambda a, b: evaluate(a, env) + evaluate(b, env),
		"-" : lambda a, b: evaluate(a, env) - evaluate(b, env),
		"*" : lambda a, b: evaluate(a, env) * evaluate(b, env),
		"/" : lambda a, b: evaluate(a, env) / evaluate(b, env),
		"mod" : lambda a, b: evaluate(a, env) % evaluate(b, env),
		">" : lambda a, b: evaluate(a, env) > evaluate(b, env)
	}
	arg1 = evaluate(ast[1], env)
	arg2 = evaluate(ast[2], env)

	if not(is_integer(arg1)) or not(is_integer(arg2)):
		raise LispError("Arithmetic operations only work on integers")
	return exprs.get(ast[0], err_syntax)(arg1, arg2)

def eval_if_statement(ast, env):
	if evaluate(ast[1], env) is True:
		return evaluate(ast[2], env)
	else:
		return evaluate(ast[3], env)





