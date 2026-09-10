"""Structural/helper tests. These do not evaluate an agent or feature value."""
from pathlib import Path
import copy
import importlib.util
import json
import tempfile
import unittest

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('session', HERE / 'scripts' / 'session.py')
session = importlib.util.module_from_spec(spec)
spec.loader.exec_module(session)
HTML = '<!doctype html><html lang="es"><head><title>Prueba estructural</title></head><body><p>No es una demo de producto.</p></body></html>'


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source.ts').write_text('export const unchanged = true;')
        (self.root / '.gitignore').write_text('node_modules\n')
        self.sid, self.folder = session.initialize(self.root, 'Proyecto de prueba', 'Explorar capacidades')
        self.data = json.loads((HERE / 'assets' / 'idea-input.example.json').read_text())
        self.data['title'] = 'Una capacidad distinta'

    def add(self, title=None, data=None):
        payload = copy.deepcopy(data or self.data)
        if title:
            payload['title'] = title
        return session.add_idea(self.root, self.sid, payload, HTML)

    def idea(self, iid='I001'):
        return json.loads((self.folder / 'ideas' / iid / 'idea.json').read_text())

    def test_init_stays_in_scratch_and_does_not_touch_product(self):
        self.assertTrue(self.folder.is_relative_to(self.root / '.scratch' / 'brainstorming'))
        self.assertEqual((self.root / 'source.ts').read_text(), 'export const unchanged = true;')
        self.assertEqual((self.root / '.gitignore').read_text(), 'node_modules\n')
        self.assertEqual(set(p.name for p in self.root.iterdir()), {'source.ts', '.gitignore', '.scratch'})
        self.assertIn('El helper no inspeccionó', (self.folder / 'context.md').read_text())

    def test_ids_are_sequential_and_survive_status_changes(self):
        self.assertEqual(self.add(), 'I001')
        session.decide(self.root, self.sid, 'I001', 'discarded', 'El usuario descartó esta idea.')
        self.assertEqual(self.add('Otra capacidad'), 'I002')
        session.validate(self.root, self.sid)

    def test_duplicate_title_is_rejected(self):
        self.add()
        with self.assertRaises(session.SessionError):
            self.add('  UNA CAPACIDAD DISTINTA  ')
        self.assertFalse((self.folder / 'ideas' / 'I002').exists())

    def test_parent_lineage_requires_existing_ideas(self):
        self.add()
        data = copy.deepcopy(self.data)
        data.update(title='Variante de la primera', parent_ids=['I001'])
        self.assertEqual(self.add(data=data), 'I002')
        data.update(title='Variante imposible', parent_ids=['I999'])
        with self.assertRaises(session.SessionError):
            self.add(data=data)

    def test_decision_records_user_reason_but_no_implementation_status(self):
        self.add()
        session.decide(self.root, self.sid, 'I001', 'saved', 'El usuario quiere conservarla, no construirla.')
        self.assertEqual(self.idea()['status'], 'saved')
        events = json.loads((self.folder / 'session.json').read_text())['events']
        self.assertEqual(events[-1]['from'], 'proposed')
        self.assertEqual(events[-1]['to'], 'saved')
        with self.assertRaises(session.SessionError):
            session.decide(self.root, self.sid, 'I001', 'approved-for-implementation', 'No existe ese estado.')

    def test_silence_never_changes_status(self):
        self.add()
        session.render(self.root, self.sid)
        self.assertEqual(self.idea()['status'], 'proposed')

    def test_empty_decision_reason_rejected(self):
        self.add()
        with self.assertRaises(session.SessionError):
            session.decide(self.root, self.sid, 'I001', 'saved', '   ')

    def test_revision_preserves_previous_content_and_status(self):
        self.add()
        session.decide(self.root, self.sid, 'I001', 'saved', 'Conservar por pedido del usuario.')
        data = copy.deepcopy(self.data)
        data['pitch'] = 'Una explicación refinada del mismo resultado.'
        revised_html = HTML.replace('No es una demo de producto.', 'Otra muestra estructural.')
        session.revise(self.root, self.sid, 'I001', data, revised_html, 'El usuario pidió refinar la muestra.')
        self.assertEqual(self.idea()['revision'], 2)
        self.assertEqual(self.idea()['status'], 'saved')
        backup = self.folder / 'ideas' / 'I001' / 'revisions' / 'r001'
        self.assertEqual((backup / 'prototype.html').read_text(), HTML)
        self.assertEqual(json.loads((backup / 'idea.json').read_text())['revision'], 1)
        session.validate(self.root, self.sid)

    def test_self_parent_and_forward_parent_cannot_be_added_by_revision(self):
        self.add()
        self.add('Segunda idea')
        for parent in ['I001', 'I002']:
            data = copy.deepcopy(self.data)
            data['parent_ids'] = [parent]
            with self.assertRaises(session.SessionError):
                session.revise(self.root, self.sid, 'I001', data, HTML, 'No debe permitir ciclos.')

    def test_template_and_remote_scripts_are_rejected(self):
        for content in [HTML.replace('<body>', '<body><!-- BRAINSTORMER_TEMPLATE_ONLY -->'), HTML.replace('</body>', '<script src="https://invalid.test/a.js"></script></body>')]:
            with self.assertRaises(session.SessionError):
                session.add_idea(self.root, self.sid, self.data, content)
        self.assertFalse((self.folder / 'ideas' / 'I001').exists())

    def test_omission_requires_explicit_reason_and_mode(self):
        with self.assertRaises(session.SessionError):
            session.add_idea(self.root, self.sid, self.data, None)
        data = copy.deepcopy(self.data)
        data['prototype']['mode'] = 'omitted'
        with self.assertRaises(session.SessionError):
            session.add_idea(self.root, self.sid, data, None)
        session.add_idea(self.root, self.sid, data, None, 'El usuario pidió sólo ideas esta ronda.')
        self.assertIsNone(self.idea()['prototype_path'])
        self.assertNotIn('href="ideas/I001/prototype.html"', (self.folder / 'index.html').read_text())
        session.validate(self.root, self.sid)

    def test_novelty_claim_without_evidence_is_rejected(self):
        data = copy.deepcopy(self.data)
        data['novelty']['assessment'] = 'not-found-in-inspected-scope'
        with self.assertRaises(session.SessionError):
            self.add(data=data)

    def test_gallery_escapes_user_text(self):
        self.add('<img src=x onerror=alert(1)>')
        page = (self.folder / 'index.html').read_text()
        self.assertIn('&lt;img src=x onerror=alert(1)&gt;', page)
        self.assertNotIn('<img src=x', page)

    def test_context_is_preserved_when_rendering(self):
        path = self.folder / 'context.md'
        path.write_text('Contexto revisado por el agente.')
        self.add()
        self.assertEqual(path.read_text(), 'Contexto revisado por el agente.')

    def test_traversal_is_rejected(self):
        for sid in ['../outside', str(self.folder), '.', 'a/b']:
            with self.assertRaises(session.SessionError):
                session.load(self.root, sid)

    def test_output_symlink_cannot_overwrite_an_external_file(self):
        outside = self.root / 'source.ts'
        index = self.folder / 'index.html'
        index.unlink()
        try:
            index.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('No hay permisos para probar symlinks en este sistema.')
        with self.assertRaises(session.SessionError):
            session.render(self.root, self.sid)
        self.assertEqual(outside.read_text(), 'export const unchanged = true;')

    def test_workspace_symlink_is_rejected(self):
        other = self.root / 'other-project'
        other.mkdir()
        target = self.root / 'outside'
        target.mkdir()
        try:
            (other / '.scratch').symlink_to(target, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('No hay permisos para probar symlinks en este sistema.')
        with self.assertRaises(session.SessionError):
            session.initialize(other, 'Otro', 'No escapar')
        self.assertEqual(list(target.iterdir()), [])

    def test_validate_is_read_only_and_rejects_tampered_paths(self):
        self.add()
        snapshots = {p: p.read_bytes() for p in self.folder.rglob('*') if p.is_file()}
        session.validate(self.root, self.sid)
        self.assertEqual(snapshots, {p: p.read_bytes() for p in self.folder.rglob('*') if p.is_file()})
        item = self.idea()
        item['prototype_path'] = '../source.ts'
        (self.folder / 'ideas' / 'I001' / 'idea.json').write_text(json.dumps(item))
        with self.assertRaises(session.SessionError):
            session.validate(self.root, self.sid)

    def test_multiple_sessions_do_not_overwrite_previous(self):
        sid2, folder2 = session.initialize(self.root, 'Proyecto de prueba', 'Explorar de nuevo')
        self.assertNotEqual(sid2, self.sid)
        self.assertTrue(folder2.exists() and self.folder.exists())


    def test_revision_rejects_normalized_title_duplicate(self):
        self.add('Atlas')
        self.add('Loops')
        data = copy.deepcopy(self.data)
        data['title'] = 'Ａｔｌａｓ'
        with self.assertRaises(session.SessionError):
            session.revise(self.root, self.sid, 'I002', data, HTML, 'No duplicar con Unicode.')
        self.assertEqual(self.idea('I002')['revision'], 1)

    def test_saved_is_not_a_plan_and_leaves_other_ideas_pending(self):
        self.add('Atlas')
        self.add('Loops')
        session.decide(self.root, self.sid, 'I001', 'saved', 'Conservar, no implementar.')
        self.assertEqual(self.idea('I001')['status'], 'saved')
        self.assertEqual(self.idea('I002')['status'], 'proposed')
        self.assertEqual((self.root / 'source.ts').read_text(), 'export const unchanged = true;')
        self.assertFalse((self.root / 'plan.md').exists())

    def test_revision_preserves_explicit_user_decision(self):
        self.add('Atlas')
        session.decide(self.root, self.sid, 'I001', 'saved', 'Conservar por el caso de uso.')
        data = copy.deepcopy(self.data)
        data.update(title='Atlas',pitch='Una demostración refinada del mismo resultado.')
        session.revise(self.root, self.sid, 'I001', data, HTML, 'Refinar experiencia, no planificar.')
        item = self.idea()
        self.assertEqual(item['status'], 'saved')
        self.assertEqual(item['decision_reason'], 'Conservar por el caso de uso.')
        self.assertEqual(item['revision'], 2)
        self.assertTrue((self.folder / 'ideas/I001/revisions/r001/idea.json').is_file())


if __name__ == '__main__':
    unittest.main()
