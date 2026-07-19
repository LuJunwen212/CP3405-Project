# Team 2 — Sprint 7 Retrospective (W29)

**Date:** Sunday, 19 July 2026  
**Prepared by:** R2 — Scrum Master  
**Sprint:** Sprint 7 / `vW29`  
**Related evidence:** `standup_midweek_W29.md`

## 1. Retrospective Summary

Sprint 7 improved the team's Scrum process by making role status, dependencies, and blockers visible before the final weekend. The mandatory midweek check-in was completed on Wednesday, with every role reviewed individually and each blocker documented together with an R2 response action.

The main Sprint 7 risks were therefore surfaced by **Wednesday rather than Sunday**. Compared with the Sprint 6 Sunday-discovery pattern, the major risks became visible approximately **four days earlier**. This gave the team time to adjust schedules, clarify responsibilities, test workflows, replace unsuitable LLM models, and set recovery checkpoints before the release deadline.

However, one important issue still escaped the midweek process. On Sunday, R7 found that R5's Markdown technical report displayed `NaN` closing prices even though the JSON output contained valid values. This showed that a successful GitHub Actions run did not guarantee that every generated artefact was current, consistent, and ready for downstream use.

## 2. Did the Midweek Check-In Catch Anything?

Yes. The midweek check-in identified several specific risks rather than reporting that everyone was simply “on track.”

| Risk identified by Wednesday | R2 response | Outcome |
|---|---|---|
| R8 was scheduled before R4's final Macro output could be safely consumed. | Retained R4's Saturday schedule and moved R8 later in the pipeline. | The dependency order was protected without forcing R4 to use incomplete data. |
| R8 had not yet demonstrated a successful live API run and some models had free-tier or cost limitations. | Required live validation, accurate failure reporting, and use of workable models. | R8 resolved authentication and produced valid outputs from three models. |
| R9's release accountability was at risk after the previous release was missed. | Assigned a workflow-understanding task and set Friday, Saturday, and Sunday checkpoints. | R9 demonstrated a basic understanding of the selected workflow and had a clear release responsibility. |
| R10's implementation and evidence were incomplete, and final calibration depended on complete actual market data. | Required committed files, cumulative accuracy tracking, testing, and workflow validation before release. | The dependency was documented and treated as an integration constraint rather than hidden delay. |
| R7 could not start until upstream reports and R8 synthesis were available. | Tracked this as an expected dependency and monitored the upstream chain. | R7 was not incorrectly treated as late while waiting for required inputs. |

The check-in therefore achieved its main purpose: it made risks visible while there was still time to act.

## 3. Hardest Dependency to Manage

The hardest planned dependency was the timing between **R4 Macro and R8 LLM synthesis**.

R4 needed to run late enough to collect sufficiently complete macro and market information. Running R4 earlier would have reduced the quality of its output. However, R8 could not perform a valid synthesis until the upstream reports were available.

The resolution was to keep R4's existing schedule and move R8 later. This was preferable to asking R4 to produce an incomplete report merely to satisfy an earlier workflow time. The decision protected both the dependency order and the quality of the pipeline input.

The hardest unplanned dependency issue was the **R5-to-R7 artefact problem** on Sunday. R7 depended on the Markdown technical report, but the report contained `NaN` closing prices while the JSON values were valid. R5 reran the workflow on the agreed branch, after which the JSON, Markdown, charts, and presentation materials were updated.

## 4. What Went Well

- Every role was individually checked by Wednesday, and the result was committed in `standup_midweek_W29.md`.
- R3 completed the Almanac work early and produced the required CSV, JSON, and Markdown outputs.
- R4, R5, and R6 made strong technical progress and demonstrated working automation before the final scheduled runs.
- R8 resolved the API authentication blocker and replaced unsuitable models with workable alternatives.
- R9's release risk was identified before Sunday and converted into specific evidence-based checkpoints.
- R10 identified parser and file-format issues through testing with real project files.
- Blockers were usually recorded with an owner, response action, and next checkpoint rather than only being acknowledged.
- The R5 Sunday incident was investigated and resolved without invalidating the underlying numerical analysis.

