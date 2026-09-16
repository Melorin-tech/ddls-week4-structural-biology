# Project guidance

## Scientific goal
Determine whether residues 18–28 of canonical human p53 can be handed to medicinal chemistry as a fixed structural target in unbound p53. If they are not sufficiently supported relative to the structured core, assess residues 94–312 residue by residue as the alternative design region.

## Working rules
- All Python must use `uv`.
- Input data are in `data-3/`: `p53.fasta`, `p53_alphafold_model.cif`, and `p53_alphafold_pae.json`.
- For this AlphaFold mmCIF, read `B_iso_or_equiv` as per-residue pLDDT. In the JSON, `predicted_aligned_error` is PAE and must be used to assess placement of residues 18–28 relative to the rest of p53; pLDDT alone does not establish that placement consistency.
- Outputs go in `results/`.
- Never report a structural conclusion without first reporting the confidence that matches the exact claim.
- Always confirm that the model sequence matches the owner's construct and that the assembly/state is appropriate.
- See `spec.md` for the full scientific specification.

## Version control
Before any big change, commit the current working state first, and commit again whenever something starts working, using short clear commit messages.
