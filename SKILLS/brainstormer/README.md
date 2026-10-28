# brainstormer · v1.1.0

Una skill para explorar nuevas capacidades de un producto con propuestas concretas,
conversación y prototipos pequeños. **No es una auditoría, una grill de detalles,
un planificador ni un agente de implementación.**

## Instalar

Copiá la carpeta completa `brainstormer/` al directorio de skills que descubra tu
agente. No copies sólo `SKILL.md`: sus referencias, plantillas y helper son parte
del paquete. Como ubicación de proyecto podés usar `.agents/skills/brainstormer/`
cuando tu entorno admita ese directorio. Otros hosts requieren otra ruta; el
formato del paquete no implica detección automática universal.

La instalación de la skill y sus archivos es una acción diferente a ejecutar una
sesión. **Los resultados de las sesiones van en `.scratch/brainstorming/`**, salvo una ruta de artefactos exigida por el repositorio; nunca
dentro de la carpeta de la skill. Este paquete no modifica ni instala nada en un
repositorio remoto automáticamente.

## Invocación recomendada

```text
Usá la skill brainstormer en este proyecto.
Analizá qué hace, qué capacidades tiene y qué ideas exploramos antes.
Proponé una primera ronda de features nuevas y sustanciales, coherentes con el
producto. Prepará una ficha y un HTML interactivo independiente por opción en
.scratch/brainstorming. Quiero explorar posibilidades; no implementes cambios,
no generes tickets y no armes todavía un plan de ejecución.
```

Para una ronda específica:

```text
Usá brainstormer, pero esta ronda dedicada a efectos nuevos.
Cada opción debe ser un efecto distinto, explicado con un uso concreto y un
prototipo que permita apreciar su comportamiento. Evitá presets de lo existente.
```

Para retomar:

```text
Retomá nuestra última sesión de brainstormer. Leé las ideas y decisiones guardadas.
Mostrame dónde quedamos y continuemos con opciones nuevas, sin repetir descartes
ni convertir favoritas en tareas.
```

Estos son pedidos en lenguaje natural. Un host puede ofrecer además su propia
sintaxis para invocar skills; no se presupone un comando universal.

## Qué pasa durante una sesión

El agente entiende el producto y contrasta lo existente. Para una sesión completa, abre una carpeta; una ronda pedida solo en chat no crea archivos.
Genera una ronda manejable que respeta la cantidad pedida, con demos independientes cuando forman parte del encargo.
Vos probás, combinás, conservás, descartás o pedís nuevas rondas. Quedan fichas,
prototipos y decisiones; no un roadmap. No hace falta elegir una sola idea.

Un ejemplo de conversación es: «Guardemos I001 e I004; I002 no encaja. Hagamos una
variante de I003 y después mostrame más fuentes de entrada». Esto conserva ideas,
registra el descarte y mantiene la exploración abierta. No autoriza construir nada.

## Qué incluye la carpeta

| Archivo | Función |
| --- | --- |
| `LICENSE` | Aviso MIT que debe acompañar la copia portable. |
| `SKILL.md` | Instrucciones que carga el agente; instrucciones centrales compactas. |
| `references/session-contract.md` | Evidencia, persistencia, estados, rondas y helper. |
| `references/feature-filter.md` | Umbral de novedad, valor concreto y selección de rondas. |
| `references/prototype-contract.md` | Interactividad, simulación honesta y pruebas. |
| `assets/idea.schema.json` | Esquema de la ficha de entrada. |
| `assets/idea-input.example.json` | Ejemplo editable, no una idea ya validada. |
| `assets/prototype-template.html` | Esqueleto marcado como incompleto, no una demo aprobable. |
| `scripts/session.py` | Helper opcional para archivos, IDs, decisiones, revisiones e índice. |
| `tests/test_session.py` | pruebas unitarias del helper. |
| `evals/evals.json` | Casos de evaluación conversacional; no ejecutados con agentes en esta entrega. |

El helper necesita Python 3.10+ y su biblioteca estándar. Las instrucciones pueden
usarse sin Python escribiendo la misma estructura manualmente. Ninguna parte de la
skill exige un framework de frontend, proveedor de IA, servicio pago o servidor.

## Probar el helper

Desde la carpeta `brainstormer/`:

```sh
python -m unittest discover -s tests -v
python scripts/session.py --help
```

Los comandos de sesión están detallados en `references/session-contract.md`.
El script no inspecciona repositorios, no genera ideas y no evalúa valor: automatiza
el mantenimiento del laboratorio. Rechaza rutas de escape y symlinks bajo su zona
de escritura, pero **no es un sandbox para JavaScript no confiable**.

## Evaluar el comportamiento del agente

`evals/evals.json` contiene casos positivos, negativos y límites de autorización.
Probá cada caso en sesiones aisladas, con fixtures o repositorios de prueba, y compará
el comportamiento con y sin la skill. Observá las escrituras reales y las demos,
no sólo que el agente diga que respetó las reglas. No uses esas evaluaciones para
modificar un repositorio productivo.

La suite comprueba el helper. La plantilla HTML está incompleta a propósito y no demuestra un prototipo funcional. Las pruebas de archivos no equivalen a una evaluación de la skill con agentes; registrar por separado cualquier ejecución real.

## Referencias de diseño

Formato: Agent Skills, especificación oficial (`https://agentskills.io/specification`).
Descripción activable, instrucciones compactas y referencias bajo demanda:
`https://agentskills.io/skill-creation/best-practices`.
Separación entre pruebas de artefactos y evaluación del agente:
`https://agentskills.io/skill-creation/evaluating-skills`.

El nombre, frontmatter y estructura siguen ese formato abierto. La carga y los
permisos concretos dependen del host donde la instales.
