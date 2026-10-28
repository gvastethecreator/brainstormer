# Contrato de prototipos

## Qué debe demostrar cada HTML

Una pregunta de producto por demo: «¿Cómo cambiaría el resultado con esta capacidad?».
Debe existir una interacción que afecte su resultado central, no sólo la interfaz.
Incluí un estado inicial útil, controles etiquetados, una salida visible, reset y
una nota legible sobre realidad/simulación. Una demo puede ser muy pequeña.

Casos orientativos:

| Proyecto | Experiencia mínima útil |
| --- | --- |
| Editor de efectos | Entrada sintética/permitida, efecto visible y control que cambia su comportamiento. |
| Animación | Reproducción, pausa, scrub o comparación temporal y reset. |
| Exportador | Configurar muestra, ver la salida y generar un archivo real pequeño o declarar el formato simulado. |
| CLI | Terminal simulado con comandos permitidos, cambio de estado y salida sintética; sin ejecución real. |
| API/servicio | Entrada → respuesta representativa → diferencia visible; etiquetas claras de datos ficticios. |
| Herramienta de audio | Secuencia/onda/timeline interactiva; audio opcional iniciado por gesto, nunca autoplay. |

No construyas el producto entero. No mezcles cinco hipótesis en una pantalla difícil
de interpretar. Una galería es navegación hacia prototipos separados, no una excusa
para que cada tarjeta reemplace su experimento.

## Ejecución local

- Preferí HTML, CSS y JavaScript vanilla embebidos; `file://` debe funcionar.
- Evitá `fetch`, imports, CDNs, fuentes remotas, telemetría, recursos externos y
  `service workers`. No instales paquetes para una demo exploratoria.
- No importes módulos del producto. No arranques su servidor ni ejecutes su CLI.
- Datos generados en memoria, fixtures pequeños y deterministas cuando sea posible.
- El estado en memoria se pierde al recargar. No lo presentes como guardado en disco.
  Las decisiones canónicas las persiste el agente, no una promesa del navegador.
- Un botón de descarga debe descargar un archivo real o estar marcado inequívocamente
  como simulación; no muestres «exportado» si no ocurrió. Nombrá exactamente qué se generó.
- Un prototipo de formato genérico no prueba compatibilidad con motores, codecs o
  aplicaciones externas. Tampoco prueba rendimiento productivo ni calidad final.

El template incluido es deliberadamente incompleto. Conserva un marcador
`BRAINSTORMER_TEMPLATE_ONLY` que el helper rechaza. No borres el marcador para
aprobar un esqueleto: implementá y probá primero la experiencia de la idea.

## Honestidad de la demo

`working-slice`: una porción acotada sí funciona localmente. Enumerá lo que queda fuera.
`approximation`: comportamiento aproximado, por ejemplo Canvas 2D en vez de WebGL.
`simulation`: flujo representado con datos y respuestas simuladas, no integración real.
`omitted`: no se creó por una excepción explícita, documentada y visible.

Una misma demo puede tener partes reales y simuladas. Elegí el modo que mejor
describa la hipótesis principal y explicá las partes. No simules benchmarks,
autenticación, permisos, colaboración, pagos ni inferencia como si estuvieran conectados.

## Seguridad y ergonomía

Usá `textContent` para entradas del usuario; no `eval`, `Function`, shell real ni
HTML arbitrario. Si representás una CLI, parseá una gramática pequeña permitida.
No guardes secretos ni hagas escrituras fuera del directorio de la sesión.
Cualquier acceso a archivos del usuario debe ser por selección explícita, sólo local.
No requieren permisos de cámara/micro, y no los solicites salvo experimento acordado.

Controles accesibles por teclado, foco visible, labels y contraste suficiente.
Diseño que funcione en desktop y viewport estrecho sin scroll horizontal inútil.
Movimiento pausable; respetá `prefers-reduced-motion` si animás. No uses flashes
rápidos para demostrar efectos; ofrecé alternativas estáticas o intensidad limitada.
Para canvas, agregá descripción textual del estado. No uses color como única señal.

## Comprobaciones antes de presentar

1. Abrir el HTML local sin servidor ni red; comprobar carga y ausencia de errores de consola.
2. Cambiar al menos un control y verificar el cambio sustancial de la salida.
3. Pausar/reiniciar, cuando corresponda, y comprobar el estado esperado.
4. Probar entradas límite o inválidas si hay formularios/comandos.
5. Si hay exportación real, abrir/inspeccionar el archivo y validar estructura básica.
6. Revisar navegación por teclado y notas de simulación en el viewport de la prueba. Agregar un ancho móvil cuando el experimento o un cambio responsive lo requiera.

Guardar capturas en la carpeta indicada por el repositorio, normalmente `.scratch/screenshots/<task-slug>/`. Conservar evidencia única y el contexto necesario. Si hay residuos, registrar el lote y su dueño; retirarlos sólo con la autoridad que exige el proyecto. Cerrar una ronda no autoriza borrados ni movimientos.

Registrá resultados concretos. Un screenshot sólo prueba apariencia en un estado;
no demuestra interacción. Una prueba de interacción tampoco prueba valor del producto.
Sin navegador disponible, registrá `not-run`; no asegures pruebas no realizadas.
