# Scientific specification

## Owner and data
- **Owner:** Dr Margit Holló, Department of Oncology-Pathology, Karolinska Institutet.
- **Protein:** canonical human p53, UniProt P04637, 393 residues.
- **Input files:** `data-3/p53.fasta`, `data-3/p53_alphafold_model.cif`, and `data-3/p53_alphafold_pae.json`.
- According to the owner, the construct has no mutation, truncation, or purification tag.

## Exact decision
Determine whether residues **18–28** can be handed to medicinal chemistry as a fixed structural target in **unbound p53**.

The comparison region is residues **94–312**.

## Decision rule
Compare `B_iso_or_equiv` for residues 18–28 with the corresponding values for residues 94–312. Inspect `predicted_aligned_error` for placement of residues 18–28 relative to the protein, using the corresponding region-to-protein values in the JSON.

A yes requires both:
1. `B_iso_or_equiv` across 18–28 sits in the same strong range as the local values for 94–312; and
2. `predicted_aligned_error` supports consistent positioning of 18–28 relative to the rest of the protein.

If residues 18–28 are materially weaker on either comparison, there is no independent handoff of 18–28. Instead, assess residues 94–312 residue by residue; do not treat the entire interval as automatically suitable. No arbitrary numerical cutoff is imposed.

## Biological context
Residues 18–28 form the MDM2-binding motif, including the familiar MDM2-contacting residues Phe19, Trp23, and Leu26. The MDM2-bound helix does not by itself establish a fixed conformation in unbound p53. The unbound AlphaFold model must stand on its own under the comparative file-based test. MDM2-bound structural evidence is relevant if the intended design is against the MDM2-engaged conformation or to mimic that interface, but not as proof of an unbound fixed target.

## Required checks
Before interpreting the decision, confirm that:
- the model sequence matches the owner's construct;
- it is canonical human p53 UniProt P04637 and is 393 residues;
- there is no mutation, truncation, or purification tag relative to the owner's construct; and
- the assembly/state being evaluated is appropriate: the decision concerns unbound p53, not an MDM2-bound or otherwise partner-bound state.

## Done means
The work is done only when the sequence/model/assembly checks are reported, the residue-level `B_iso_or_equiv` comparison of 18–28 with 94–312 is reported, the relevant `predicted_aligned_error` placement assessment is reported, and the decision is stated according to the owner's comparative rule. If 18–28 fails either comparison, the result must state no independent handoff and assess 94–312 residue by residue instead.
