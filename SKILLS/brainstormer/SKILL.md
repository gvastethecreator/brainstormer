---
name: brainstormer
description: "Product feature discovery. Use to explore new capabilities in an existing project with concrete ideas and small interactive prototypes."
compatibility: "Full sessions need project reads and local writes. Offline HTML previews use a browser; the optional helper needs Python 3.10+ and its standard library."
metadata:
  version: "1.1.0"
  language: es
---

# Brainstormer

Explorá qué capacidades nuevas merece la pena agregar a un producto. Convertí las ideas en experiencias pequeñas que el usuario pueda probar, comparar, conservar o descartar. Usá su idioma y conservá los identificadores técnicos.

## Contrato

- Una feature habilita un resultado, un flujo o una posibilidad expresiva nueva para alguien concreto. La novedad depende de lo que permite hacer, no del tamaño del código.
- Cada opción describe una capacidad específica. «Más efectos» es una categoría; cada efecto propuesto necesita comportamiento, uso y demo propios.
- Una sesión completa escribe en `.scratch/brainstorming/`. El código de las demos está autorizado; integrar la idea en el producto, cambiar configuración o crear tickets requiere un pedido de esa acción.
- «Me gusta», «guardala» o «profundicemos» mantienen la exploración. Si el usuario pide planificar o implementar, cerrar el registro y continuar bajo ese nuevo alcance, reutilizando su autorización.
- Si pide solo ideas o una respuesta en chat, entregar esa ronda sin crear un laboratorio ni prototipos obligatorios. Si pide guardar las ideas, conservar fichas con la omisión del prototipo documentada.

Respetá las rutas del repositorio. Las capturas de navegador usan su carpeta de capturas, separada de las demos; conservá prueba durable solo cuando sea necesaria. Si el repo exige otro dueño para prototipos, usalo y enlazalo desde la sesión. El helper admite su estructura fija: en otra estructura, mantené el registro manualmente.

## Proceso

### 1. Entender el producto y lo ya explorado

Leé reglas, propósito, público, recorrido principal y restricciones. Revisá los registros de capacidades, comandos, entradas/salidas, pantallas o handlers relevantes, junto con documentación y tests. Empezá por índices y fichas de sesiones anteriores; abrí solo los prototipos necesarios para comparar.

Distingí implementado, parcial, documentado, pendiente e incierto. Un nombre de archivo, dependencia o búsqueda vacía no demuestra una capacidad ni su ausencia. Ampliá la inspección solo para comprobar una candidata. Con acceso incompleto, presentá hipótesis y nombrá el alcance revisado.

**Termina cuando:** hay una lectura breve del producto, evidencia de sus capacidades y límites de acceso. Preguntá solo si una decisión ausente cambia de forma sustancial el valor de las propuestas.

### 2. Abrir o retomar la sesión, cuando corresponda

Para una sesión persistente, leé [session-contract.md](references/session-contract.md). Creá una carpeta nueva o retomá la solicitada conservando IDs, decisiones y revisiones. Registrá objetivo, alcance inspeccionado, fuentes y supuestos en `context.md`.

El helper [session.py](scripts/session.py) asigna IDs y mantiene archivos; no inspecciona el producto ni decide novedad. Resolvé `<skill-root>` a la carpeta instalada y consultá `python <skill-root>/scripts/session.py --help`. Aplicá `simple-english`, si está disponible, antes de redactar un brief o plan; conservá el idioma del artefacto.

**Termina cuando:** la sesión tiene contexto suficiente para retomarse. Para una ronda solo en chat, este paso se omite. Sin escritura, entregá las ideas y declaralo; ofrecé archivos solo si la herramienta puede crearlos.

### 3. Filtrar candidatas

Considerá nuevas entradas, transformaciones, comportamiento temporal, composición, salidas, reutilización y dominios adyacentes. Son lentes de búsqueda, no cuotas ni motivos para agregar IA o colaboración por reflejo.

Conservá una candidata si tiene usuario y situación concretos, resultado nuevo, encaje con el producto, diferencia frente a lo existente y una hipótesis que pueda experimentarse. Consultá [feature-filter.md](references/feature-filter.md) cuando el umbral sea dudoso.

Elegí una ronda variada, normalmente de 4–6 ideas o la cantidad pedida. Presentá menos si no hay suficientes ideas sólidas. Los bugs, refactors y ajustes cosméticos pueden ser relevantes, pero no sustituyen la búsqueda de capacidades nuevas. Evitá inventar demanda, ROI o viabilidad.

**Termina cuando:** cada opción tiene valor y diferencia explicables, y la ronda aporta alternativas reales.

### 4. Hacer experimentable cada propuesta

En una sesión con demos, leé [prototype-contract.md](references/prototype-contract.md) antes de construir. Prepará una ficha y un HTML independiente por opción, con una interacción que cambie el resultado central y un reinicio. Usá datos sintéticos o fixtures autorizados y rotulá lo real, aproximado y simulado.

Preferí HTML autocontenido y offline. Una CLI puede representarse con un terminal simulado de comandos limitados; nunca ejecutes shell real desde la demo. Una plantilla incompleta no cuenta como prototipo.

Al cerrar la ronda, abrí cada demo, comprobá su control principal, reinicio y enlaces; revisá consola y red con el navegador disponible. Un screenshot prueba un estado visual, no la interacción. Sin navegador, registrá `not-run` y explicá qué queda sin comprobar.

**Termina cuando:** cada propuesta tiene demo utilizable y evidencia de lo probado, o una omisión pedida o causada por una limitación real.

### 5. Presentar y continuar la exploración

Mostrá la lectura breve del proyecto y, por idea: ID si está guardada, nombre, resultado nuevo, diferencia con lo existente, incertidumbre y enlace real a la demo cuando exista. Pedí una sola decisión ligera sobre la ronda; no obligues a elegir una favorita ni aprobar toda la tanda.

Usá las reacciones para explorar, guardar, descartar, variar o combinar. «Más opciones» abre otra ronda. Evitá cuestionarios de arquitectura, cronogramas o detalles técnicos que todavía no cambian la experiencia.

**Termina cuando:** las opciones se pueden comparar y el usuario entiende qué decisión está abierta.

### 6. Conservar las decisiones

`idea.json` es canónico; `session.json` conserva IDs e historial. `brief.md`, `session.md` e `index.html` son vistas derivadas. El índice permite navegar y filtrar: no promete escribir decisiones en disco desde el navegador.

Los estados son `proposed`, `exploring`, `saved`, `parked` y `discarded`. `saved` conserva una posibilidad; no compromete su construcción. Registrá solo decisiones expresadas: el silencio deja el estado intacto.

Una variante o combinación usa un ID nuevo con `parent_ids`; un refinamiento conserva ID y guarda revisión previa. Actualizá las vistas desde los registros. Leé el contrato de sesión para los comandos y la recuperación de discrepancias.

**Termina cuando:** fichas, demos, índice y decisiones coinciden, o la respuesta en chat deja claro qué se propuso sin persistirlo. Cerrá con lo conservado, la incertidumbre y las pruebas pendientes, sin agregar un roadmap por iniciativa propia.
