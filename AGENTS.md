# Project guidance

## Scientific goal
Determine whether residues 18–28 of canonical human p53 can be handed to medicinal chemistry as a fixed structural target in unbound p53. If they are not sufficiently supported relative to the structured core, assess residues 94–312 residue by residue as the alternative design region.

## Working rules
- All Python must use `uv`.
- Input data are in `data-3/`: `p53.fasta`, `p53_alphafold_model.cif`, and `p53_alphafold_pae.json`.
- Interpret `B_iso_or_equiv` in the structure file as the residue-level confidence values, and interpret the corresponding `predicted_aligned_error` values in the JSON as confidence for placement of residues 18–28 relative to the protein.
- Outputs go in `results/`.
- Never report a structural conclusion without first reporting the confidence that matches the exact claim.
- Always confirm that the model sequence matches the owner's construct and that the assembly/state is appropriate.
- See `spec.md` for the full scientific specification.

## Version control
Before any big change, commit the current working state first, and commit again whenever something starts working, using short clear commit messages.
