# Final evidence-based interpretation

## 1. Exact question
Whether residues 18–28 can be handed to medicinal chemistry as a fixed structural target in unbound p53.

## 2. Sequence/model validity
Both models represent the exact 393-residue sequence from `data-3/p53.fasta`, matching the owner's canonical human p53 construct (UniProt P04637) exactly, with no mismatches, missing residues, insertions, or truncation. The original AlphaFold mmCIF and course model each contain one p53 chain, residues 1–393, with no MDM2 or other protein partner.

## 3. Local confidence
For AlphaFold, residues 18–28 have pLDDT mean/median/min/max 68.88/71.25/57.66/77.12; residues 94–312 have 90.84/96.62/39.03/98.69. For the course model, residues 18–28 have 70.74/72.49/58.95/78.99; residues 94–312 have 86.32/90.81/49.43/97.26. The 94–312 region is heterogeneous, not uniformly reliable: its lower tail is weak, especially at residues 294–312 in both models, while much of 105–293 is stronger.

## 4. Placement confidence
For AlphaFold, 18–28 → 94–312 has PAE mean/median 30.70/31.00 Å and the reverse direction is 28.65/29.00 Å. For the course model the corresponding values are 28.06/28.06 Å and 28.49/28.37 Å. Within-core PAE is much lower: AlphaFold mean/median 7.03/3.00 Å; course mean/median 6.21/2.06 Å. Directionality was retained; no directional averaging was used.

## 5. Structural geometry
After alignment using Cα atoms of residues 94–312, the core RMSD was 5.47 Å and the 18–28 RMSD was 24.03 Å. This is geometry disagreement between the predictions, not itself a confidence score. The supplied AlphaFold model has helix-like annotation around part of 18–24; the course PDB has no equivalent returned secondary-structure annotation. The coordinate comparison does not establish intrinsic disorder or experimental flexibility.

## 6. Owner's decision rule
- **pLDDT condition:** Not supported as a matched strong range across both prediction sources: 18–28 is consistently lower than the central 94–312 distributions, although 94–312 itself has a heterogeneous low-confidence tail.
- **PAE placement condition:** Not supported: both models show high directional PAE for 18–28 relative to 94–312, unlike their much lower within-core PAE.

Under the owner's rule, if 18–28 is materially weaker on either comparison, there is no independent handoff of residues 18–28.

## 7. Biological interpretation
A local helix-like appearance is a geometric feature of a prediction. It is distinct from local pLDDT, which reports local model confidence, and from PAE, which addresses confidence in relative placement to the rest of p53. The MDM2-bound helix is an experimentally observed partner-bound conformation, but it does not by itself establish a fixed conformation in unbound p53. These prediction data do not prove intrinsic disorder or experimentally prove flexibility; they support lower local confidence and uncertain relative placement for 18–28 in these models.

## 8. Alternative region
The owner's instruction is to assess residues 94–312 residue by residue, not to declare the whole interval suitable. A descriptive table is saved in `alternative_region_table.json`. For orientation only, the table labels pLDDT >=90 in both models as descriptively strong and pLDDT <70 in both as descriptively weak; these are not decision cutoffs. Broadly, residues 105–179, 191–227, 229–242, 244–246, 249–259, 264–267, 269–282, and 284–288 contain many/mostly jointly strong positions, while residues 183, 185, and 294–312 are weak in both models. Mixed/intermediate positions must be assessed individually with their PAE context. No portion is automatically endorsed solely by this summary.

## 9. Final concise answer
The two prediction sources do not support treating residues 18–28 as a fixed, independently placed structural target in unbound p53 under Dr Holló's rule. The next evaluation should be a residue-by-residue assessment of 94–312, retaining both local pLDDT and relevant PAE rather than assuming the entire core interval is suitable.
