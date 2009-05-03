dataflow.py
===========

dataflow.py is a port of larrytheliquid's ruby dataflow gem, mostly to
see if a python version (without blocks) would be useable. Turns out
it is, which is not what I'd initially expected. Having created it,
I'm interested in seeing how it can be applied to concurrency problems
as well as actor-like constructs.

dataflow functions:

 - **dataflow_vars**: decorator for generating dataflow variables for a function
 - **spawn**\(callable, \*args): start a thread using the given callable, plus any additional arguments
 - **var**\(name=None): create a new dataflow variable (with optional name)
 - **unify**\(var, value): set the value of a dataflow variable.

dataflow can provide arguments automatically::

	@dataflow_vars
	def sum_items(x, y, z):
		# notice how the order automatically gets resolved
		spawn(lambda: unify(y, x() + 2))
		spawn(lambda: unify(z, y() + 3))
		spawn(lambda: unify(x, 1))
		return z() # => 6


or you can create them whenever you like::

	f = var()
	spawn(lambda: unify(f, 'f'))
	f() # => 6


Accessing any attribute or item (dictionary key) of a dataflow
variable automatically waits for it to be assigned, and passes
that access onto its value::

	f = var()
	spawn(lambda: unify(f, {'key': 'val'})
	f['key'] # => 'val'