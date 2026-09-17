# Week 4 structural biology lab report

## 1. Question

The exact question is whether residues **18–28 of human canonical p53 can be handed to medicinal chemistry as a fixed structural target in unbound p53**.

The owner's decision rule requires both of the following: (1) the per-residue `B_iso_or_equiv` values for residues 18–28 must occupy the same strong range as the local values for residues 94–312; and (2) `predicted_aligned_error` (PAE) must support consistent positioning of residues 18–28 relative to the rest of p53. No arbitrary numerical cutoff was imposed.

## 2. Protein and files

The protein is canonical human p53, UniProt P04637, 393 residues. The analyzed inputs were `data-3/p53.fasta`, `data-3/p53_alphafold_model.cif`, and `data-3/p53_alphafold_pae.json`, together with the completed course GPU fold outputs under `results/`.

Both analyzed models correspond exactly to the owner's 393-aa canonical p53 construct: the sequence check found an exact match, with no mismatches, missing residues, insertions, truncation, mutation, or purification tag. Each model contains one p53 chain, residues 1–393, and no MDM2 or other protein partner. The evaluated state is therefore unbound p53, not an MDM2-bound or otherwise partner-bound assembly.

## 3. Right confidence

**pLDDT** is local model confidence. For the AlphaFold model, `B_iso_or_equiv` was read as the per-residue pLDDT. For the course GPU model, the saved per-residue pLDDT output was used.

For residues 18–28, the AlphaFold pLDDT summary is mean **68.88**, median **71.25**, minimum **57.66**, and maximum **77.12**. The corresponding course GPU values are mean **70.74**, median **72.49**, minimum **58.95**, and maximum **78.99**.

For the comparison region 94–312, AlphaFold gives mean **90.84**, median **96.62**, minimum **39.03**, and maximum **98.69**. The course GPU fold gives mean **86.32**, median **90.81**, minimum **49.43**, and maximum **97.26**. Thus 94–312 is heterogeneous rather than uniformly reliable, but the central distribution is stronger than residues 18–28 in both sources. These summaries are comparisons, not an arbitrary pass/fail cutoff.

**PAE** is different: it reports confidence in the relative placement of regions. For AlphaFold, the directional PAE for 18–28 relative to 94–312 is mean/median **30.70/31.00 Å** in the 18–28 → 94–312 direction, and **28.65/29.00 Å** in the reverse direction. For the course GPU fold, the corresponding values are **28.06/28.06 Å** and **28.49/28.37 Å**. Within-core PAE is much lower: AlphaFold 94–312 → 94–312 is mean/median **7.03/3.00 Å**, and the course model is **6.21/2.06 Å**. The directional values were retained rather than averaged.

## 4. Structure check

After alignment using Cα atoms from residues 94–312, the core Cα RMSD was **5.47 Å**. The residues 18–28 Cα RMSD after that core alignment was **24.03 Å**. RMSD here is a geometry/model-agreement observation, not a confidence score.

The supplied AlphaFold model has a helix-like appearance/annotation around part of residues 18–24. That attractive appearance alone is insufficient for the owner's decision, because local geometry does not establish either matched local confidence or consistent placement relative to the rest of p53.

## 5. Trap / honest truth

The familiar MDM2-contacting residues Phe19, Trp23, and Leu26 are in the 18–28 motif, and the MDM2-bound helix is relevant for a partner-bound design or an interface-mimic design. It does not establish a fixed conformation for residues 18–28 in unbound p53.

The present prediction evidence does **not** prove intrinsic disorder or experimental flexibility. It shows lower local pLDDT for 18–28 than for the central comparison distribution and high directional PAE for its placement relative to 94–312 in both models. These are the confidence observations relevant to the unbound decision.

## 6. Recommendation

Under Dr Margit Holló's decision rule, residues 18–28 are materially weaker than the comparison region on the local-confidence comparison and fail the relative-placement comparison. Therefore, residues **18–28 are not supported for independent handoff as a fixed structural target in unbound p53**.

The alternative is not an automatic recommendation of the entire 94–312 interval. That interval must be assessed residue by residue using local pLDDT together with the relevant PAE. The existing descriptive strong/weak/mixed categories may help organize that review, but they are descriptive analysis labels, not owner-defined decision thresholds.

## 7. Caveats and next steps

- The conclusion applies to the supplied unbound prediction models and the owner's comparative file-based rule; it is not an experimental structure determination.
- pLDDT should not be used as a substitute for PAE when judging placement between regions.
- Review residues 94–312 individually, retaining both their local pLDDT and PAE context rather than endorsing the whole interval from a regional summary.
- If the intended medicinal-chemistry objective is the MDM2-engaged conformation or an interface mimic, evaluate that partner-bound design question separately; it is not evidence for an unbound fixed target.
- Any subsequent structural or experimental validation should be designed around the specific residue-level candidates and biological state being targeted.

## 8. AI disclosure

Pi/AI assisted with scripted parsing, confidence extraction, visualization, cross-model comparison, and drafting. The interview-derived question and decision rule, sequence/state checks, and final scientific interpretation were manually reviewed against the supplied interview, specification, scripts, and result summaries.
