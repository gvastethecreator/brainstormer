# Filtro de features — capacidades, no tareas

Usar al seleccionar una ronda; no es un score de negocio ni un ranking automático.

## La frase que debe poder completar cada opción

«Para [persona y situación], permitir [acción nueva] produce [resultado útil]
que hoy requiere [alternativa real / paso manual / capacidad no encontrada].»

La última parte exige evidencia o incertidumbre explícita. Un ejemplo inventado
sirve como hipótesis, no como prueba de una limitación real del producto.

## Cuatro diferencias que no hay que confundir

| Tipo | Ejemplo | Tratamiento |
| --- | --- | --- |
| Mantenimiento | Corregir un crash al exportar | Fuera de esta sesión, salvo bloqueo breve. |
| Ajuste incremental | Un preset de un efecto ya disponible | No alcanza por sí solo. |
| Capacidad nueva | Muestrear instantes distintos por zona de una imagen | Candidata si cambia la posibilidad expresiva. |
| Flujo nuevo | Entregar frames y coordenadas como atlas | Candidata si abre un destino útil, no por tener otra extensión. |

No rechaces efectos pequeños porque son fáciles de implementar. No aceptes una
feature sólo porque es ambiciosa. Considerá cambios sustanciales en resultados,
no líneas de código, cantidad de pantallas o presencia de IA.

## Selección de una ronda

Explorá más candidatas que las que mostrás. Descartá las que ya existen, los clones
semánticos, las ideas sin usuario concreto y las que sólo agregan gestión o UI.
Elegí opciones con diferencias observables y respetá la cantidad pedida. Si faltan
candidatas sólidas, explicá el límite; no rellenes con duplicados ni cambies el
alcance silenciosamente.

Variar fuentes, efectos, tiempo, composición y salidas es una forma de explorar,
no una obligación de cubrir categorías. Una ronda sólo de efectos es válida:
cada opción tiene comportamiento, caso de uso y HTML propios.

Ejemplos de formulación:

- No: «Nuevos efectos». Sí: «Desfase temporal por franjas: cada zona muestra un
  instante distinto; permite convertir movimiento en una deformación temporal».
- No: «Animaciones mejores». Sí: «Componer ciclos con inicio y final compatibles,
  con comparación visible de la unión». No implica que el producto carezca de loops.
- No: «Exportar a más sitios». Sí: «Atlas regular con alpha y coordenadas para
  reutilizar una animación fuera del editor», contrastando primero las salidas reales.
- No: «Una CLI más fácil». Sí: «Recetas parametrizadas que permiten ensayar una
  transformación sobre un conjunto de entradas y comparar sus resultados».

## Riesgos sin convertir la sesión en un plan

Mencioná una incertidumbre determinante cuando importe: coste de servicio,
privacidad, permiso de hardware, compatibilidad de salida, tamaño de datos o
incoherencia con el público. No hagas tickets, arquitectura, cronogramas o
estimaciones. El prototipo prueba una experiencia, no esas garantías.

No ofrezcas marketplace, colaboración, inteligencia artificial o monetización
como defaults universales. Tampoco los prohíbas si existe una razón específica
y evidencia de valor en el proyecto: exigí el mismo filtro que a otras features.

## Reacción del usuario

Una ronda puede conservar varias ideas. No fuerces un ganador. Profundizar quiere
decir probar una diferencia, variante, combinación o caso de uso; no discutir
variables, endpoints o implementación. No interpretes el silencio como rechazo.

«Guardemos todo» conserva las opciones, no crea un backlog. «Hacé el plan de I003»
permite un handoff a planificación fuera de la sesión; no permite ejecutar ese plan.
«Más» no obliga a decidir lo anterior. «Dale» continúa la acción exploratoria actual.

Al volver a una idea descartada por una razón nueva, reconocé explícitamente su
historial y la diferencia. No la vuelvas a presentar con otro nombre como inédita.
Usá identificadores de sesión + idea al comparar ideas de sesiones diferentes.
