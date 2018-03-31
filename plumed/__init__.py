
import pandas as pd
import numpy as np

"""#! FIELDS drms ext.bias der_drms
#! SET min_drms 0.0
#! SET max_drms 2.0
#! SET nbins_drms  256
#! SET periodic_drms false"""

def get_umbrellas(files):
    return sorted([ float([l for l in  open(f).readlines() if "AT=" in l and "RESTRAINT" in l][-1].split("AT=")[-1].split()[0]) for f in files])

def to_grid(df, output="bias.dat"):
	name = df.columns[0]
	with open(output, "w") as f:
		f.write("#! FIELDS {} ext.bias der_{}\n".format(name, name))
		f.write("#! SET min_{} {}\n#! SET max_{} {}\n".format(name, df[name].min(), name, df[name].max()))
		f.write("#! SET nbins_name  {}\n#! SET periodic_{} false\n".format(name, len(df), name))
		for arg in df.values:
			f.write("{} {} {}\n".format(*arg))

def read_wham(f):
	df = pd.read_csv(f, sep="\t", comment="#",header=None)
	columns = "Coor		Free	FreeErr		Prob		ProbErr".split()
	df.columns = columns
	return df

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

def read_hills(f="HILLS"):
	lines = open(f).readlines()
	columns = lines[0].split()[2:]
	data = [map(float, l.split()) for l in lines if not l.startswith("#")]
	df = pd.DataFrame(data, columns=columns)
	return df

def read_fes(f="fes.dat"):
	lines = open(f).readlines()
	columns = lines[0].split()[2:]
	data = [map(float, l.split()) for l in lines if not l.startswith("#")]
	df = pd.DataFrame(data, columns=columns)
	return df

def read_plumeds(filenames):
    import natsort
    return [ read_plumed(f) for f in natsort.natsorted(filenames)]

def read_plumed(f):
    def foo(token): return float(token.split("=")[-1])
    line = [l for l in open(f).readlines() if "RESTRAINT" in l][-1]
    tokens = line.split()

    center = [token for token in tokens if token.startswith("AT")][-1]
    weight = [token for token in tokens if token.startswith("KAPPA")][-1]

    center, weight = foo(center), foo(weight)

    ind = int(f.split(".")[-2])
    return ind, center, weight

def read_str(filename):

    columns = ['_Gen_dist_constraint.ID',
 '_Gen_dist_constraint.Member_ID',
 '_Gen_dist_constraint.Member_logic_code',
 '_Gen_dist_constraint.Assembly_atom_ID_1',
 '_Gen_dist_constraint.Entity_assembly_ID_1',
 '_Gen_dist_constraint.Entity_ID_1',
 '_Gen_dist_constraint.Comp_index_ID_1',
 '_Gen_dist_constraint.Seq_ID_1',
 '_Gen_dist_constraint.Comp_ID_1',
 '_Gen_dist_constraint.Atom_ID_1',
 '_Gen_dist_constraint.Atom_type_1',
 '_Gen_dist_constraint.Atom_isotope_number_1',
 '_Gen_dist_constraint.Resonance_ID_1',
 '_Gen_dist_constraint.Assembly_atom_ID_2',
 '_Gen_dist_constraint.Entity_assembly_ID_2',
 '_Gen_dist_constraint.Entity_ID_2',
 '_Gen_dist_constraint.Comp_index_ID_2',
 '_Gen_dist_constraint.Seq_ID_2',
 '_Gen_dist_constraint.Comp_ID_2',
 '_Gen_dist_constraint.Atom_ID_2',
 '_Gen_dist_constraint.Atom_type_2',
 '_Gen_dist_constraint.Atom_isotope_number_2',
 '_Gen_dist_constraint.Resonance_ID_2',
 '_Gen_dist_constraint.Intensity_val',
 '_Gen_dist_constraint.Intensity_lower_val_err',
 '_Gen_dist_constraint.Intensity_upper_val_err',
 '_Gen_dist_constraint.Distance_val',
 '_Gen_dist_constraint.Distance_lower_bound_val',
 '_Gen_dist_constraint.Distance_upper_bound_val',
 '_Gen_dist_constraint.Contribution_fractional_val',
 '_Gen_dist_constraint.Spectral_peak_ID',
 '_Gen_dist_constraint.Spectral_peak_list_ID',
 '_Gen_dist_constraint.PDB_record_ID_1',
 '_Gen_dist_constraint.PDB_model_num_1',
 '_Gen_dist_constraint.PDB_strand_ID_1',
 '_Gen_dist_constraint.PDB_ins_code_1',
 '_Gen_dist_constraint.PDB_residue_no_1',
 '_Gen_dist_constraint.PDB_residue_name_1',
 '_Gen_dist_constraint.PDB_atom_name_1',
 '_Gen_dist_constraint.PDB_record_ID_2',
 '_Gen_dist_constraint.PDB_model_num_2',
 '_Gen_dist_constraint.PDB_strand_ID_2',
 '_Gen_dist_constraint.PDB_ins_code_2',
 '_Gen_dist_constraint.PDB_residue_no_2',
 '_Gen_dist_constraint.PDB_residue_name_2',
 '_Gen_dist_constraint.PDB_atom_name_2',
 '_Gen_dist_constraint.Auth_entity_assembly_ID_1',
 '_Gen_dist_constraint.Auth_asym_ID_1',
 '_Gen_dist_constraint.Auth_chain_ID_1',
 '_Gen_dist_constraint.Auth_seq_ID_1',
 '_Gen_dist_constraint.Auth_comp_ID_1',
 '_Gen_dist_constraint.Auth_atom_ID_1',
 '_Gen_dist_constraint.Auth_alt_ID_1',
 '_Gen_dist_constraint.Auth_atom_name_1',
 '_Gen_dist_constraint.Auth_entity_assembly_ID_2',
 '_Gen_dist_constraint.Auth_asym_ID_2',
 '_Gen_dist_constraint.Auth_chain_ID_2',
 '_Gen_dist_constraint.Auth_seq_ID_2',
 '_Gen_dist_constraint.Auth_comp_ID_2',
 '_Gen_dist_constraint.Auth_atom_ID_2',
 '_Gen_dist_constraint.Auth_alt_ID_2',
 '_Gen_dist_constraint.Auth_atom_name_2',
 '_Gen_dist_constraint.Entry_ID',
 '_Gen_dist_constraint.Gen_dist_constraint_list_ID']


    lines = [l.split() for l in open(filename).readlines() if len(l.split()) == 64]
    df = pd.DataFrame(lines, columns=columns)

    return df.convert_objects(convert_numeric=True)
