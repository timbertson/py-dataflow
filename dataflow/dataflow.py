#!/usr/bin/env python
import threading
import inspect
import thread

__all__ = ['dataflow_vars', 'spawn']
from var import var

def dataflow_vars(func):
	argspec = inspect.getargspec(func)
	if any([x is not None for x in argspec[1:]]):
		raise ValueError(
			"dataflow_vars expects wrapped function "
			"to accept only named, non-defaulted arguments")
	args = argspec[0]

	def _call_with_args(*args_received):
		missing_args = args[len(args_received):]
		missing_arg_vars = map(var, missing_args)
		return func(*(list(args_received) + missing_arg_vars))
	return _call_with_args

def spawn(func, *args):
	thread_ = threading.Thread(target=func, args=args)
	thread_.start()
	return thread_

