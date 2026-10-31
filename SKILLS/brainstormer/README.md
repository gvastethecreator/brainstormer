# brainstormer · v1.1.0

A skill to explore new product capabilities with concrete proposals,
conversation, and small prototypes. **It is not an audit, a detail grill,
a planner, or an implementation agent.**

## Install

Copy the whole `brainstormer/` folder into the skills directory that your
agent discovers. Do not copy only `SKILL.md`: its references, templates, and helper are part
of the package. As a project location, you can use `.agents/skills/brainstormer/`
when your environment supports that directory. Other hosts need another path; the
package format does not imply universal automatic discovery.

Installing the skill and its files is a different action from running a
session. **Session results go in `.scratch/brainstorming/`**, unless the repository requires an artifact path; never
inside the skill folder. This package does not modify or install anything in a
remote repository automatically.

## Recommended invocation

```text
Use the brainstormer skill in this project.
Analyze what it does, which capabilities it has, and which ideas we explored before.
Propose a first round of new, substantial features that fit the
product. Prepare an idea record and a standalone interactive HTML file per option in
.scratch/brainstorming. I want to explore possibilities; do not implement changes,
do not generate tickets, and do not build an execution plan yet.
```

For a specific round:

```text
Use brainstormer, but dedicate this round to new effects.
Each option must be a distinct effect, explained with a concrete use and a
prototype that lets me observe its behavior. Avoid presets of what already exists.
```

To resume:

```text
Resume our last brainstormer session. Read the saved ideas and decisions.
Show me where we left off and let's continue with new options, without repeating discards
or turning favorites into tasks.
```

These are natural-language requests. A host can also offer its own
syntax to invoke skills; no universal command is assumed.

## What happens during a session

The agent understands the product and checks it against what exists. For a full session, it opens a folder; a round requested only in chat creates no files.
It generates a manageable round that respects the requested count, with standalone demos when they are part of the request.
You try, combine, keep, discard, or ask for new rounds. What remains is idea records,
prototypes, and decisions; not a roadmap. You do not need to pick a single idea.

An example conversation is: "Let's save I001 and I004; I002 does not fit. Let's make a
variant of I003 and then show me more input sources". This keeps ideas,
records the discard, and keeps the exploration open. It does not authorize building anything.

## What the folder includes

| File | Purpose |
| --- | --- |
| `LICENSE` | MIT notice that must accompany the portable copy. |
| `SKILL.md` | Instructions that the agent loads; compact core instructions. |
| `references/session-contract.md` | Evidence, persistence, statuses, rounds, and helper. |
| `references/feature-filter.md` | Novelty threshold, concrete value, and round selection. |
| `references/prototype-contract.md` | Interactivity, honest simulation, and testing. |
| `assets/idea.schema.json` | Schema of the input idea record. |
| `assets/idea-input.example.json` | Editable example, not an already validated idea. |
| `assets/prototype-template.html` | Skeleton marked as incomplete, not an approvable demo. |
| `scripts/session.py` | Optional helper for files, IDs, decisions, revisions, and index. |
| `tests/test_session.py` | Unit tests for the helper. |
| `evals/evals.json` | Conversational evaluation cases; not run with agents in this release. |

The helper needs Python 3.10+ and its standard library. The instructions can
be used without Python by writing the same structure manually. No part of the
skill requires a frontend framework, AI provider, paid service, or server.

## Test the helper

From the `brainstormer/` folder:

```sh
python -m unittest discover -s tests -v
python scripts/session.py --help
```

The session commands are described in `references/session-contract.md`.
The script does not inspect repositories, generate ideas, or assess value: it automates
lab maintenance. It rejects escape paths and symlinks under its write
zone, but **it is not a sandbox for untrusted JavaScript**.

## Evaluate the agent's behavior

`evals/evals.json` contains positive cases, negative cases, and authorization limits.
Try each case in isolated sessions, with fixtures or test repositories, and compare
the behavior with and without the skill. Observe the real writes and the demos,
not only the agent's claim that it followed the rules. Do not use these evaluations to
modify a production repository.

The suite checks the helper. The HTML template is incomplete on purpose and does not demonstrate a working prototype. File tests are not equivalent to an evaluation of the skill with agents; record any real run separately.

## Design references

Format: Agent Skills, official specification (`https://agentskills.io/specification`).
Triggerable description, compact instructions, and on-demand references:
`https://agentskills.io/skill-creation/best-practices`.
Separation between artifact tests and agent evaluation:
`https://agentskills.io/skill-creation/evaluating-skills`.

The name, frontmatter, and structure follow that open format. Loading and
specific permissions depend on the host where you install it.
