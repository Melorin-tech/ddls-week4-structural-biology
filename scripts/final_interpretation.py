from pathlib import Path
import json, csv
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data-3'; O=ROOT/'results'; C=O/'cross_model_comparison'; out=O/'final_interpretation'; out.mkdir(exist_ok=True)
x=json.loads((C/'cross_model_summary.json').read_text())
rows=list(csv.DictReader((C/'course_per_residue_plddt.csv').open()))
af=json.loads((O/'confidence_summary.json').read_text())
# Descriptive segmentation only: not the owner's decision threshold.
# Mark a position strong in a model when pLDDT >= 90, weak otherwise; report both models.
segments=[]
for i in range(94,313):
    a=float(json.loads((O/'per_residue_plddt.csv').read_text().splitlines()[i].split(',')[2]))
    c=float(rows[i-1]['plddt'])
    label='both_descriptively_strong' if a>=90 and c>=90 else ('both_descriptively_weak' if a<70 and c<70 else 'mixed_or_intermediate')
    if segments and segments[-1]['label']==label and segments[-1]['end']==i-1: segments[-1]['end']=i
    else: segments.append({'start':i,'end':i,'label':label})
for s in segments:
 vals=[]
 for i in range(s['start'],s['end']+1): vals.append((float(json.loads((O/'per_residue_plddt.csv').read_text().splitlines()[i].split(',')[2]),),float(rows[i-1]['plddt'])))
 s.update({'length':s['end']-s['start']+1,'alphafold_plddt_mean':float(np.mean([v[0] for v in vals])),'course_plddt_mean':float(np.mean([v[1] for v in vals]))})
result={'alternative_region_descriptive_segments':segments,'note':'pLDDT >=90 and <70 are descriptive summaries only, not predefined decision cutoffs; PAE must be consulted for placement.'}
(out/'alternative_region_table.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'final_interpretation.md').write_text('')
print(json.dumps(result,indent=2))
