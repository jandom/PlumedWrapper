
import pandas as pd

def read_fes(fname):
	lines = [l[1:] for l in open(fname).readlines() if l.startswith("#")]
	columns = lines[1].split()
	data = [map(float, l.split()) for l in lines[2:]]
	df = pd.DataFrame(data, columns=columns)
	df.Window = map(int, df.Window)
	return df
