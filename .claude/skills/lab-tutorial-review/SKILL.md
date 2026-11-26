---
name: lab-tutorial-review
description: Review a TD page in docs/ for exercise progression and self-checks, and propose changes ranked by effort against value. Use when asked to review, improve, or harden a tutorial page.
---

# Lab tutorial review

Follow the "Exercise style" rules in CLAUDE.md. This skill is the review process.

## 1. Read and run

- Read the whole TD and the repository or files that it uses.
- Run the commands that you can run locally, Docker included. Note each claim that you cannot check, and say so in the report.
- Look for factual errors: wrong file names, ports that do not match, outdated tools or models, and commands that fail.

## 2. Check each exercise

| Check | Question |
|---|---|
| Self-check | Does the student know when the step succeeded? |
| Predict | Is there a surprising result worth predicting first? |
| Load | Does one step bring in more than one new command or flag? |
| Fail first | Can the student see the problem before the solution? |
| Scaffolding | Is the full command given where only the goal would do? Remove commands only where a stuck student does not block the next steps. |
| Retrieval | Does the exercise reuse a skill from an earlier section or TD? |
| Section end | Does the section end with a question block? Do ungraded TDs end sections with `??? tip "Going further"`? Does a graded TD have "Send me your work" after the Recap? |
| Difficulty | Does each Challenge use `warning` for medium and `danger` for hard? |

## 3. Report before you edit

Group the findings by effort against value: "Do now", "Worth it later", and "Skip". Use a table: change, where (`file:line`), and why. List factual errors separately. Wait for approval.

## 4. Apply and prove

- Make the approved edits. Then run `uv run zensical build --strict`.
- Serve `site/` and check the changed sections in the browser, including the "On this page" sidebar.
- Commit and push only when the user asks.
