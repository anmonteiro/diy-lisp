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
    	"eq" : lambda ast: (evaluate(["atom", ast[1]], env) and
    		evaluate(["atom", ast[2]], env) and
    		evaluate(ast[1], env) == evaluate(ast[2], env)),
    	"if" : lambda ast: eval_if_statement(ast, env),
    	"define" : lambda ast: eval_define(ast, env),
    	"lambda" : lambda ast: eval_lambda(ast, env),
    	"cons" : lambda ast: eval_cons(ast, env),
    	"head" : lambda ast: eval_head(ast, env),
    	"tail" : lambda ast: eval_tail(ast, env),
    	"empty" : lambda ast: eval_empty(ast, env),
    	"env" : lambda ast: eval_in_env(ast, env)
    }
    exprs.update(exprs.fromkeys(math_operators,
    	lambda ast: eval_math_operators(ast, env)))
	
    if is_symbol(ast):
    	return env.lookup(ast)
    elif is_atom(ast):
    	return ast
    elif is_list(ast):
    	#if is_closure(ast[0]):
    	#	return eval_closure(ast, env)
    	#print ast
    	#print is_list(ast[0])
    	expr = ast[0] if not(is_list(ast[0])) else "env"

    	return exprs.get(expr, exprs["env"])(ast)


def err_syntax(ast, second = None):
	raise LispError("Invalid syntax!")


def validate_num_args(ast, expected_num_args):
	num_args = len(ast) - 1 # subtract the actual keyword
	if num_args != expected_num_args:
		raise LispError("Wrong number of arguments for %s: %d; expected %d" %
			(ast[0], num_args, expected_num_args))


def err_non_symbol(ast):
	raise LispError("Found non-symbol for first argument of '%s'" % ast[0])


def err_not_function(expr):
	raise LispError("%s is not a function" % unparse(expr))

def err_empty_list(ast):
	raise LispError("Unexpected empty list")


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
	if evaluate(ast[1], env):
		return evaluate(ast[2], env)
	else:
		return evaluate(ast[3], env)


def eval_define(ast, env):
	validate_num_args(ast, 2)
	if not(is_symbol(ast[1])):
		err_non_symbol(ast)

	new_binding = evaluate(ast[2], env)
	env.set(ast[1], new_binding)
	return new_binding


def eval_lambda(ast, env):
	# arguments should be type list
	validate_num_args(ast, 2)
	if not(is_list(ast[1])):
		err_syntax(ast)
	result = Closure(env, ast[1], ast[2])
	return result


def eval_closure(ast, env):
	closure, args = ast[0], ast[1:]
	body = closure.body
	params = closure.params

	validate_num_args(ast, len(params))

	# evaluate arguments before binding them to parameters
	args = [evaluate(arg, env) for arg in args]
	
	# bind arguments to parameters
	# for readability reasons, prefer 2 steps instead of:
	# args = dict(zip(params, [evaluate(arg, env) for arg in args]))
	args = dict(zip(params, args))

	closure_env = closure.env.extend(args)

	return evaluate(body, closure_env)


def eval_in_env(ast, env):
	args = ast[1:]
	expr = env.lookup(ast[0]) if is_symbol(ast[0]) else evaluate(ast[0], env)
	args[:0] = [expr]

	return eval_closure(args, env) if is_closure(expr) else err_not_function(expr)

# Operations with lists
def eval_cons(ast, env):
	result = evaluate(ast[2], env)
	result[:0] = [evaluate(ast[1], env)]

	return result

def eval_head(ast, env):
	result = evaluate(ast[1], env)
	print result
	return result[0] if len(result) > 0 else err_empty_list(ast)

def eval_tail(ast, env):
	result = evaluate(ast[1], env)
	print result
	return result[1:] if len(result) > 0 else err_empty_list(ast)

def eval_empty(ast, env):
	return len(evaluate(ast[1], env)) == 0

