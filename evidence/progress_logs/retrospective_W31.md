# Team 2 — Sprint 9 Retrospective (W31)

**Date:** Sunday, 2 August 2026  
**Prepared by:** R2 — Scrum Master  
**Sprint:** Sprint 9 / `vW31`  
**Related evidence:** `standup_midweek_W31.md`

---

## 1. Retrospective Summary

Sprint 9 (our final sprint) focused on complete code and report reproducibility, streamlining deliverables with visual evidence, and building a front-end interface. The sprint proceeded much better than expected. The major dependencies and external data risks were surfaced and addressed by the Wednesday mid-week check-in.

A significant highlight of this sprint was the proactive testing and development phase. R1 overfulfilled expectations by successfully building a front-end web page (dashboard) to finalize the entire project, complete with an automatic update system scheduled for Sunday at 4:00 PM. Additionally, roles like R8 and R10 completed their automated testing as early as Wednesday, drastically reducing the weekend pressure that we experienced in Sprint 8.

---

## 2. Did the Midweek Check-In Catch Anything?

Yes. The midweek check-in successfully identified workflow uncertainties and mapped out a strict tracking plan for the weekend.

| Risk identified by Wednesday | R2 response | Outcome |
|---|---|---|
| R4 stated it was impossible to determine in advance whether the automated data from unstable macroeconomic sources could be achieved before Saturday. | R2 accepted manual exclusion or fallback handling for unstable sources (per DoD) and committed to tracking the automation live on Saturday. | Prevented the pipeline from stalling due to known external data instability, with a clear fallback plan in place. |
| R5 experienced a NameError crash last Saturday (W30). A check was required to ensure results would generate as scheduled this week. | R2 set a strict action plan to focus on observing R5's automated generation on Saturday and resolving any issues promptly. | Ensured leadership was on standby to intercept any potential local-to-production discrepancies. |
| R7 was waiting on planned dependencies (R3, R4, R5, R6, and R8 outputs). | Recorded this as an expected dependency, with R2 confirming R8's output would be available in time. | R7's schedule was protected and properly sequenced. |

The check-in achieved its purpose by transitioning the team from passive waiting to active monitoring for our most vulnerable pipeline stages.

---

## 3. Hardest Dependency to Manage

The hardest planned dependency remained the strict pipeline execution order:

**R3 Almanac + R4 Macro + R5 Technical → R8 LLM Synthesis → R7 Human Score → R9 Release**

However, Sprint 9 introduced a new final dependency: **The Front-End Dashboard Integration**. Because R1 set up an automatic update system scheduled to trigger on Sunday at 4:00 PM to update the data for the current week, all upstream data fetching, technical chart generation (leveraging Markdown image support), and LLM synthesis had to be entirely error-free and reproducible before this Sunday deadline.

---

## 4. What Went Well

- All roles were checked individually by Wednesday, and everyone was highly cooperative. The overall status was marked as *"Much better than expected"*.
- **R1** successfully built the front-end web pages and configured the Sunday 4:00 PM automatic update system, overfulfilling the role's requirements.
- **R3** completed all tasks ahead of schedule, updated the W31 cron schedule, and provided valuable suggestions for the dashboard's construction.
- **R8 and R10** successfully completed their automated tests and generated reports by Wednesday, moving their validation entirely out of the weekend bottleneck.
- Visual evidence (such as R5 technical charts) was successfully embedded into the documentation files to streamline the final deliverables.
- **R6** successfully tested the Python script and GitHub Actions workflow, verifying the JSON output, automatic Markdown report generation, and provided valuable suggestions for the dashboard's construction.

---

## 5. What Did Not Go Well

- **Inherent Data Instability:** R4's macroeconomic data sources remain inherently unstable. The team has to continuously rely on fallback handling and cannot fully guarantee automated data extraction for certain sources until the script actually runs on Saturday.
- Because Sprint 9 required comprehensive presentation prep and building a unified dashboard, coordinating the final visual deliverables across all 10 roles required heavy communication overhead right before the weekend.

---

## 6. Blockers Timeline (Sprint 8 Comparison)

**When did blockers surface this sprint?**  
Planned/Integration Risks: Surfaced on Wednesday (e.g., R4's unstable data sources).

**How does this compare to Sprint 8?**  
In Sprint 8, we experienced a critical execution blocker on Saturday morning (the 9:30 AM R5 NameError). In Sprint 9, roles like R8 and R10 eliminated their weekend execution risk entirely by successfully completing automated testing on Wednesday. This forward-loaded testing meant the weekend execution was much smoother and significantly less stressful than Sprint 8.

---

## 7. One Process Change That Made the Difference

The most effective process change this sprint was **mid-week automated testing in the production environment**.

By having R8 and R10 complete their automated tests on Wednesday, the team directly addressed Priority 1 from last week's retrospective (*"Eliminate the Local-to-Production Discrepancy"*). Proving the code ran in the automated environment before the weekend was the exact change needed to prevent a repeat of W30's Saturday crash.

---

## 8. Demo Day & Final Release Preparation

As this is the final sprint, our improvement actions transition into final delivery preparations:

### Priority 1 — Verify Complete Reproducibility
Every role must independently verify that their scripts can be re-run from scratch and that the generated reports are error-free and up-to-date.  
**Owner:** All Agent Operators.  
**Checkpoint:** Before R9 tags the final vW31 release.

### Priority 2 — Finalize Presentations
Consolidate role evidence, calibration findings, and technical reports into a polished, professional presentation ready for Sprint Day delivery.  
**Owner:** R2.  
**Checkpoint:** Monday Sprint Review.

---

## 9. Final R2 Assessment

Sprint 9 successfully concluded our system's development. The team successfully streamlined deliverables, embedded visual evidence into our documentation, and deployed a functional front-end dashboard. By moving automated testing to Wednesday for several roles, we eliminated the weekend bottleneck that plagued Sprint 8. The mid-week check-ins effectively managed our final dependencies, and our pipeline is now hardened, reproducible, and fully integrated. **We are completely prepared for Demo Day on Monday.**