## 5. What Did Not Go Well

- The team initially treated successful workflow execution as sufficient evidence that generated outputs were correct.
- R5's JSON and Markdown outputs were inconsistent, and different team members reviewed different branches or file versions.
- The R5 artefact problem was discovered on Sunday rather than during the midweek or synthesis gate.
- R9 required repeated clarification about GitHub Actions evidence and release responsibilities.
- R8's original model plan did not match the practical free-tier and cost constraints.
- R10's parser was vulnerable to changes in upstream prediction and actual-data formats.
- The project naming convention makes it difficult to distinguish the prediction creation week from the actual market week used for calibration.
- Several workflow dependencies were understood by individuals but were not enforced through automated validation.

## 6. Sprint 6 Comparison

In Sprint 6, the main failure pattern was that missing or blocked work became visible on Sunday, when downstream roles no longer had enough time to recover.

In Sprint 7, the main schedule, accountability, API, and integration risks were documented by Wednesday. This was approximately **four days earlier** than the Sprint 6 Sunday-discovery pattern.

The improvement was not that every issue disappeared. The improvement was that most issues became visible early enough for the team to make decisions before the release deadline.

The Sunday R5 incident also shows that the team has not fully solved the problem. Sprint 7 improved **status visibility**, but Sprint 8 must improve **artefact validity and branch consistency**.

## 7. One Process Change That Made the Difference

The most effective change was the **individual midweek role check combined with a written response action**.

Instead of using a general group message, each role was reviewed against four questions:

1. Has the role started?
2. What specific output will be delivered?
3. What dependency or blocker exists?
4. What action, owner, and deadline will resolve it?

The check-in was then committed as `standup_midweek_W29.md`, making the status and response actions visible to the whole team.

This process changed the Scrum Master's work from late reporting to early intervention.

## 8. Sprint 8 Improvement Actions

### Priority 1 — Add an artefact validation gate

Before R7 or R8 consumes an upstream report:

- compare key values between JSON and Markdown outputs;
- fail the workflow if required values are missing or `NaN`;
- confirm that all expected artefacts were modified by the latest run;
- confirm the agreed branch and latest commit;
- record the validation result in the GitHub Actions log.

**Owner:** R2 coordinates; each agent owner implements validation for their own output.  
**Checkpoint:** Before the downstream synthesis or review begins.

### Priority 2 — Standardise generated-file schemas

Define the required fields and naming rules for prediction, actual, calibration, and agent outputs. Parsers should validate the schema and produce a clear error when an upstream format changes.

**Owner:** R6, R7, R8, and R10, coordinated by R2.  
**Checkpoint:** Agreed during Sprint 8 planning.

### Priority 3 — Make the dependency gate explicit

R8 should not start the final synthesis until R3, R4, and R5 outputs have passed validation. R7 should confirm the exact branch and commit before beginning the Human Score review.

**Owner:** R2 monitors the gate; R8 and R7 confirm input readiness.  
**Checkpoint:** Before each downstream workflow starts.

### Priority 4 — Keep evidence-based accountability checkpoints

Roles with late or release-critical work should have a named deadline and required evidence, such as a commit, Actions run, generated file, or release link.

**Owner:** R2.  
**Checkpoint:** Midweek and before the final release.

## 9. Final R2 Assessment

Sprint 7 was a clear improvement over Sprint 6 because the main risks surfaced by Wednesday and were acted on before Sunday. The midweek check-in was useful and caught real schedule, accountability, API, and dependency problems.

The sprint also exposed the next process weakness: the team can no longer define “done” as only a green workflow or an existing output file. “Done” must mean that the correct artefacts were generated, validated, committed to the agreed branch, and confirmed usable by the next role.

**Sprint 7 retrospective conclusion:** The Scrum process improved from late blocker discovery to early risk control, but Sprint 8 must add automated artefact validation to prevent stale or inconsistent outputs from reaching downstream roles.
