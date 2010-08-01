import threading
from thread import interrupt_main
from lib import locking, MultipleAssignmentError

import logging
log = logging.getLogger(__name__)

__all__ = ['var','unify']

def _debug(s):
	log.debug("<%r>: %s" % (threading.currentThread(), s))

def unify(var, val):
	try:
		var._var_unify(val)
	except MultipleAssignmentError:
		interrupt_main()
		raise

class var(object):
	_value = None
	_bound = False
	def __init__(self, name=None):
		self._name = name
		self._lock = threading.Lock()
		self._condition = threading.Condition()
	
	def _wait(self):
		"switch from waiting on _lock to waiting on _condition; wait(); and then back again"
		self._lock.release()
		self._condition.acquire()
		self._condition.wait()
		self._lock.acquire()
		self._condition.release()
	
	def _notify_all(self):
		_debug("%r notifying all waiters" % (self,))
		self._condition.acquire()
		self._condition.notifyAll()
		self._condition.release()

	@locking
	def _var_unify(self, val):
		_debug("%r unifying to %r" % (self, val))
		if self._bound:
			raise MultipleAssignmentError("%s has already assigned to %r" % (self, self._value))
		self._value = val
		self._bound = True
		self._notify_all()

	@locking
	def __call__(self):
		if not self._bound:
			_debug("%r waiting" % (self))
			self._wait()
		return self._value
	
	def __getattr__(self, attr):
		return getattr(self(), attr)
	
	def __getitem__(self, attr):
		return self()[attr]
	
	def __repr__(self):
		return str(self)

	def __str__(self):
		return "<dataflow var %s>" % (self._name,)

