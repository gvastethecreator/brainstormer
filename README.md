# Brainstormer

Agent Skill for product feature discovery. It turns ideas into small interactive prototypes the user can try, keep, or discard.

The operating skill is written in Spanish. Session files go in `.scratch/brainstorming/`, not inside this package.

## Quick start

```text
npx skills add gvastethecreator/brainstormer
```

Copy `SKILLS/brainstormer` into the skill directory your agent already loads. Keep references, templates, and `scripts/session.py`.

Optional helper: Python 3.10+ and the standard library.

```text
python <skill-root>/scripts/session.py --help
python -m unittest discover -s <skill-root>/tests -v
```

Spanish install notes and prompts: [SKILLS/brainstormer/README.md](SKILLS/brainstormer/README.md). Operating contract: [SKILL.md](SKILLS/brainstormer/SKILL.md).

License: [MIT](LICENSE).
