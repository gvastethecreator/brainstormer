# Session contract

This contract applies to persistent sessions. A round requested only in chat can skip files. Use the artifact path that the repository requires; the helper supports only `.scratch/brainstorming/`, so another structure requires manual maintenance.

## Sources and evidence

A source must identify a file/range, symbol, test, document, or
user instruction that was actually read. Save the version reference if it is
verified. Never turn memories, a tree SHA, or a partially read branch
into an audit of the latest commit.

Use three possible results for novelty:

- `not-found-in-inspected-scope`: it did not appear in the documented scope; it does not prove absolute absence.
- `distinct-extension`: it builds on something existing, but enables a new outcome; describe the difference.
- `unknown`: an exploratory proposal whose absence is not verified yet.

Confidence `low`, `medium`, or `high` expresses confidence in that assessment, not commercial
success or guaranteed feasibility. With documentation only or failed access,
`unknown` and confidence `low` usually apply.

A partial implementation is existing work, not a brand-new idea. You can explore
a new outcome on top of it, but identify the existing part and the difference.
Do not infer demand, revenue, "10×", development time, or performance without data.

## Files and consistency

- `context.md`: written by the agent; scope, product, rules, evidence, limits,
  link to previous sessions. The helper does not overwrite it when it renders.
- `session.json`: identifier, project, dates, title, IDs, and action history.
- `ideas/I001/idea.json`: canonical idea record, status, and decision notes.
- `ideas/I001/prototype.html`: current demo, unless there is an explicit, justified omission.
- `ideas/I001/revisions/r001/`: previous idea record and demo when the same idea is refined.
- `brief.md`, `session.md`, and `index.html`: regenerable views. Do not edit only one view.

The helper is designed for **one writer per session**. File writes
are individually atomic; they are not a multi-file transaction or a
sync system. Do not use two agents that write to the same session at the same time.

Do not put secrets, tokens, real personal data, or unnecessary private content
in the lab: it could end up in a public repository. Do not change `.gitignore`
on your own. When you share a ZIP, review the data first.

## Open a session with the optional helper

Replace `<skill>` and `<project>` with real paths. On Windows, you can use `py -3`
instead of `python`, depending on the available installation.

```sh
python <skill>/scripts/session.py init --root <project> --name my-project --title "Explore new capabilities"
```

The command prints a session ID and its path; use that ID literally in the other
commands. Fill in `context.md` first. Do not claim that the helper inspected the repo.

Build the input idea record from `assets/idea-input.example.json` and the schema
`assets/idea.schema.json`. Create an authentic HTML file, based on
`assets/prototype-template.html` if that is useful; remove the template marker **only after**
you implement the interaction that tests the idea.

Also create these drafts inside the session itself, for example in `drafts/`.
Do not use the skill directory as a workspace.

```sh
python <skill>/scripts/session.py add --root <project> --session <id> --idea <draft-path.json> --prototype <demo-path.html>
python <skill>/scripts/session.py decide --root <project> --session <id> --id I001 --status saved --reason "The user wants to keep this possibility because…"
python <skill>/scripts/session.py revise --root <project> --session <id> --id I001 --idea <draft-path.json> --prototype <demo-path.html> --reason "Requested comparison of two behaviors"
python <skill>/scripts/session.py render --root <project> --session <id>
python <skill>/scripts/session.py validate --root <project> --session <id>
```

Omitting a prototype requires `prototype.mode = "omitted"`, an explicit
limitation in the idea record, and `--omit-prototype "reason"` instead of `--prototype`. Use it
only at the user's request or for a real limitation, never to hide pending work.

The helper checks shape, paths, statuses, IDs, and some basic HTML errors.
**It does not certify** relevance, novelty, visual quality, JavaScript safety, or that
an interaction makes sense. HTML is code: review it before you open third-party
material. The agent must do those checks separately.

## Idea record

Input fields (without IDs or dates, which the helper assigns):

| Field | Content |
| --- | --- |
| `title` | Name of a single capability, not a generic topic. |
| `category` | A category that is useful for this project, with no mandatory rigid taxonomy. |
| `pitch` | Short explanation of what someone could now do. |
| `user_value` | Person, situation, and concrete benefit. |
| `use_case` | An observable before/after journey, not a slogan. |
| `novelty_delta` | Difference from existing capabilities, or a statement of hypothesis. |
| `evidence` | List of `{kind, source, finding}`; it can be empty only if uncertainty is declared. |
| `novelty` | `{assessment, confidence, inspected_scope, uncertainty}`. |
| `prototype` | `{mode, question, observable, limitations, checks}`. |
| `open_question` | A product uncertainty that is worth observing, not a technical list. |
| `parent_ids` | Existing IDs that produced a variant or combination; usually an empty list. |

`evidence.kind`: `code`, `test`, `documentation`, `user`, or `hypothesis`.
`prototype.mode`: `working-slice`, `approximation`, `simulation`, or `omitted`.
`checks`: list of `{check, result}`, with `result` = `passed`, `failed`, or `not-run`.
Record what was actually tested, without turning static validation into browser testing.

The final idea record adds `id`, `status`, `created_at`, `updated_at`, `revision`,
`decision_reason`, and `prototype_path`. Do not blindly copy those fields when you create
a new idea. `parent_ids` lets you trace lineage, not priority or dependency.

## Interaction between rounds

A useful first answer can have this shape:

"The project already supports A and B; I am still uncertain about C. This round
explores new outcomes, not adjustments to those controls.

**I001 — Concrete feature.** It would enable X for Y. It differs from A in Z.
[Local demo].

**I002 — Another concrete feature.** ...

Which ones would you explore and which would you discard?"

Do not present links before you create the files. Do not ask the user to pick a single idea
if they are interested in several. For "more", propose another round without requiring them to close
the previous one. For "go deeper into I002", use a comparative demo or a variant and a
question focused on the experience; do not drift into an architecture design.

## Decisions and closing

Silence keeps `proposed`. A request to go deeper allows `exploring`.
`Saved`, `parked`, and `discarded` need a user reaction, not your preference.
Moving back from any status is allowed with an explicit decision and traceability.

When you resume, read both the saved ideas and the discards and their reasons.
You can return to a discarded idea if the user asks for it or important new evidence
appears, but announce the reason and its relation to the previous idea.

Do not create tasks because the session closes. The output is: kept ideas, prototypes,
decisions, and open questions. If the user later asks to plan an idea, keep that
request separate from discovery mode. If they ask to implement it, verify the explicit
scope: the rest of the ideas remain unauthorized.

## Continuity summary

When a round ends, keep in the context: the explored topic, explicit reactions,
ideas that are still undecided, and areas that the user asked to explore later. These are
conversation notes, not tasks. Do not carry constraints that are specific to one project into
another without evidence. To refer to ideas from another session, use their full session and ID.

Interpret "go ahead", "let's continue", and "I like it" within the scope already authorized. On their own,
they do not turn an exploration into an implementation. A plan request changes the stage
and keeps its limit; an implementation authorization allows you to continue without
asking for it again. Neither favorites nor index filters represent permissions.
