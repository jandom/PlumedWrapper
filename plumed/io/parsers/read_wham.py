
import pandas as pd

def read_wham(f):
	df = pd.read_csv(f, sep="\t", comment="#", header=None)
	columns = "Coor		Free	FreeErr		Prob		ProbErr".split()
	df.columns = columns
	return df
