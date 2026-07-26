# Team 2 — Sprint 8 Retrospective (W30)

**Date:** Sunday, 26 July 2026  
**Prepared by:** R2 — Scrum Master  
**Sprint:** Sprint 8 / `vW30`  
**Related evidence:** `standup_midweek_W30.md`

## 1. Retrospective Summary

Sprint 8 focused on system hardening and minimizing human intervention. The sprint proceeded largely as planned, with major dependencies and technical formatting requirements (such as R8's plain text standardization) surfaced and addressed by the Wednesday mid-week check-in.

However, a critical unplanned technical blocker surfaced on Saturday morning: R5's automated code execution failed due to a `NameError`. Because the team was actively monitoring the scheduled runs, R1 (Zaikun Zheng) and R2 (Guanyu Lu) were able to immediately identify and resolve the issue within under two hours, preventing a cascading failure for downstream roles (R8, R7, and R9). This demonstrated a significant improvement in the team's incident response and pipeline recovery capabilities.

## 2. Did the Midweek Check-In Catch Anything?

Yes. The midweek check-in successfully identified an integration requirement before the weekend synthesis gate.

| Risk identified by Wednesday | R2 response | Outcome |
| --- | --- | --- |
| R8 needed to standardize the output format of the large language model and make the output in plain text. | R8 updated the code, but because R8 depends on the final upstream agent reports, R2 noted that the team needed to wait until Saturday to check the results.  | The requirement was logged early, ensuring R8's code was ready to consume upstream reports once generated. |
| Some sources for R4 Macro did not provide stable or accessible automated data.  | Accepted manual exclusion or fallback handling for unstable sources because this is consistent with the agreed DoD.  | Prevented the pipeline from failing due to known external data instability. |
| R7 was waiting on planned dependencies (R3, R4, R5, R6, and R8 outputs).  | Recorded this as an expected dependency rather than a performance delay, with R2 confirming R8's output would be available in time.  | R7's schedule was protected and properly sequenced. |

The check-in therefore achieved its main purpose: it made risks visible while there was still time to act.

## 3. Hardest Dependency to Manage

The hardest planned dependency remains the strict pipeline execution order: `R3 Almanac + R4 Macro + R5 Technical → R8 LLM Synthesis → R7 Human Score → R9 Release`. R8 could not validate its plain text standardization until Saturday because it depended entirely on the final upstream agent reports.

The hardest **unplanned** dependency was the sudden failure of the R5 Technical workflow on Saturday morning. At 9:30 AM, R2 (Guanyu Lu) discovered the R5 code execution automated run failed with a `FATAL: NameError: name 'normalize_week' is not defined`. This immediately blocked R8's synthesis. Because R1 (Zaikun Zheng) and R2 (Guanyu Lu) intervened, the code was successfully repaired and the automation executed by 11:10 AM, allowing the rest of the dependency chain to proceed without collapsing into Sunday.

## 4. What Went Well

* All roles were checked individually by Wednesday, and everyone was highly cooperative.
* R3 completed all tasks ahead of schedule, including standardizing file generation locations, adding strict report validation, and updating documentation.
* R4 successfully implemented its script to collect data from public macroeconomic, market, Treasury, labour, and news sources, complete with retry handling and structured error handling.
* R5 accomplished fixing and validating its code and forced workflow failures on `NaN` values, effectively fulfilling its W30 Sprint Goal tasks.
* R6 successfully updated the GitHub Actions workflow, integrating the role number into the workflow name and adding support for manual year overrides alongside minor optimizations. These updates were tested and functioned exactly as expected.
* R8 standardizes the output format for all large language models, automatically converts the output results into plain text, and successfully generated reports automatically on Saturday.

* **Incident Response:** When the R2 detected R5 automation failed on Saturday at 9:30 AM, R1 and R2 caught the error instantly, debugged it, and restored the automated pipeline by 11:10 AM.

## 5. What Did Not Go Well

* **The "Works on My Machine" Gap:** There was a critical discrepancy in R5's environment testing. R5 successfully modified the code and executed the pipeline to produce results on Tuesday night. However, when the automated GitHub Actions workflow triggered on Saturday morning, it threw a `FATAL: NameError: name 'normalize_week' is not defined`.
* Because R8's final output validation relied on the live weekend run, the Saturday morning R5 failure created a brief bottleneck that temporarily delayed R8 and R7.



## 6. Blockers Timeline (Sprint 7 Comparison)

**When did blockers surface this sprint?**
* *Planned/Integration Blockers:* Surfaced on **Wednesday** (e.g., R8's output standardization and R4's unstable data sources).

* *Technical/Execution Blockers:* Surfaced on **Saturday** (R5 `NameError`).

**How many days earlier than Sprint 7?**

In Sprint 7, major schedule and integration risks were successfully pulled forward to Wednesday (four days earlier than Sprint 6). In Sprint 8, we maintained this Wednesday visibility for planned work. However, the unexpected R5 execution bug surfaced on Saturday. The critical difference this sprint was the *resolution speed*. Instead of an issue lingering until Sunday, the Saturday blocker was detected and fixed in **100 minutes**, proving the team is actively monitoring the automated runs.



## 7. One Process Change That Made the Difference

The most effective process change this sprint was **active weekend workflow monitoring by leadership (R1 and R2)**.

By actively watching the execution on Saturday morning, the team caught the R5 `NameError` at 9:30 AM and deployed a patch by 11:10 AM. This immediate triage is what prevented a single failed step from collapsing the entire sprint into Sunday night.

## 8. Sprint 9 Improvement Actions (Demo Prep)

### Priority 1 — Eliminate the Local-to-Production Discrepancy

Code that runs successfully on Tuesday night on week9 branch must be proven to run in the automated GitHub Actions environment *before* the weekend.

**Owner:** All Agent Operators.

**Checkpoint:** Ensure test runs mirror the exact production environment.

### Priority 2 — Finalize Demo Day Role Assignments

As Sprint 9 is the final sprint, every team member must have their presentation segments assigned and rehearsed.

**Owner:** R2.

**Checkpoint:** Monday Sprint Review.

## 9. Final R2 Assessment

Sprint 8 successfully tested our system hardening. While the pipeline did experience a failure (R5's `NameError`), the team did not panic, and we did not bypass the system to manually patch data files. Instead, R1 and R2 fixed the code and re-ran the automation successfully. The mid-week check-ins continue to effectively manage dependencies, and our weekend incident response has dramatically improved. We are well-positioned for the final Sprint 9 and Demo Day.

**Sprint 8 retrospective conclusion**: The Scrum process improved from passive weekend execution to active monitoring and rapid incident recovery, but Sprint 9 must eliminate the local-to-production discrepancy to prevent "works on my machine" errors from disrupting the final automated pipeline.
