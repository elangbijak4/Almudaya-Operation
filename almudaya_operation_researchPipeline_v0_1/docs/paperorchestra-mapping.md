# PaperOrchestra → Almudaya Operation mapping

Source: Song et al., *PaperOrchestra: A Multi-Agent Framework for Automated AI Research Paper Writing*, arXiv:2604.05018v1 (2026), especially Section 4 and Appendix A–B.

| PaperOrchestra construct | Almudaya representation |
|---|---|
| Outline Agent | `research_planner` role |
| Plotting Agent | `visualization_specialist` role |
| Literature Review Agent | `literature_specialist` role |
| Semantic Scholar citation matching | `bibliographic_verifier` resource adapter / `citation_verifier` role |
| Section Writing Agent | `manuscript_writer` role |
| Content Refinement Agent | `quality_refiner` role |
| PaperBanana visual critique | optional diagram-generation and VLM-critique resource adapters |
| AgentReview | optional manuscript-evaluation adapter |
| Step 2 and Step 3 parallelism | workflow parallel branch |
| Plot critique and redraw | bounded nested feedback loop |
| Content refinement acceptance/rollback | OBS predicate + versioned artifact rollback |
| LaTeX and PDF outputs | output contract |

## Generalization boundary

The Operation expresses the observable organizational pattern and control policies. It does not embed PaperOrchestra's exact prompts, internal implementation, proprietary service configuration, or experimental benchmark setup. Vendors can be replaced by compatible resource adapters without changing the mission structure.
