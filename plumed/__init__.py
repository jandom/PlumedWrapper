
import pandas as pd 

def read_wham(f):
	df = pd.read_csv(f, sep="\t", comment="#",header=None)
	columns = "Coor		Free	FreeErr		Prob		ProbErr".split()
	df.columns = columns
	return df

def read_colvar(f):
	lines = open(f).readlines()
	columns = lines[0].split()[2:]
	data = []
	for i, l in enumerate(lines):
		if l.startswith("#"): continue
		try: 
			row = map(float, l.split())
			if len(row) != len(columns): continue
			data.append(row)
		except ValueError:
			print i, l
	#data = [map(float, l.split()) for i, l in enumerate(lines) if not l.startswith("#")]
	df = pd.DataFrame(data , columns=columns)
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
