# Prototype contract

## What each HTML file must demonstrate

One product question per demo: "How would the outcome change with this capability?".
There must be an interaction that affects its core result, not only the interface.
Include a useful initial state, labeled controls, a visible output, a reset, and
a readable note about reality/simulation. A demo can be very small.

Guiding cases:

| Project | Minimum useful experience |
| --- | --- |
| Effects editor | Synthetic/allowed input, a visible effect, and a control that changes its behavior. |
| Animation | Playback, pause, scrub or time comparison, and reset. |
| Exporter | Configure a sample, see the output, and generate a small real file or declare the format simulated. |
| CLI | Simulated terminal with allowed commands, state change, and synthetic output; no real execution. |
| API/service | Input → representative response → visible difference; clear labels for fictional data. |
| Audio tool | Interactive sequence/waveform/timeline; optional audio started by a gesture, never autoplay. |

Do not build the whole product. Do not mix five hypotheses in one screen that is hard
to interpret. A gallery is navigation to separate prototypes, not an excuse
for each card to replace its experiment.

## Local execution

- Prefer embedded vanilla HTML, CSS, and JavaScript; `file://` must work.
- Avoid `fetch`, imports, CDNs, remote fonts, telemetry, external resources, and
  `service workers`. Do not install packages for an exploratory demo.
- Do not import product modules. Do not start its server or run its CLI.
- Use data generated in memory and small, deterministic fixtures when possible.
- In-memory state is lost on reload. Do not present it as saved to disk.
  The agent persists the canonical decisions, not a browser promise.
- A download button must download a real file or be marked unambiguously
  as a simulation; do not show "exported" if it did not happen. Name exactly what was generated.
- A generic-format prototype does not prove compatibility with engines, codecs, or
  external applications. It does not prove production performance or final quality either.

The included template is deliberately incomplete. It keeps a
`BRAINSTORMER_TEMPLATE_ONLY` marker that the helper rejects. Do not delete the marker to
get a skeleton approved: implement and test the idea's experience first.

## Demo honesty

`working-slice`: a bounded slice does work locally. List what stays out.
`approximation`: approximate behavior, for example Canvas 2D instead of WebGL.
`simulation`: a flow represented with simulated data and responses, not a real integration.
`omitted`: not created, because of an explicit, documented, and visible exception.

One demo can have real and simulated parts. Choose the mode that best
describes the main hypothesis and explain the parts. Do not simulate benchmarks,
authentication, permissions, collaboration, payments, or inference as if they were connected.

## Safety and ergonomics

Use `textContent` for user input; no `eval`, `Function`, real shell, or
arbitrary HTML. If you represent a CLI, parse a small allowed grammar.
Do not store secrets or write outside the session directory.
Any access to user files must be through explicit selection, and local only.
Demos do not need camera/mic permissions; do not request them unless the experiment was agreed.

Keyboard-accessible controls, visible focus, labels, and sufficient contrast.
A layout that works on desktop and in a narrow viewport without useless horizontal scrolling.
Pausable motion; respect `prefers-reduced-motion` if you animate. Do not use rapid
flashes to demonstrate effects; offer static alternatives or limited intensity.
For canvas, add a text description of the state. Do not use color as the only signal.

## Checks before presenting

1. Open the local HTML file without a server or network; check that it loads without console errors.
2. Change at least one control and verify the substantial change in the output.
3. Pause/reset, when applicable, and check the expected state.
4. Test edge or invalid inputs if there are forms/commands.
5. If there is a real export, open/inspect the file and validate its basic structure.
6. Review keyboard navigation and simulation notes in the test viewport. Add a mobile width when the experiment or a responsive change requires it.

Save screenshots in the folder that the repository specifies, usually `.scratch/screenshots/<task-slug>/`. Keep unique evidence and the necessary context. If there is leftover material, record the batch and its owner; remove it only with the authority that the project requires. Closing a round does not authorize deletions or moves.

Record concrete results. A screenshot only proves the appearance of one state;
it does not demonstrate interaction. An interaction test does not prove product value either.
Without an available browser, record `not-run`; do not claim tests that you did not run.
