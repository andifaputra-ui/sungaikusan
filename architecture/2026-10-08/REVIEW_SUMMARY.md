# Architecture decision in brief — 8 October 2026

**Recommendation: replace the legacy physical-context/reserve architecture with targeted development falsification plus a separate probability audit of one locked reconstruction.** No implementation of the new sampling/access rules has occurred.

Read [the complete decision](ARCHITECTURE_DECISION_FOR_REVIEW.md) for inference, migration, uncertainty and the strongest counterargument.

## Consequential choices proposed

1. Assess the fixed Kusan L1 lowland reconstruction over its explicitly enumerated 2017–2025 acquisition catalogue; do not claim whole-catchment or new-basin generalization.
2. Replace the central-block-only final population with the full L1 area. Preserve old reserve/exposure facts as reporting domains, rather than excluding their geography from fixed-map inference.
3. Use disjoint30 m response tiles anchored to the10 m map lattice, retaining partial edges and10/50 m sensitivity readings. Keep interval-valued references; do not introduce majority-water labels.
4. Use a small independent-evidence-first development panel to challenge persistent/new water, smooth land, mixed/small features, difficult observations and ordinary controls. Purposive development is explicitly not population validation.
5. After a candidate evaluation lock, sample acquisition dates probabilistically, process only those dates, then sample tiles from four mechanical frozen-map W/abstention strata. This explicitly replaces the old prediction-independent final-selection precaution. Reference readers remain blind to strata/predictions.
6. Make sampling auxiliaries optional. No complete RBI, GlobeLand30 or multisource thematic atlas is a prerequisite for final frame validity. Preserve all sources' declared roles and versions.
7. Keep final responses sealed until the candidate, response protocol and analysis are locked. Preserve UNKNOWN, nonresponse and original reader disagreement; no favourable replacement.

The proposed36-date/288-tile configuration is a planning scenario, not a sufficient sample-size declaration or authorization. The need for adequate acquisition-time references remains unresolved. A/B, new SAR, imagery orders, new randomization and final method freeze remain blocked.

## Strongest objection

This architecture needs more careful information governance and gives up an untouched-geography claim. Rare missed water can be poorly sampled within mapped non-water, and optical cloud/timing uncertainty may still prevent useful final accuracy bounds. No weighting scheme or larger sample repairs unobserved historical states.

## Verification

48 design/stratum checks passed, including243 exhaustively enumerated artificial sampling designs and19,683 artificial tile maps. A separate3,025-case exhaustive test checked12,100 interval-bound pairs. No random seed, real sample or research pixels were used. Historical artifacts are retained; the continuation checkpoint and curated GitHub backup identify the exact saved package.

## Decision sought

Approve or amend this validation architecture. Approval would enable its documented preparation/migration plan; it would not itself authorize imagery acquisition, the288-record draw, A/B, new-date processing or full-series production.
