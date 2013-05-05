def tuple_sum(*args):
	return tuple(sum(t) for t in zip(*args))

def tuple_invert(tup):
	return tuple(-1 * t for t in tup)