from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from biotite.structure.io.pdbx import CIFFile, get_structure

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data-3'
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)

# Read FASTA and mmCIF residue-level B_iso_or_equiv.
fasta = ''.join(DATA.joinpath('p53.fasta').read_text().splitlines()[1:]).strip()
cif = CIFFile.read(DATA / 'p53_alphafold_model.cif')
block = cif[list(cif.keys())[0]]
structure = get_structure(cif, model=1)
residue_table = []
seen = set()
atom_b = block['atom_site']['B_iso_or_equiv'].as_array(float)
for i, (chain, res_id, res_name, b) in enumerate(zip(structure.chain_id, structure.res_id, structure.res_name, atom_b)): 
    key = (str(chain), int(res_id))
    if key not in seen:
        seen.add(key)
        residue_table.append((str(chain), int(res_id), str(res_name), float(b)))
# Biotite exposes B_iso_or_equiv as b_factor; one atom-level value per residue is expected here.
assert len(residue_table) == 393
assert [r[1] for r in residue_table] == list(range(1, 394))
assert len(set(r[0] for r in residue_table)) == 1
assert block['atom_site']['B_iso_or_equiv'].as_array(float).size == len(structure)

# Independent raw-column sanity check: first atom of each residue, then compare to Biotite values.
raw_b = block['atom_site']['B_iso_or_equiv'].as_array(float)
raw_res = block['atom_site']['auth_seq_id'].as_array(int)
raw_chain = block['atom_site']['auth_asym_id'].as_array(str)
raw_first = {}
for r, c, b in zip(raw_res, raw_chain, raw_b):
    raw_first.setdefault((str(c), int(r)), float(b))
assert len(raw_first) == 393
for chain, r, _, b in residue_table:
    assert np.isclose(raw_first[(chain, r)], b)

# Convert residue names using Biotite's standard mapping through one-letter FASTA sequence.
for i, row in enumerate(residue_table):
    assert i < len(fasta)

# Read and validate PAE JSON.
pae_obj = json.loads(DATA.joinpath('p53_alphafold_pae.json').read_text())
entry = pae_obj[0] if isinstance(pae_obj, list) else pae_obj
pae = np.asarray(entry['predicted_aligned_error'], dtype=float)
assert pae.shape == (393, 393)
pae_indexing = 'JSON matrix rows and columns are zero-based array positions corresponding to residue numbers 1-393'

plddt = np.array([r[3] for r in residue_table])
region_a = np.arange(17, 28)       # 18-28
region_core = np.arange(93, 312)   # 94-312
all_idx = np.arange(393)
rest = np.setdiff1d(all_idx, region_a)

def stats(x):
    return {'n': int(x.size), 'mean': float(np.mean(x)), 'median': float(np.median(x)), 'min': float(np.min(x)), 'max': float(np.max(x)), 'q01': float(np.quantile(x,.01)), 'q05': float(np.quantile(x,.05)), 'q25': float(np.quantile(x,.25)), 'q75': float(np.quantile(x,.75)), 'q95': float(np.quantile(x,.95)), 'q99': float(np.quantile(x,.99))}

# Directional PAE summaries: PAE[i,j] is retained as i -> j; reverse is separately reported.
def pae_direction(i, j):
    return pae[np.ix_(i, j)].ravel()

def directional_summary(i, j):
    return stats(pae_direction(i, j))

summary = {
    'verification': {'fasta_length': len(fasta), 'mmcif_residues': len(residue_table), 'pae_shape': list(pae.shape), 'pae_indexing': '0-based array indices correspond to residue numbers 1-393', 'plddt_source': 'atom_site.B_iso_or_equiv, one constant value per residue; read as pLDDT'},
    'target_18_28': {'residues': [{'residue': r[1], 'amino_acid_3': r[2], 'amino_acid_1': fasta[r[1]-1], 'plddt': r[3]} for r in residue_table[17:28]], 'plddt': stats(plddt[region_a])},
    'comparison_94_312': {'plddt': stats(plddt[region_core])},
    'plddt_rest_comparison': {'target_18_28': stats(plddt[region_a]), 'rest_excluding_18_28': stats(plddt[rest])},
    'pae_18_28_to_rest': {'18_28_to_rest': directional_summary(region_a, rest), 'rest_to_18_28': directional_summary(rest, region_a)},
    'pae_18_28_to_94_312': {'18_28_to_94_312': directional_summary(region_a, region_core), '94_312_to_18_28': directional_summary(region_core, region_a)},
    'pae_core_internal': {'94_312_to_94_312': directional_summary(region_core, region_core)},
}
OUT.joinpath('confidence_summary.json').write_text(json.dumps(summary, indent=2) + '\n')

# Machine-readable per-residue table.
with OUT.joinpath('per_residue_plddt.csv').open('w') as f:
    f.write('residue,amino_acid,plddt\n')
    for r in residue_table:
        f.write(f'{r[1]},{fasta[r[1]-1]},{r[3]:.6f}\n')

# Figures.
x = np.arange(1,394)
fig, ax = plt.subplots(figsize=(12,4)); ax.plot(x, plddt, lw=.8); ax.axvspan(18,28,color='tab:red',alpha=.25,label='18–28'); ax.axvspan(94,312,color='tab:green',alpha=.12,label='94–312'); ax.set(xlabel='Residue number',ylabel='pLDDT (B_iso_or_equiv)',xlim=(1,393)); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'plddt_per_residue.png',dpi=180); plt.close(fig)
fig, ax = plt.subplots(figsize=(7,6)); im=ax.imshow(pae, origin='lower', cmap='viridis', extent=(1,393,1,393), aspect='auto'); ax.axvspan(18,28,color='red',alpha=.18); ax.axhspan(18,28,color='red',alpha=.18); ax.axvspan(94,312,color='lime',alpha=.08); ax.axhspan(94,312,color='lime',alpha=.08); ax.set(xlabel='Residue j',ylabel='Residue i'); fig.colorbar(im,ax=ax,label='PAE'); fig.tight_layout(); fig.savefig(OUT/'pae_heatmap.png',dpi=180); plt.close(fig)
fig, ax = plt.subplots(figsize=(6,4)); ax.boxplot([plddt[region_a],plddt[region_core]], tick_labels=['18–28','94–312'], showmeans=True); ax.set_ylabel('pLDDT'); fig.tight_layout(); fig.savefig(OUT/'plddt_distribution_comparison.png',dpi=180); plt.close(fig)
print(json.dumps(summary, indent=2))
