# relies on the decorated method's instance having an initialised _lock variable
def locking(process):
	def fn(self, *args, **kwargs):
		self._lock.acquire()
		try:
			ret = process(self, *args, **kwargs)
		finally:
			self._lock.release()
		return ret
	fn.__name__ = process.__name__
	return fn

class MultipleAssignmentError(RuntimeError):
	pass

