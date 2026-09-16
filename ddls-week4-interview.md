# DDLS 2026 — Week 4 interview transcript

**Lab:** Interview a Structural-Biology Data Owner
**Data owner:** Dr. Margit Holló — Structural cancer-biology researcher (p53)
**Student:** Negar Abbasi Aval <negar.abbasi.aval@scilifelab.se>
**Exported:** 2026-09-16T23:13:08+00:00

> This is the record of your interview with the data owner. Hand it to your analyst agent as the raw source for `AGENTS.md` and `spec.md`.

---

**You**:

Hi, thank you for speaking with me. Could you first walk me through the protein you are working with and what you are trying to find out from its structure? What experimental or practical decision will you make based on the answer?

**Dr. Margit Holló**:

I’m Dr Margit Holló, Department of Oncology-Pathology at Karolinska Institutet. We are working with human p53, using its reference sequence and an AlphaFold model. I want to know whether the small helix at the very front can serve as a fixed target for a medicinal-chemistry collaborator. The practical decision is whether to give them that structural feature to design against; do you want to start with the sequence, the model, or the decision rule?

**You**:

Let’s start with the structural feature you want to use for the decision. Which exact residues make up the small helix at the front, and what about the AlphaFold model makes you confident that this helix is a stable, fixed structure that the medicinal-chemistry team can design against?

**Dr. Margit Holló**:

The feature I mean is **residues 18–28**, approximately **TFS DLWKLLPE** in the reference sequence. In the model it appears as a clean, continuous helix, with the familiar MDM2-contacting residues **Phe19, Trp23 and Leu26** presented on one face. That is what caught my eye; why are you asking whether the picture is enough for the design decision?

**You**:

’m asking because I want to understand exactly what evidence you are relying on before I translate this into a design recommendation. Apart from how residues 18–28 look in the AlphaFold model, is there any experimental or biological evidence that this region forms a stable helix on its own, and do you know whether its structure changes when p53 interacts with MDM2 or another partner?

**Dr. Margit Holló**:

Honestly, that end of p53 is pretty floppy in the tube until it latches onto MDM2; the helix is well defined in the MDM2-bound complex, where **Phe19, Trp23 and Leu26** occupy the binding pocket. I do not know of evidence that residues 18–28 maintain the same stable helix free of a partner; I saw the clear helix in the model and assumed it was fine. For the design recommendation, are you now checking the model’s numerical support for **18–28**, or comparing it with the proposed core region **94–312**?

**You**:

Yes, I would like to compare the numerical support for residues 18–28 with the structured core region 94–312. Before that, I want to make sure I understand exactly what model we are evaluating. Is the AlphaFold model the full-length canonical human p53 reference sequence, and is that sequence identical to the construct relevant to your design work, with no mutations, truncations or tags? Also, do you have the FASTA sequence and the AlphaFold structure/confidence files available for the analysis?

**Dr. Margit Holló**:

Yes. The files represent the **canonical human p53, UniProt P04637, 393 residues**—the reference sequence, with no mutation, truncation, or purification tag. I have `p53.fasta`, `p53_alphafold_model.cif`, and the accompanying `p53_alphafold_pae.json`; the first two are straightforward, while the large numeric companion file is the one you must interpret. Compare residues **18–28** against **94–312** using the residue-level values in the structure file and the corresponding region-to-protein values in the JSON.

**You**:

For the actual design decision, what would you consider sufficient evidence to tell the medicinal-chemistry collaborator that residues 18–28 can be treated as a fixed structural target? And if the model shows that this region is substantially less reliable than the 94–312 core, what would you want us to recommend instead?

**Dr. Margit Holló**:

A **yes** requires two things in the files: the `B_iso_or_equiv` values across **18–28** must sit in the same strong range as the local values for **94–312**, and `predicted_aligned_error` must show that 18–28 is positioned consistently relative to the rest of the protein. The attractive helix alone is not sufficient.

If either test fails, my recommendation is **no handoff for 18–28**; assess **94–312** as the design region instead, residue by residue, rather than treating the entire interval as automatically suitable. Biologically, the front segment is the MDM2-binding motif, not an independently established rigid domain; do you want a simple numerical cutoff, or only this comparative rule?

**You**:

The comparative rule is sufficient; I would prefer not to impose an arbitrary cutoff that you did not use for the decision. One final point about biological context: if residues 18–28 are well defined when bound to MDM2 but uncertain in the unbound AlphaFold model, would you consider the MDM2-bound experimental structure relevant supporting evidence, or is the medicinal-chemistry decision specifically about whether the unbound p53 model provides a fixed target independently of MDM2?

**Dr. Margit Holló**:

The MDM2-bound structure is relevant only if the chemists intend to design against the **MDM2-engaged conformation** or to mimic that interface. It does not establish that residues 18–28 are a fixed target in unbound p53; for that decision, the unbound AlphaFold model must stand on its own under the comparative file-based test. So if 18–28 falls short against **94–312**, I would not hand over the helix as an independent target—use the core region instead.

**You**:

Let me play this back to make sure I have the decision correctly. You want me to determine whether residues 18–28 of canonical 393-residue human p53 can be handed to the medicinal-chemistry team as a fixed structural target in unbound p53, by comparing their residue-level confidence with residues 94–312 and checking whether the PAE supports consistent positioning of 18–28 relative to the rest of the protein. If either confidence test is weaker than the core comparison, the conclusion should be no handoff of 18–28 as an independent fixed target, and instead I should assess residues 94–312 residue by residue as the alternative design region; the MDM2-bound helix is relevant biological context but does not validate rigidity in unbound p53. Is that an accurate statement of your question and decision rule?

**Dr. Margit Holló**:

Yes. That is the question and the decision rule: compare **`B_iso_or_equiv`** for 18–28 against 94–312, then inspect the relevant **`predicted_aligned_error`** values for its placement relative to the protein. If 18–28 is materially weaker on either comparison, no independent handoff; evaluate **94–312** residue by residue. The MDM2-bound helix supports a partner-bound conformation, not an unbound fixed target.
