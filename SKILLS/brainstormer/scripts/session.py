#!/usr/bin/env python3
"""Local, dependency-free bookkeeping for Brainstormer (Python 3.10+).

All writes are fenced into PROJECT/.scratch/brainstorming. This is not a
JavaScript sandbox, an agent evaluator, or a semantic feature validator.
One writer per session; each file write is atomic, multi-file edits are not.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata
import uuid

STATUSES = {"proposed", "exploring", "saved", "parked", "discarded"}
STATUS_LABELS = {"proposed": "Proposed", "exploring": "Exploring", "saved": "Saved", "parked": "Parked", "discarded": "Discarded"}
ASSESSMENTS = {"not-found-in-inspected-scope", "distinct-extension", "unknown"}
MODES = {"working-slice", "approximation", "simulation", "omitted"}
FIELDS = {"title", "category", "pitch", "user_value", "use_case", "novelty_delta", "evidence", "novelty", "prototype", "open_question", "parent_ids"}
SESSION_RE = re.compile(r"[a-z0-9][a-z0-9_-]{1,119}\Z")
IDEA_RE = re.compile(r"I[0-9]{3,}\Z")


class SessionError(ValueError):
    """Actionable input or workspace error."""


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SessionError(f"{field}: non-empty text is required")
    return value.strip()


def slug(value: str) -> str:
    plain = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")[:42] or "project"


def safe(base: Path, *parts: str) -> Path:
    """Reject traversal and symlinks in every existing component below base."""
    target = base.joinpath(*parts)
    try:
        relative = target.relative_to(base)
    except ValueError as exc:
        raise SessionError("Path is outside the brainstorming workspace") from exc
    if ".." in relative.parts:
        raise SessionError("'..' is not allowed in session paths")
    current = base
    if current.is_symlink():
        raise SessionError(f"Symlinks are not allowed: {current}")
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise SessionError(f"Symlinks are not allowed: {current}")
        # Canonical checks also catch junction/reparse redirects where is_symlink
        # may be false (notably on Windows). The project root is already resolved.
        if current.exists() and current.resolve() != current:
            raise SessionError(f"Directory redirects are not allowed: {current}")
    return target


def workspace(root: str | Path, create: bool = False) -> Path:
    try:
        project = Path(root).expanduser().resolve(strict=True)
    except OSError as exc:
        raise SessionError(f"Project root not found: {root}") from exc
    if not project.is_dir():
        raise SessionError("The root must be an existing directory")
    base = safe(project, ".scratch", "brainstorming")
    if create:
        base.mkdir(parents=True, exist_ok=True)
    if not base.is_dir():
        raise SessionError("No brainstorming workspace; run init first")
    return base


def write(base: Path, path: Path, content: str) -> None:
    checked = safe(base, str(path.relative_to(base)))
    checked.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=checked.parent, delete=False, newline="\n") as handle:
            temp_name = handle.name
            handle.write(content)
        os.replace(temp_name, checked)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def dump(value: object) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def read_json(path: Path) -> dict:
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SessionError(f"Could not read valid JSON: {path}") from exc
    if not isinstance(result, dict):
        raise SessionError(f"Expected a JSON object: {path}")
    return result


def load(root: str | Path, sid: str) -> tuple[Path, Path, dict]:
    if not SESSION_RE.fullmatch(sid):
        raise SessionError("Invalid session ID; use the ID that init returned, not a path")
    base = workspace(root)
    folder = safe(base, sid)
    session = read_json(safe(base, sid, "session.json"))
    if session.get("schema_version") != 1 or session.get("id") != sid:
        raise SessionError("Invalid session.json ID or version")
    ids = session.get("idea_ids")
    if not isinstance(ids, list) or any(not isinstance(i, str) or not IDEA_RE.fullmatch(i) for i in ids) or len(set(ids)) != len(ids):
        raise SessionError("Invalid ID list")
    next_number = session.get("next_idea_number")
    if type(next_number) is not int or next_number <= max([int(i[1:]) for i in ids] + [0]):
        raise SessionError("Inconsistent ID counter")
    if not isinstance(session.get("events"), list):
        raise SessionError("Invalid session history")
    return base, folder, session


def check_idea(data: dict, valid_parents: list[str]) -> None:
    if not isinstance(data, dict):
        raise SessionError("The idea must be a JSON object")
    if set(data) != FIELDS:
        raise SessionError(f"Idea fields: missing {sorted(FIELDS - set(data))}; extra {sorted(set(data) - FIELDS)}")
    for field in ("title", "category", "pitch", "user_value", "use_case", "novelty_delta", "open_question"):
        text(data[field], field)
    parents = data["parent_ids"]
    if not isinstance(parents, list) or any(not isinstance(p, str) or p not in valid_parents for p in parents):
        raise SessionError("parent_ids must refer only to earlier ideas in this session")
    if len(set(parents)) != len(parents):
        raise SessionError("parent_ids contains duplicates")
    evidence = data["evidence"]
    if not isinstance(evidence, list):
        raise SessionError("evidence must be a list")
    for item in evidence:
        if not isinstance(item, dict) or item.get("kind") not in {"code", "test", "documentation", "user", "hypothesis"}:
            raise SessionError("Invalid evidence kind")
        text(item.get("source"), "evidence.source")
        text(item.get("finding"), "evidence.finding")
    novelty = data["novelty"]
    if not isinstance(novelty, dict) or novelty.get("assessment") not in ASSESSMENTS or novelty.get("confidence") not in {"low", "medium", "high"}:
        raise SessionError("Invalid novelty assessment")
    scope = novelty.get("inspected_scope")
    if not isinstance(scope, list) or any(not isinstance(v, str) or not v.strip() for v in scope):
        raise SessionError("inspected_scope must be a list of references")
    text(novelty.get("uncertainty"), "novelty.uncertainty")
    if novelty["assessment"] != "unknown" and (not evidence or not scope):
        raise SessionError("A novelty claim needs evidence and an inspected scope")
    proto = data["prototype"]
    if not isinstance(proto, dict) or proto.get("mode") not in MODES:
        raise SessionError("Invalid prototype mode")
    for field in ("question", "observable"):
        text(proto.get(field), f"prototype.{field}")
    limits = proto.get("limitations")
    if not isinstance(limits, list) or not limits or any(not isinstance(v, str) or not v.strip() for v in limits):
        raise SessionError("The prototype needs at least one explicit limitation")
    checks = proto.get("checks")
    if not isinstance(checks, list):
        raise SessionError("prototype.checks must be a list")
    for item in checks:
        if not isinstance(item, dict) or item.get("result") not in {"passed", "failed", "not-run"}:
            raise SessionError("Invalid check result")
        text(item.get("check"), "prototype.check")


def check_html(content: str) -> None:
    if "<html" not in content.lower() or "</html>" not in content.lower():
        raise SessionError("A complete HTML document is required")
    if "BRAINSTORMER_TEMPLATE_ONLY" in content:
        raise SessionError("The incomplete template does not count as a prototype")
    if re.search(r"<script\b[^>]*\bsrc\s*=", content, re.I):
        raise SessionError("The HTML must embed its scripts, with no external/local src")
    if re.search(r"<link\b[^>]*\brel\s*=\s*['\"]?stylesheet", content, re.I):
        raise SessionError("The HTML must embed its styles")
    if re.search(r"\b(?:src|poster)\s*=\s*['\"]\s*(?:https?:)?//", content, re.I):
        raise SessionError("The prototype must not load remote resources")


def check_prototype(data: dict, prototype: str | None, omit_reason: str | None) -> None:
    if data["prototype"]["mode"] == "omitted":
        text(omit_reason, "Explicit reason to omit the prototype")
        if prototype is not None:
            raise SessionError("An omitted prototype must not include HTML")
    else:
        if omit_reason is not None or prototype is None:
            raise SessionError("This idea needs HTML; do not use implicit omission")
        check_html(prototype)


def initialize(root: str | Path, name: str, title: str) -> tuple[str, Path]:
    name, title = text(name, "name"), text(title, "title")
    base = workspace(root, create=True)
    sid = f"{datetime.now().date().isoformat()}-{slug(name)}-{uuid.uuid4().hex[:8]}"
    folder = safe(base, sid)
    folder.mkdir(exist_ok=False)
    safe(base, sid, "ideas").mkdir()
    timestamp = now()
    session = {"schema_version": 1, "id": sid, "project_name": name, "title": title, "created_at": timestamp, "updated_at": timestamp, "mode": "discovery", "next_idea_number": 1, "idea_ids": [], "events": [{"at": timestamp, "action": "session-created"}]}
    write(base, folder / "session.json", dump(session))
    write(base, folder / "context.md", f"# Context — {name}\n\nStatus: pending; the agent must complete it. The helper did not inspect the project.\n\n## Purpose and user\n\nPending.\n\n## Scope actually inspected and version\n\nPending. Do not confuse a tree SHA with a commit.\n\n## Existing, partial, and documented capabilities\n\nPending.\n\n## Access limits and assumptions\n\nPending.\n\n## Previous sessions and ideas consulted\n\nPending.\n\n## Goal of this exploration\n\n{title}\n")
    render(root, sid)
    return sid, folder


def get_ideas(base: Path, folder: Path, session: dict) -> list[dict]:
    ideas = []
    for iid in session["idea_ids"]:
        item = read_json(safe(base, folder.name, "ideas", iid, "idea.json"))
        if item.get("id") != iid or item.get("status") not in STATUSES:
            raise SessionError(f"Invalid ID or status in {iid}")
        ideas.append(item)
    return ideas


def add_idea(root: str | Path, sid: str, data: dict, prototype: str | None, omit_reason: str | None = None) -> str:
    base, folder, session = load(root, sid)
    check_idea(data, session["idea_ids"])
    check_prototype(data, prototype, omit_reason)
    existing = get_ideas(base, folder, session)
    normalized_title = unicodedata.normalize("NFKC", data["title"]).strip().casefold()
    if any(unicodedata.normalize("NFKC", i["title"]).strip().casefold() == normalized_title for i in existing):
        raise SessionError("Duplicate title; review the existing idea or name a real variant")
    iid = f"I{session['next_idea_number']:03d}"
    directory = safe(base, sid, "ideas", iid)
    directory.mkdir(exist_ok=False)
    timestamp = now()
    item = copy.deepcopy(data)
    item.update({"id": iid, "status": "proposed", "created_at": timestamp, "updated_at": timestamp, "revision": 1, "decision_reason": "", "prototype_path": f"ideas/{iid}/prototype.html" if prototype is not None else None})
    if omit_reason:
        item["prototype"]["limitations"].append(f"Explicit omission: {omit_reason}")
    write(base, directory / "idea.json", dump(item))
    if prototype is not None:
        write(base, directory / "prototype.html", prototype)
    session["idea_ids"].append(iid)
    session["next_idea_number"] += 1
    session["updated_at"] = timestamp
    session["events"].append({"at": timestamp, "action": "idea-added", "id": iid})
    write(base, folder / "session.json", dump(session))
    render(root, sid)
    return iid


def decide(root: str | Path, sid: str, iid: str, status: str, reason: str) -> None:
    if status not in STATUSES:
        raise SessionError("Invalid status")
    reason = text(reason, "reason")
    base, folder, session = load(root, sid)
    if iid not in session["idea_ids"]:
        raise SessionError("Unknown idea")
    path = safe(base, sid, "ideas", iid, "idea.json")
    item = read_json(path)
    previous = item["status"]
    timestamp = now()
    item.update(status=status, decision_reason=reason, updated_at=timestamp)
    write(base, path, dump(item))
    session["updated_at"] = timestamp
    session["events"].append({"at": timestamp, "action": "decision", "id": iid, "from": previous, "to": status, "reason": reason})
    write(base, folder / "session.json", dump(session))
    render(root, sid)


def revise(root: str | Path, sid: str, iid: str, data: dict, prototype: str | None, reason: str, omit_reason: str | None = None) -> None:
    reason = text(reason, "reason")
    base, folder, session = load(root, sid)
    if iid not in session["idea_ids"]:
        raise SessionError("Unknown idea")
    previous_ids = session["idea_ids"][:session["idea_ids"].index(iid)]
    check_idea(data, previous_ids)
    check_prototype(data, prototype, omit_reason)
    directory = safe(base, sid, "ideas", iid)
    old = read_json(safe(base, sid, "ideas", iid, "idea.json"))
    # A variant involving later ideas must get a new ID, never a cyclic lineage.
    other_titles = {unicodedata.normalize("NFKC", i["title"]).strip().casefold() for i in get_ideas(base, folder, session) if i["id"] != iid}
    if unicodedata.normalize("NFKC", data["title"]).strip().casefold() in other_titles:
        raise SessionError("The revision would duplicate the title of another idea")
    backup = safe(base, sid, "ideas", iid, "revisions", f"r{old['revision']:03d}")
    backup.mkdir(parents=True, exist_ok=False)
    write(base, backup / "idea.json", dump(old))
    old_html = safe(base, sid, "ideas", iid, "prototype.html")
    if old_html.exists():
        write(base, backup / "prototype.html", old_html.read_text(encoding="utf-8"))
    item = copy.deepcopy(old)
    item.update(copy.deepcopy(data))
    timestamp = now()
    item.update(revision=old["revision"] + 1, updated_at=timestamp, prototype_path=f"ideas/{iid}/prototype.html" if prototype is not None else None)
    if omit_reason:
        item["prototype"]["limitations"].append(f"Explicit omission: {omit_reason}")
    write(base, directory / "idea.json", dump(item))
    if prototype is not None:
        write(base, old_html, prototype)
    elif old_html.exists():
        old_html.unlink()
    session["updated_at"] = timestamp
    session["events"].append({"at": timestamp, "action": "idea-revised", "id": iid, "revision": item["revision"], "reason": reason})
    write(base, folder / "session.json", dump(session))
    render(root, sid)


STYLE = """
:root{color-scheme:dark;font:16px/1.55 system-ui,sans-serif;color:#ecede9;background:#131719}*{box-sizing:border-box}body{margin:0}main{max-width:1180px;margin:auto;padding:48px 26px 70px}h1{font-size:clamp(2rem,5vw,3.8rem);line-height:1.07;letter-spacing:-.045em;max-width:850px;margin:14px 0 20px}h2{line-height:1.2;letter-spacing:-.025em}p{max-width:76ch}.eyebrow{letter-spacing:.14em;text-transform:uppercase;font-size:.76rem;color:#afc9be}.muted{color:#bac4c2}.notice{border-left:3px solid #b5c7a4;padding:12px 18px;background:#1b2223;margin:25px 0}.toolbar{display:flex;gap:16px;flex-wrap:wrap;margin:30px 0 20px}label{display:grid;gap:6px;font-size:.84rem;color:#c7cecb}input,select{font:inherit;color:inherit;background:#222a2c;border:1px solid #526062;padding:12px;border-radius:9px}input{min-width:260px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}article{background:#1d2527;border:1px solid #414d4e;border-radius:16px;padding:24px;display:flex;flex-direction:column}article p{margin:9px 0}article .pitch{font-size:1.13rem}.tag{font-size:.76rem;color:#d4e4dc;border:1px solid #546763;border-radius:30px;padding:4px 10px;display:inline-block}.meta{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.actions{margin-top:auto;padding-top:20px;display:flex;gap:17px;align-items:center}a{color:#c4e6d5;text-underline-offset:4px}.button{background:#c7ddbe;color:#18201d;text-decoration:none;padding:10px 14px;border-radius:8px;font-weight:650}.button:hover{background:#d9eace}:focus-visible{outline:3px solid #f0dbac;outline-offset:4px}footer{margin-top:40px;border-top:1px solid #424e50;padding-top:20px;font-size:.85rem;color:#bac4c2}[hidden]{display:none!important}@media(max-width:720px){main{padding:28px 16px}.grid{grid-template-columns:1fr}.toolbar>*{width:100%}input{min-width:0;width:100%}article{padding:20px}}
"""


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def brief(item: dict) -> str:
    lines = [f"# {item['id']} — {item['title']}", "", f"Status: **{STATUS_LABELS[item['status']]}** · Revision {item['revision']} · {item['category']}", "", item["pitch"], ""]
    for label, field in (("User value", "user_value"), ("Use case", "use_case"), ("Proposed difference", "novelty_delta"), ("Open question", "open_question")):
        lines.extend([f"## {label}", "", item[field], ""])
    n, p = item["novelty"], item["prototype"]
    lines += ["## Novelty and evidence", "", f"Assessment: `{n['assessment']}`. Confidence: `{n['confidence']}`.", "", n["uncertainty"], "", "Scope: " + ("; ".join(n["inspected_scope"]) or "Not inspected"), ""]
    lines += [f"- [{e['kind']}] {e['source']}: {e['finding']}" for e in item["evidence"]]
    lines += ["", "## Prototype", "", f"Mode: `{p['mode']}`.", "", f"Question: {p['question']}", "", f"Observable: {p['observable']}", ""]
    lines += ["[Open the HTML](prototype.html)" if item["prototype_path"] else "No HTML was created; see the explicit omission.", ""]
    lines += [f"- Limitation: {v}" for v in p["limitations"]]
    lines += [f"- Check `{v['result']}`: {v['check']}" for v in p["checks"]]
    lines += ["", "## Decision", "", item["decision_reason"] or "No user decision. Silence does not mean discard.", "", "Parent ideas: " + (", ".join(item["parent_ids"]) or "None"), "", "Keeping an idea does not authorize planning or implementing it.", ""]
    return "\n".join(lines)


def render(root: str | Path, sid: str) -> None:
    base, folder, session = load(root, sid)
    ideas = get_ideas(base, folder, session)
    cards = []
    for item in ideas:
        iid = item["id"]
        write(base, safe(base, sid, "ideas", iid, "brief.md"), brief(item))
        action = f'<a class="button" href="ideas/{iid}/prototype.html">Try the idea ↗</a>' if item["prototype_path"] else '<span>Demo omitted: see the idea record.</span>'
        cards.append(f'''<article data-status="{esc(item['status'])}"><div class="meta"><span class="eyebrow">{esc(iid)} / {esc(item['category'])}</span><span class="tag">{esc(STATUS_LABELS[item['status']])}</span></div><h2>{esc(item['title'])}</h2><p class="pitch">{esc(item['pitch'])}</p><p class="muted">{esc(item['user_value'])}</p><p><strong>Novelty:</strong> {esc(item['novelty']['assessment'])} · {esc(item['novelty']['confidence'])}</p><p class="muted">Demo: {esc(item['prototype']['mode'])}. {esc(item['prototype']['question'])}</p><div class="actions">{action}<a href="ideas/{iid}/brief.md">Read the idea record</a></div></article>''')
    options = ''.join(f'<option value="{k}">{esc(v)}</option>' for k, v in STATUS_LABELS.items())
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(session['title'])} — Brainstormer</title><style>{STYLE}</style></head><body><main><header><p class="eyebrow">Brainstormer / {esc(session['project_name'])}</p><h1>{esc(session['title'])}</h1><p class="muted">A lab of possibilities. Each card opens a standalone experiment. It is not a roadmap or a list of commitments.</p></header><div class="notice">Keeping an idea does not authorize building it. Filters only change this view; decisions are recorded with the agent, not from the browser.</div><nav><a href="context.md">Context and scope</a> · <a href="session.md">Decisions</a></nav><div class="toolbar"><label>Search ideas<input id="search" type="search" placeholder="Name, capability, or outcome…"></label><label>Status<select id="status"><option value="all">All</option>{options}</select></label></div><p id="count" class="muted" aria-live="polite">{len(ideas)} ideas</p><div class="grid">{''.join(cards)}</div><p id="empty" hidden>No ideas match these filters.</p><footer>Session {esc(sid)} · Updated {esc(session['updated_at'])}.<br>Local index without telemetry. Evidence and limitations are in each idea record. This index did not validate the quality of the real product.</footer></main><script>
const search=document.getElementById('search'),status=document.getElementById('status'),cards=[...document.querySelectorAll('article')];
function filter(){{const q=search.value.trim().toLocaleLowerCase();let count=0;for(const card of cards){{const show=(status.value==='all'||card.dataset.status===status.value)&&card.textContent.toLocaleLowerCase().includes(q);card.hidden=!show;if(show)count++;}}document.getElementById('count').textContent=count+' of '+cards.length+' ideas';document.getElementById('empty').hidden=count!==0;}}
search.addEventListener('input',filter);status.addEventListener('change',filter);
</script></body></html>'''
    write(base, folder / "index.html", page)
    lines = [f"# {session['title']}", "", f"Project: {session['project_name']}", "", "Mode: discovery. This file is not an implementation plan.", "", "[Open the gallery](index.html)", "", "## Ideas", ""]
    for item in ideas:
        lines += [f"### {item['id']} — {item['title']}", "", f"{STATUS_LABELS[item['status']]} · [Idea record](ideas/{item['id']}/brief.md)", "", item["decision_reason"] or "No user decision.", ""]
    lines += ["## History", ""]
    for event in session["events"]:
        lines.append(f"- {event['at']} · {event['action']} {event.get('id', '')} {event.get('to', '')} {event.get('reason', '')}".rstrip())
    write(base, folder / "session.md", "\n".join(lines) + "\n")


def validate(root: str | Path, sid: str) -> list[str]:
    base, folder, session = load(root, sid)
    ideas = get_ideas(base, folder, session)
    previous = []
    for item in ideas:
        iid = item["id"]
        check_idea({key: item[key] for key in FIELDS}, previous)
        expected = None if item["prototype"]["mode"] == "omitted" else f"ideas/{iid}/prototype.html"
        if item.get("prototype_path") != expected:
            raise SessionError(f"Inconsistent prototype path: {iid}")
        if expected:
            check_html(safe(base, sid, expected).read_text(encoding="utf-8"))
        if type(item.get("revision")) is not int or item["revision"] < 1:
            raise SessionError(f"Invalid revision: {iid}")
        previous.append(iid)
    for name in ("context.md", "session.md", "index.html"):
        if not safe(base, sid, name).is_file():
            raise SessionError(f"Missing file: {name}")
    return [f"{len(ideas)} ideas: structure, statuses, IDs, and paths checked.", "Does not assess value, novelty, JavaScript, or browser behavior."]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "add", "decide", "revise", "render", "validate"):
        p = commands.add_parser(command)
        p.add_argument("--root", required=True, help="Existing local project root")
        if command == "init":
            p.add_argument("--name", required=True)
            p.add_argument("--title", default="Explore new capabilities")
            continue
        p.add_argument("--session", required=True, help="Exact session ID")
        if command in {"decide", "revise"}:
            p.add_argument("--id", required=True)
            p.add_argument("--reason", required=True)
        if command == "decide":
            p.add_argument("--status", choices=sorted(STATUSES), required=True)
        if command in {"add", "revise"}:
            p.add_argument("--idea", required=True, help="Input JSON without managed fields")
            choice = p.add_mutually_exclusive_group(required=True)
            choice.add_argument("--prototype", help="Self-contained HTML document")
            choice.add_argument("--omit-prototype", help="Explicit omission reason")
    args = parser.parse_args()
    try:
        if args.command == "init":
            sid, folder = initialize(args.root, args.name, args.title)
            print(dump({"session": sid, "path": str(folder)}), end="")
        elif args.command in {"add", "revise"}:
            data = read_json(Path(args.idea))
            prototype = Path(args.prototype).read_text(encoding="utf-8") if args.prototype else None
            if args.command == "add":
                print(add_idea(args.root, args.session, data, prototype, args.omit_prototype))
            else:
                revise(args.root, args.session, args.id, data, prototype, args.reason, args.omit_prototype)
                print(f"Revision saved: {args.id}")
        elif args.command == "decide":
            decide(args.root, args.session, args.id, args.status, args.reason)
            print(f"{args.id}: {args.status}")
        elif args.command == "render":
            render(args.root, args.session)
            print("Index and views regenerated")
        else:
            print("\n".join(validate(args.root, args.session)))
        return 0
    except (SessionError, OSError, KeyError, TypeError) as exc:
        print(f"brainstormer: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
