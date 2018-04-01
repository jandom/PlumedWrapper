
import pandas as pd

def read_fes(fname):
	lines = open(fname).readlines()
	columns = lines[0].split()[2:]
	data = [map(float, l.split()) for l in lines if not l.startswith("#")]
	df = pd.DataFrame(data, columns=columns)
	return df
