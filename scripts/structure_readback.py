from pathlib import Path
import re
from biotite.structure.io.pdbx import CIFFile, get_structure

FASTA = Path('data-3/p53.fasta')
MMCIF = Path('data-3/p53_alphafold_model.cif')

fasta_lines = FASTA.read_text().splitlines()
header = fasta_lines[0]
fasta_seq = ''.join(fasta_lines[1:]).replace(' ', '').upper()

cif = CIFFile.read(MMCIF)
block = cif[list(cif.keys())[0]]
structure = get_structure(cif, model=1)
poly = block['entity_poly_seq']
entity_seq = poly['mon_id'].as_array(str).tolist()
three_to_one = {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
entity_seq = ''.join(three_to_one[x] for x in entity_seq)

chains = sorted(set(structure.chain_id))
res_keys = []
seen = set()
for chain, res_id, ins in zip(structure.chain_id, structure.res_id, structure.ins_code):
    key = (chain, int(res_id), ins)
    if key not in seen:
        seen.add(key); res_keys.append(key)

print('FASTA header:', header)
print('FASTA length:', len(fasta_seq))
print('mmCIF modeled chains:', chains)
print('mmCIF modeled residues:', len(res_keys))
print('mmCIF residue ranges:', {c: (min(r for ch,r,i in res_keys if ch==c), max(r for ch,r,i in res_keys if ch==c)) for c in chains})
print('entity_poly sequence length:', len(entity_seq))
print('entity_poly vs FASTA length match:', len(entity_seq) == len(fasta_seq))
print('entity_poly vs FASTA exact match:', entity_seq == fasta_seq)
if entity_seq != fasta_seq:
    print('mismatches:', [(i+1,a,b) for i,(a,b) in enumerate(zip(entity_seq,fasta_seq)) if a != b])
print('mmCIF data block:', list(cif.keys())[0])
print('entity description:', block['entity']['pdbx_description'].as_item())
print('entity molecules:', block['entity']['pdbx_number_of_molecules'].as_item())
print('struct_asym IDs:', block['struct_asym']['id'].as_array(str).tolist())
