# Contrato de sesión

Este contrato aplica a sesiones persistentes. Una ronda pedida solo en chat puede omitir archivos. Usar la ruta de artefactos exigida por el repositorio; el helper admite únicamente `.scratch/brainstorming/`, por lo que otra estructura requiere mantenimiento manual.

## Fuentes y evidencia

Una fuente debe identificar un archivo/rango, símbolo, prueba, documento o
instrucción del usuario realmente leído. Guardá la referencia de versión si está
verificada. Nunca conviertas recuerdos, un tree SHA o una rama leída parcialmente
en una auditoría del último commit.

Usá tres resultados posibles para la novedad:

- `not-found-in-inspected-scope`: no apareció en el alcance documentado; no prueba ausencia absoluta.
- `distinct-extension`: parte de algo existente, pero habilita un resultado nuevo; describí la diferencia.
- `unknown`: propuesta exploratoria cuya ausencia aún no está verificada.

Confianza `low`, `medium` o `high` expresa confianza en esa evaluación, no éxito
comercial ni viabilidad garantizada. Con sólo documentación o acceso fallido,
normalmente corresponde `unknown` y confianza `low`.

Una implementación parcial es trabajo existente, no una idea inédita. Podés explorar
un resultado nuevo sobre ella, pero identificá la parte existente y la diferencia.
No infieras demanda, ingresos, «10×», tiempo de desarrollo o rendimiento sin datos.

## Archivos y consistencia

- `context.md`: escrito por el agente; alcance, producto, reglas, evidencia, límites,
  vínculo con sesiones previas. El helper no lo sobrescribe al renderizar.
- `session.json`: identificador, proyecto, fechas, título, IDs e historial de acciones.
- `ideas/I001/idea.json`: ficha canónica, estado y notas de decisión.
- `ideas/I001/prototype.html`: demo actual, salvo omisión explícita justificada.
- `ideas/I001/revisions/r001/`: ficha y demo anteriores cuando se refina la misma idea.
- `brief.md`, `session.md` e `index.html`: vistas regenerables. No edites sólo una vista.

El helper está pensado para **un escritor por sesión**. Las escrituras de archivos
son atómicas individualmente, no una transacción multiarchivo ni un sistema de
sincronización. No uses dos agentes escribiendo la misma sesión a la vez.

No pongas secretos, tokens, datos personales reales ni contenido privado innecesario
en el laboratorio: podría terminar en un repositorio público. No cambies `.gitignore`
por tu cuenta. Al compartir un ZIP, revisá los datos primero.

## Abrir una sesión con el helper opcional

Sustituí `<skill>` y `<proyecto>` por rutas reales. En Windows puede usarse `py -3`
en lugar de `python`, según la instalación disponible.

```sh
python <skill>/scripts/session.py init --root <proyecto> --name mi-proyecto --title "Explorar nuevas capacidades"
```

El comando imprime un ID de sesión y su ruta; usá ese ID literalmente en los demás
comandos. Primero completá `context.md`. No inventes que el helper inspeccionó el repo.

Construí la ficha de entrada siguiendo `assets/idea-input.example.json` y el esquema
`assets/idea.schema.json`. Creá un HTML auténtico basado, si resulta útil, en
`assets/prototype-template.html`; quitá el marcador de plantilla **sólo después**
de implementar la interacción que prueba la idea.

Creá también estos borradores dentro de la propia sesión, por ejemplo en `drafts/`.
No uses el directorio de la skill como lugar de trabajo.

```sh
python <skill>/scripts/session.py add --root <proyecto> --session <id> --idea <ruta-draft.json> --prototype <ruta-demo.html>
python <skill>/scripts/session.py decide --root <proyecto> --session <id> --id I001 --status saved --reason "El usuario quiere conservar esta posibilidad por…"
python <skill>/scripts/session.py revise --root <proyecto> --session <id> --id I001 --idea <ruta-draft.json> --prototype <ruta-demo.html> --reason "Comparación solicitada de dos comportamientos"
python <skill>/scripts/session.py render --root <proyecto> --session <id>
python <skill>/scripts/session.py validate --root <proyecto> --session <id>
```

La omisión de un prototipo requiere `prototype.mode = "omitted"`, una limitación
explícita en la ficha y `--omit-prototype "razón"` en vez de `--prototype`. Usalo
sólo por pedido del usuario o limitación real, nunca para disimular trabajo pendiente.

