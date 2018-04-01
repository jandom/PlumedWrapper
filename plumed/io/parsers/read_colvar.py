
import pandas as pd
import numpy as np
import six

def read_colvar(fname, verbose=False):
	if verbose: print(fname)
	f = open(fname) if isinstance(fname, six.string_types) else fname
	with f:
		line = f.readline()
		assert line[:2] == '#!', 'Missing or incorrect header'
		columns = line.split()[2:]
	df = pd.read_csv(fname, sep=" ", comment="#", header=None)
	del df[0]
	df.columns = columns
	df.time = map(np.round, df.time)
	return df
