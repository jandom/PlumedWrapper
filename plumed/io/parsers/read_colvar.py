
import pandas as pd
import numpy as np

def read_colvar(fn, verbose=False):
	if verbose: print(fn)
	with open(fn) as f:
		line = f.readline()
		assert line[:2] == '#!', 'Missing or incorrect header'
		columns = line.split()[2:]
	df = pd.read_csv(fn, sep=" ", comment="#", header=None)
	del df[0]
	df.columns = columns
	df.time = map(np.round, df.time)
	return df
