
from MDAnalysis import Universe
from plumed.contacts import get_contacts, get_lines, filter_contacts, write_lines
import numpy as np
import argparse
import glob

parser = argparse.ArgumentParser()
parser.add_argument("--beta", default=1/50., type=float)
parser.add_argument("--alpha", default=1.8, type=float)
parser.add_argument("--kappa", default=0.0, type=float)
parser.add_argument("--slope", default=0.0, type=float)
args = parser.parse_args()

u_in = Universe("protein-pace-inward.pdb")
u_out = Universe("protein-pace-outward.pdb")

#select = "((resid 1-80) or (resid 91-170)) and protein and not name H* and not "
select = "protein and not name H* and not "
select += """ (
	(resname ASP and name OD*) or
	(resname GLU and name OE*) or
	(resname PHE and (name CD* or name CE*)) or
	(resname TYR and (name CD* or name CE*)) or
	(resname ARG and name NH*) or
	(resname VAL and name CG*) or
	(resname LEU and name CD*)
)
"""

gr_in = u_in.select_atoms(select)
gr_out = u_out.select_atoms(select)
print("Selected atoms # {} {}".format(len(gr_in), len(gr_out)))

distances_inward, contacts_inward = get_contacts(gr_in)
distances_outward, contacts_outward = get_contacts(gr_out)
print("Distance array dimensions {} {}".format(
	distances_inward.shape.__repr__(),
	distances_outward.shape.__repr__(),
))

contacts_inward_unique = contacts_inward - contacts_outward
contacts_outward_unique = contacts_outward - contacts_inward

# remove inward
filtered_contacts_inward = filter_contacts(
	contacts_inward_unique,
	contacts_outward_unique,
	distances_inward,
	distances_outward,
	args.alpha
)

filtered_contacts_out = filter_contacts(
	contacts_outward_unique,
	contacts_inward_unique,
	distances_outward,
	distances_inward,
	args.alpha
)

lines_in = get_lines(filtered_contacts_inward, gr_in, args.beta, args.alpha)
lines_out = get_lines(filtered_contacts_out, gr_out, args.beta, args.alpha)

write_lines(lines_in, "plumed_in.dat", "cmap_in")
write_lines(lines_out, "plumed_out.dat", "cmap_out")

keys_set_shared = contacts_inward.intersection(contacts_outward)
contacts_shared = {
	frozenset((iA, iB)) : np.mean((distances_inward[iA, iB], distances_outward[iA, iB])) \
	for i, (iA, iB) in enumerate(keys_set_shared) \
	if abs(distances_inward[iA, iB] - distances_outward[iA, iB]) < 1.0
}
lines_shared = get_lines(contacts_shared, gr_out, args.beta, args.alpha)
write_lines(lines_shared, "plumed_shared.dat", "cmap_shared")

u = Universe("conf.gro")
gr = u.select_atoms("protein")
grA = gr[:len(gr)/2]
grB = gr[len(gr)/2:]

header = """
#RESTART
WHOLEMOLECULES STRIDE=1000 ENTITY0={}-{} ENTITY1={}-{}

""".format(
  grA.indices[0] + 1,
  grA.indices[-1] + 1,
  grB.indices[0] + 1,
  grB.indices[-1] + 1,
)

template = """

INCLUDE FILE=plumed_in.dat
INCLUDE FILE=plumed_out.dat
INCLUDE FILE=plumed_shared.dat

cmap: COMBINE ARG=cmap_in,cmap_out COEFFICIENTS=1,-1 PERIODIC=NO
lwall: LOWER_WALLS ARG=cmap_shared AT=1.0 KAPPA=1000 EXP=2 EPS=1 OFFSET=0


restraint: RESTRAINT ARG=cmap AT=%f KAPPA=%g

PRINT ARG=* FILE=COLVAR STRIDE=1000
"""

centers = np.linspace(-1,1,32)
weights = np.linspace(args.kappa,args.kappa,32)
data = zip(centers, weights)

for i, (center, weight) in enumerate(data):
 	body = template % (
		center, weight
	)
	open("plumed.{}.dat".format(i), "w").writelines(header + body)
