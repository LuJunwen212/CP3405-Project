# Sprint 8 Goal — W30

Deliver a reliable, clean, and properly synchronized W30 forecasting pipeline covering SPX, NDX, IWM, and all 11 S&P 500 sector ETFs.

Building on Sprint 7 lessons, the team will complete the following key tasks for W30:

1. **Check R8 and R7 Logical Conflicts**: Identify and fix any logical contradictions between R8 LLM synthesis and R7 Human Scoring, and find the root causes.
2. **Improve R9 Automation**: Further enhance and complete R9 repository merging, release packaging, and tagging automation.
3. **Fix and Validate R5 Code**: Update and improve R5 automation code to verify actual JSON and Markdown values, find any root cause of calculation issues, and ensure full data accuracy before downstream processing.
4. **Organize Output Folder Structure**: Systematically reorganize project files by creating and assigning a dedicated directory for each role (e.g., `outputs/R3/`, `outputs/R4/`, `outputs/R5/`, etc.).
5. **Force Workflow Failures on NaN Values**: Update GitHub Actions and verification scripts so that any detected `NaN` or invalid data strictly fails the workflow instead of publishing bad output files.

The team should automate as much of the workflow as possible. Where full automation cannot be achieved, each responsible role must implement partial automation where feasible and manually complete the remaining work before the required deadline. Technical limitations or automation failures must not result in missing deliverables.

R2 must conduct the mandatory midweek check-in by Wednesday to confirm that every role has started its work, role folders are structured, identify blockers, and take appropriate action before they become end-of-Sprint problems.

## Team Schedule and Role Deadlines

- **R6 (Hamzah Nutt)**: Saturday 2:00 PM (Market Data)
- **R3 (The Bao Le)**: Saturday 4:00 PM (Almanac)
- **R4 (Hu Wenhan)**: Saturday 4:00 PM (Macro)
- **R5 (Yuchu Lin)**: Saturday 4:00 PM (Technical)
- **R10 (Wang Hao)**: Saturday 6:00 PM (Confirm R6 outputs) + Sunday 1:00 PM (Calibration)
- **R8 (Kan Yijie)**: Saturday 7:00 PM (Confirm R3, R4, R5 outputs) + Sunday 1:00 PM (LLMs)
- **R7 (Swan Htet Zaw)**: Sunday 3:30 PM (Human Score + Prediction)
- **R1 (Zheng Zaikun)**: Sunday 5:30 PM (Prediction Review) + Sunday 8:30 PM (Discord Submission)
- **R2 (Guanyu Lu & Qinyang Wu)**: Sunday 7:00 PM (Final DoD check + Retrospective)
- **R9 (Junwen Lu)**: Sunday 8:00 PM (Tag and Release)

Sprint success means that blockers are identified early, output files are neatly organized into role folders, code issues in R5 and R9 are resolved, `NaN` errors fail the workflow immediately, and all required deliverables are submitted before their deadlines.
