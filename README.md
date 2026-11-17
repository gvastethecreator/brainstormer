# Brainstormer

Agent Skill for product feature discovery. It turns ideas into small interactive prototypes the user can try, keep, or discard. **It is not an audit, a detail grill, a planner, or an implementation agent.**

The operating skill is written in English. Session files go in `.scratch/brainstorming/`, not inside this package.

## Quick start

```text
npx skills add gvastethecreator/brainstormer
```

Or copy the whole `SKILLS/brainstormer` folder into the skill directory your agent already loads. Do not copy only `SKILL.md`: its references, templates, `scripts/session.py` and `LICENSE` are part of the package. A project location such as `.agents/skills/brainstormer/` works when your host discovers that directory; the package format does not imply universal automatic discovery.

Installing the skill is a different action from running a session. Session results go in `.scratch/brainstorming/` unless the repository requires another artifact path, never inside the skill folder.

Optional helper: Python 3.10+ and the standard library.

```text
python <skill-root>/scripts/session.py --help
python -m unittest discover -s <skill-root>/tests -v
```

The helper automates lab maintenance: files, IDs, decisions, revisions and the index. It does not inspect repositories, generate ideas or assess value. It rejects escape paths and symlinks under its write zone, but **it is not a sandbox for untrusted JavaScript**. Commands are in [session-contract.md](SKILLS/brainstormer/references/session-contract.md).

## Example requests

```text
Use the brainstormer skill in this project.
Analyze what it does, which capabilities it has, and which ideas we explored before.
Propose a first round of new, substantial features that fit the product.
Prepare an idea record and a standalone interactive HTML file per option in
.scratch/brainstorming. Do not implement changes, generate tickets, or build an execution plan yet.
```

```text
Use brainstormer, but dedicate this round to new effects.
Each option must be a distinct effect with a concrete use and a prototype
that lets me observe its behavior. Avoid presets of what already exists.
```

```text
Resume our last brainstormer session. Read the saved ideas and decisions,
show me where we left off, and continue with new options without repeating
discards or turning favorites into tasks.
```

A reply such as "Save I001 and I004; I002 does not fit. Make a variant of I003, then show me more input sources" keeps ideas, records the discard and keeps the exploration open. It does not authorize building anything.

## Package contents

| File | Purpose |
| --- | --- |
| `SKILL.md` | Operating contract the agent loads. |
| `references/session-contract.md` | Evidence, persistence, statuses, rounds and helper commands. |
| `references/feature-filter.md` | Novelty threshold, concrete value and round selection. |
| `references/prototype-contract.md` | Interactivity, honest simulation and testing. |
| `assets/idea.schema.json` | Schema of the input idea record. |
| `assets/idea-input.example.json` | Editable example, not a validated idea. |
| `assets/prototype-template.html` | Skeleton marked incomplete, not an approvable demo. |
| `scripts/session.py` | Optional helper for files, IDs, decisions, revisions and index. |
| `tests/test_session.py` | Unit tests for the helper. |
| `evals/evals.json` | Conversational evaluation cases: positive, negative and authorization limits. |
| `LICENSE` | MIT notice that must accompany the portable copy. |

## Evaluating behavior

Run each case in `evals/evals.json` in an isolated session with fixtures or a test repository, and compare behavior with and without the skill. Observe real writes and demos, not only the agent's claim. The unit tests cover the helper only; they are not an evaluation of the skill with agents.

Format: [Agent Skills specification](https://agentskills.io/specification).

License: [MIT](LICENSE).
