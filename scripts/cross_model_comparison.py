from pathlib import Path
import json, csv
import numpy as np
import matplotlib.pyplot as plt
from biotite.structure.io.pdb import PDBFile
from biotite.structure.io.pdbx import CIFFile, get_structure
from biotite.structure import superimpose, rmsd
from mpl_toolkits.mplot3d import Axes3D
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data-3'; C=ROOT/'results/course_gpu_fold_p53'; O=ROOT/'results/cross_model_comparison'; O.mkdir(exist_ok=True)

def stats(a):
 a=np.asarray(a,float); return {'n':int(a.size),'mean':float(a.mean()),'median':float(np.median(a)),'min':float(a.min()),'max':float(a.max()),'q01':float(np.quantile(a,.01)),'q05':float(np.quantile(a,.05)),'q25':float(np.quantile(a,.25)),'q75':float(np.quantile(a,.75)),'q95':float(np.quantile(a,.95)),'q99':float(np.quantile(a,.99))}
def dirs(pae,a,b): return {'forward':stats(pae[np.ix_(a,b)]),'reverse':stats(pae[np.ix_(b,a)])}
def one_letter(name): return {'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}[name]
fasta=''.join(D.joinpath('p53.fasta').read_text().splitlines()[1:])
# Original model confidence and coordinates
cf=CIFFile.read(D/'p53_alphafold_model.cif'); cs=get_structure(cf,model=1); cb=cf[list(cf.keys())[0]]['atom_site']['B_iso_or_equiv'].as_array(float)
seen=set(); af=[]; af_b=[]
for atom,b in zip(cs,cb):
 k=(str(atom.chain_id),int(atom.res_id))
 if k not in seen: seen.add(k); af.append(atom); af_b.append(float(b))
af_b=np.array(af_b)
# Course PDB; per-residue plddt is returned JSON, PDB sequence is checked from atom records
pdb=PDBFile.read(C/'folded_structure.pdb'); ps=pdb.get_structure(model=1); x=json.loads((C/'fold_response.json').read_text()); cu_b=np.array(x['plddt'],float); pae_af=np.array(json.loads((D/'p53_alphafold_pae.json').read_text())[0]['predicted_aligned_error'],float); pae_c=np.array(x['pae'],float)
res=[]; seen=set()
for atom in ps:
 k=(str(atom.chain_id),int(atom.res_id),str(atom.ins_code))
 if k not in seen: seen.add(k); res.append((str(atom.chain_id),int(atom.res_id),str(atom.res_name)))
seq=''.join(one_letter(r[2]) for r in res)
assert len(seq)==393 and seq==fasta and [r[1] for r in res]==list(range(1,394))
A=np.arange(393); T=np.arange(17,28); K=np.arange(93,312); R=np.setdiff1d(A,T)
summary={'sequence_check':{'length':len(seq),'exact_match':seq==fasta,'mismatches':[],'missing':[],'insertions':[],'numbering':'chain A residues 1-393'},'plddt':{'alphaFold_18_28':stats(af_b[T]),'course_18_28':stats(cu_b[T]),'alphaFold_94_312':stats(af_b[K]),'course_94_312':stats(cu_b[K]),'course_18_28_residues':[{'residue':int(i+1),'amino_acid':fasta[i],'plddt':float(cu_b[i])} for i in T]},'pae':{'alphaFold_18_28_rest':dirs(pae_af,T,R),'course_18_28_rest':dirs(pae_c,T,R),'alphaFold_18_28_core':dirs(pae_af,T,K),'course_18_28_core':dirs(pae_c,T,K),'alphaFold_core_internal':stats(pae_af[np.ix_(K,K)]),'course_core_internal':stats(pae_c[np.ix_(K,K)])}}
# Alignment: CA atoms, core 94-312; RMSD target after that alignment
ca1=cs[(cs.atom_name=='CA')]; ca2=ps[(ps.atom_name=='CA')]
# order is residue order in this one-chain model
_,trans=superimpose(ca1[K],ca2[K]); aligned=ca2.copy(); aligned=trans.apply(aligned)
summary['geometry']={'alignment':'CA atoms of residues 94-312','target_rmsd_after_core_alignment':float(rmsd(ca1[T],aligned[T])),'core_rmsd':float(rmsd(ca1[K],aligned[K])),'helix_annotation':'secondary-structure/visual assessment required; coordinates and comparison plot saved'}
(O/'cross_model_summary.json').write_text(json.dumps(summary,indent=2)+'\n');
with (O/'course_per_residue_plddt.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['residue','amino_acid','plddt']);w.writerows((i+1,fasta[i],cu_b[i]) for i in range(393))
# plots
fig,ax=plt.subplots(figsize=(12,4));ax.plot(A+1,af_b,label='AlphaFold');ax.plot(A+1,cu_b,label='Course GPU',alpha=.8);ax.axvspan(18,28,color='red',alpha=.2);ax.axvspan(94,312,color='green',alpha=.1);ax.legend();ax.set(xlabel='Residue',ylabel='pLDDT',xlim=(1,393));fig.tight_layout();fig.savefig(O/'plddt_side_by_side.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,6));im=ax.imshow(pae_c,origin='lower',extent=(1,393,1,393),aspect='auto');ax.axvspan(18,28,color='red',alpha=.2);ax.axhspan(18,28,color='red',alpha=.2);ax.axvspan(94,312,color='lime',alpha=.1);ax.axhspan(94,312,color='lime',alpha=.1);ax.set(xlabel='Residue j',ylabel='Residue i');fig.colorbar(im,ax=ax,label='Course PAE (Å)');fig.tight_layout();fig.savefig(O/'course_pae_heatmap.png',dpi=180);plt.close(fig)
# CA 3D overlay, target red and core green
fig=plt.figure(figsize=(8,7));ax=fig.add_subplot(111,projection='3d'); ax.plot(ca1.coord[:,0],ca1.coord[:,1],ca1.coord[:,2],color='gray',alpha=.3);ax.plot(aligned.coord[:,0],aligned.coord[:,1],aligned.coord[:,2],color='black',alpha=.3);ax.plot(ca1.coord[T,0],ca1.coord[T,1],ca1.coord[T,2],color='red',lw=3,label='AlphaFold 18–28');ax.plot(aligned.coord[T,0],aligned.coord[T,1],aligned.coord[T,2],color='blue',lw=3,label='Course 18–28');ax.set_title('CA overlay; core 94–312 alignment');ax.legend();fig.tight_layout();fig.savefig(O/'ca_overlay_target.png',dpi=180);plt.close(fig)
print(json.dumps(summary,indent=2))
