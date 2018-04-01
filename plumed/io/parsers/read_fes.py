
import pandas as pd

def read_fes(f="fes.dat"):
	lines = open(f).readlines()
	columns = lines[0].split()[2:]
	data = [map(float, l.split()) for l in lines if not l.startswith("#")]
	df = pd.DataFrame(data, columns=columns)
	return df
