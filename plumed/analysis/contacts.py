from MDAnalysis.lib import distances as cdists
import numpy as np

def get_contacts(gr, lower_cutoff=0.0, upper_cutoff=6.0, min_resid_separation=4):
	contacts = []
    # symmetric distancen matrix, ie. dist[i,j] == dist[j,i]
	dist = cdists.distance_array(gr.positions, gr.positions)
	mask = np.argwhere((dist < upper_cutoff) & (dist > lower_cutoff))

	for i, j in mask:
		if i == j: continue
		if abs(gr[i].resid - gr[j].resid) <= min_resid_separation: continue
		key = frozenset((i, j))
		contacts.append(key)

	return dist, set(contacts)

def get_lines(contacts, gr, beta, alpha):
	lines = []
	for i, ((iA, iB), d) in enumerate(contacts.items()):
		line = "ATOMS{}={},{} SWITCH{}=(EXP R_0={:f} D_0={:f}) WEIGHT{}={:f}".format(
			i+1, gr[iA].id, gr[iB].id,
			i+1, beta, alpha * d * 0.1,
			i+1, 1./len(contacts),
		)
		lines.append(line.replace("(","{").replace(")", "}"))
	return lines

def filter_contacts(
        unique_contacts_A,
        unique_contacts_B,
        distances_A,
        distances_B,
        alpha
    ):

	filtered_contacts = {}

	for idA, idB in unique_contacts_A:
		d_A = distances_A[idA, idB]
		d_B = distances_B[idA, idB]
		if min(d_A, d_B) * alpha > max(d_A, d_B): continue
		filtered_contacts[(idA, idB)] = d_A

	return filtered_contacts

def write_lines(lines, filename, label):
    template = """
CONTACTMAP ...
%s
LABEL=%s
SUM
... CONTACTMAP
    """ % ("\n".join(lines), label)
    print("Saving {} contacts to {}".format(len(lines), filename))
    open(filename, "w").write(template)
