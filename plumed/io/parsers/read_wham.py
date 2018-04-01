
import pandas as pd

def read_wham(fname):
	df = pd.read_csv(fname, sep="\t", comment="#", header=None)
	columns = "Coor		Free	FreeErr		Prob		ProbErr".split()
	df.columns = columns
	return df
