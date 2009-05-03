import unittest
import logging
import sys
sys.path.append('..')
from dataflow import *

# logging.basicConfig(level=logging.DEBUG)

class DataflowTest(unittest.TestCase):
	def test_should_unify_a_simple_example(self):
		x, y, z = var(), var(), var()
		spawn(lambda: unify(y, x() + 2))
		spawn(lambda: unify(z, y() + 3))
		spawn(lambda: unify(x, 1))
		self.assertEqual(z(), 6)
		self.assertEqual(y(), 3)

	def test_should_create_dataflow_vars_for_function_input_arguments(self):
		@dataflow_vars
		def test_func(x, y, z):
			# notice how the order automatically gets resolved
			spawn(lambda: unify(y, x() + 2))
			spawn(lambda: unify(z, y() + 3))
			spawn(lambda: unify(x, 1))
			return z()
		self.assertEqual(test_func(), 6)

	def test_dataflow_vars_should_skip_any_provided_leading_arguments(self):
		class Foo(object):
			@dataflow_vars
			def doit(self, x, y, z):
				spawn(lambda: unify(y, x() + 2))
				spawn(lambda: unify(z, y() + 3))
				spawn(lambda: unify(x, 1))
				return z()
		self.assertEqual(Foo().doit(), 6)
	
	def test_should_not_allow_multiple_assignment(self):
		return # FIXME: broken for now; too fragile
		@dataflow_vars
		def assign_twice(y):
			spawn(lambda: unify(y, 1))
			spawn(lambda: unify(y, 2)) # expect this to fail
			return y()
		def run_and_wait():
			assign_twice()
			import time
			time.sleep()
		
		# the best we can do is raise a sigint on the main thread
		self.assertRaises(KeyboardInterrupt, run_and_wait)
	
	def test_spawn_should_pass_additional_args(self):
		f = var()
		def add_3(num):
			unify(f, num + 3)
		spawn(add_3, 1)
		self.assertEqual(f(), 4)
	
	def test_should_pass_through_attribute_accesses(self):
		f = var()
		class WithAttr(object):
			attr = 'the attr'
		spawn(lambda: unify(f, WithAttr()))
		self.assertEqual(f.attr, 'the attr')

	def test_should_pass_through_item_accesses(self):
		f = var()
		spawn(lambda: unify(f, {'a':1}))
		self.assertEqual(f['a'], 1)

