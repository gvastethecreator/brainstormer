---
name: brainstormer
license: MIT
description: "Product feature discovery. Use to explore new capabilities in an existing project with concrete ideas and small interactive prototypes."
compatibility: "Full sessions need project reads and local writes. Offline HTML previews use a browser; the optional helper needs Python 3.10+ and its standard library."
metadata:
  version: "1.1.0"
  language: en
---

# Brainstormer

Explore which new capabilities are worth adding to a product. Turn the ideas into small experiences that the user can try, compare, keep, or discard. Use the user's language and keep technical identifiers.

## Contract

- A feature enables a new outcome, flow, or expressive possibility for a specific person. Novelty depends on what it lets someone do, not on code size.
- Each option describes one specific capability. "More effects" is a category; each proposed effect needs its own behavior, use, and demo.
- A full session writes to `.scratch/brainstorming/`. Demo code is authorized; integrating the idea into the product, changing configuration, or creating tickets requires a request for that action.
- "I like it", "save it", or "let's go deeper" keep the exploration going. If the user asks to plan or implement, close the session record and continue under that new scope, reusing the authorization that request gives.
- If the user asks for ideas only or for an answer in chat, deliver that round without creating a lab or required prototypes. If they ask to save the ideas, keep idea records with the prototype omission documented.

Respect the repository's paths. Browser screenshots use the repository's screenshot folder, separate from the demos; keep durable proof only when it is needed. If the repo requires another owner for prototypes, use it and link to it from the session. The helper supports its fixed structure: in another structure, keep the session record manually.

## Process

### 1. Understand the product and what was already explored

Read the rules, purpose, audience, main journey, and constraints. Review the relevant capability registries, commands, inputs/outputs, screens, or handlers, together with docs and tests. Start with the indexes and idea records of previous sessions; open only the prototypes you need for comparison.

Distinguish implemented, partial, documented, pending, and uncertain. A file name, a dependency, or an empty search does not prove a capability or its absence. Widen the inspection only to check a candidate. With incomplete access, present hypotheses and name the scope you reviewed.

**Done when:** there is a short summary of the product, evidence of its capabilities, and the access limits. Ask only if a missing decision substantially changes the value of the proposals.

### 2. Open or resume the session, when it applies

For a persistent session, read [session-contract.md](references/session-contract.md). Create a new folder or resume the requested one, and keep its IDs, decisions, and revisions. Record the goal, inspected scope, sources, and assumptions in `context.md`.

The [session.py](scripts/session.py) helper assigns IDs and maintains files; it does not inspect the product or decide novelty. Resolve `<skill-root>` to the installed folder and check `python <skill-root>/scripts/session.py --help`. Write briefs and plans with concrete actions, short sentences, and consistent terms; keep the artifact's language, the commands, and the uncertainty. No other skills are required.

**Done when:** the session has enough context to be resumed. For a chat-only round, skip this step. Without write access, deliver the ideas and say so; offer files only if the tool can create them.

### 3. Filter candidates

Consider new inputs, transformations, temporal behavior, composition, outputs, reuse, and adjacent domains. These are search lenses, not quotas or reasons to add AI or collaboration by reflex.

Keep a candidate if it has a concrete user and situation, a new outcome, fit with the product, a difference from what exists, and a hypothesis that someone can try out. Consult [feature-filter.md](references/feature-filter.md) when the threshold is unclear.

Choose a varied, manageable round that respects the requested count. If there are not enough solid ideas, explain the limit instead of padding with duplicates. Bugs, refactors, and cosmetic tweaks can be relevant, but they do not replace the search for new capabilities. Do not invent demand, ROI, or feasibility.

**Done when:** each option has a value and a difference that you can explain, and the round offers real alternatives.

### 4. Make each proposal hands-on

In a session with demos, read [prototype-contract.md](references/prototype-contract.md) before you build. Prepare one idea record and one standalone HTML file per option, with one interaction that changes the core result and a reset. Use synthetic data or authorized fixtures, and label what is real, approximate, and simulated.

Prefer self-contained, offline HTML. A CLI can be represented by a simulated terminal with limited commands; never run a real shell from the demo. An incomplete template does not count as a prototype.

When you close the round, open each demo and check its main control, reset, and links; review the console and network with the available browser. A screenshot proves a visual state, not the interaction. Without a browser, record `not-run` and explain what remains unchecked.

**Done when:** each proposal has a usable demo and evidence of what was tested, or an omission that the user requested or that a real limitation caused.

### 5. Present and continue the exploration

Show the short summary of the project and, per idea: the ID if it is saved, name, new outcome, difference from what exists, uncertainty, and a real link to the demo when one exists. Ask for one light decision about the round; do not force the user to pick a favorite or to approve the whole batch.

Use the reactions to explore, save, discard, vary, or combine. "More options" opens another round. Avoid questionnaires about architecture, schedules, or technical details that do not change the experience yet.

**Done when:** the options can be compared and the user understands which decision is open.

### 6. Keep the decisions

`idea.json` is canonical; `session.json` keeps the IDs and history. `brief.md`, `session.md`, and `index.html` are derived views. The index supports navigation and filtering: it does not promise to write decisions to disk from the browser.

The statuses are `proposed`, `exploring`, `saved`, `parked`, and `discarded`. `saved` keeps a possibility; it does not commit to building it. Record only expressed decisions: silence leaves the status unchanged.

A variant or combination uses a new ID with `parent_ids`; a refinement keeps the ID and saves the previous revision. Update the views from the records. Read the session contract for the commands and for recovery from mismatches.

**Done when:** idea records, demos, index, and decisions match, or the chat answer makes clear what was proposed without persisting it. Close with what was kept, the uncertainty, and the pending checks, without adding a roadmap on your own initiative.