El helper comprueba forma, rutas, estados, IDs y algunos errores HTML elementales.
**No certifica** relevancia, novedad, calidad visual, seguridad de JavaScript ni que
una interacción tenga sentido. El HTML es código: revisalo antes de abrir material
de terceros. El agente debe hacer esas comprobaciones por separado.

## Ficha de una idea

Campos de entrada (sin IDs ni fechas, que asigna el helper):

| Campo | Contenido |
| --- | --- |
| `title` | Nombre de una sola capacidad, no un tema genérico. |
| `category` | Categoría útil para este proyecto, sin taxonomía rígida obligatoria. |
| `pitch` | Explicación breve de lo que ahora se podría hacer. |
| `user_value` | Persona, situación y beneficio concreto. |
| `use_case` | Un recorrido observable antes/después, no un slogan. |
| `novelty_delta` | Diferencia con capacidades existentes o declaración de hipótesis. |
| `evidence` | Lista de `{kind, source, finding}`; puede estar vacía sólo si se declara incertidumbre. |
| `novelty` | `{assessment, confidence, inspected_scope, uncertainty}`. |
| `prototype` | `{mode, question, observable, limitations, checks}`. |
| `open_question` | Incertidumbre de producto que merece observarse, no una lista técnica. |
| `parent_ids` | IDs existentes que originaron una variante o combinación; lista vacía normalmente. |

`evidence.kind`: `code`, `test`, `documentation`, `user` o `hypothesis`.
`prototype.mode`: `working-slice`, `approximation`, `simulation` u `omitted`.
`checks`: lista de `{check, result}`, con `result` = `passed`, `failed` o `not-run`.
Anotá lo realmente probado, sin convertir validación estática en prueba de navegador.

La ficha final añade `id`, `status`, `created_at`, `updated_at`, `revision`,
`decision_reason` y `prototype_path`. No copies ciegamente esos campos al crear
una idea nueva. `parent_ids` permite rastrear parentesco, no prioridad ni dependencia.

## Interacción entre rondas

Una primera respuesta útil puede tener esta forma:

«El proyecto ya permite A y B; todavía tengo incertidumbre sobre C. Esta ronda
explora resultados nuevos, no ajustes de esos controles.

**I001 — Feature concreta.** Permitiría X para Y. Se diferencia de A en Z.
[Demo local].

**I002 — Otra feature concreta.** ...

¿Cuáles explorarías y cuáles descartarías?»

No presentes enlaces antes de crear los archivos. No pidas elegir una sola idea
si al usuario le interesan varias. Para «más», proponé otra ronda sin exigir cerrar
la anterior. Para «profundizá I002», usá una demo comparativa o variante y una
pregunta centrada en la experiencia; no derives a un diseño de arquitectura.

## Decisiones y cierre

El silencio mantiene `proposed`. Una solicitud de profundización admite `exploring`.
`Saved`, `parked` y `discarded` necesitan una reacción del usuario, no tu preferencia.
Se permite volver desde cualquier estado con una decisión explícita y trazabilidad.

Al retomar, leé tanto las ideas guardadas como los descartes y sus razones.
Podés volver a una descartada si el usuario lo pide o aparece evidencia nueva
importante, pero anunciá el motivo y su relación con la idea anterior.

No crees tareas por cerrar la sesión. La salida es: ideas conservadas, prototipos,
decisiones y preguntas abiertas. Si luego piden planificar una idea, separá ese
pedido del modo de descubrimiento. Si piden implementarla, verificá el alcance
explícito: el resto de las ideas sigue sin autorización.

## Resumen de continuidad

Al terminar una ronda, conservá en el contexto: tema explorado, reacciones explícitas,
ideas aún sin decidir y áreas que el usuario pidió explorar después. Son notas de
conversación, no tareas. No arrastres restricciones específicas de un proyecto a
otro sin evidencia. Para referir ideas de otra sesión usá su sesión e ID completos.

Interpretá «dale», «sigamos» y «me gusta» con el alcance ya autorizado. Por sí solos
no convierten una exploración en implementación. Un pedido de plan cambia la etapa
y conserva su límite; una autorización de implementación permite continuar sin
pedirla otra vez. Ni favoritos ni filtros del índice representan permisos.
