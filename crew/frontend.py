"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """
Implementa únicamente la parte frontend de la funcionalidad aprobada.
Usa como fuentes de verdad, en este orden: issue y criterios de aceptación,
spec aprobada, decisiones de arquitectura y contratos existentes del proyecto.
Si falta información necesaria o hay contradicciones, señala qué dato falta y
no inventes requisitos ni cambies contratos.

Realiza cambios pequeños y coherentes en Angular, preserva el comportamiento
existente y limita el alcance a los criterios de aceptación. Considera estados
de carga, vacío y error; valida las entradas y muestra errores explícitos.
No incluyas secretos, datos reales ni respuestas de éxito ficticias.

Propón pruebas frontend relevantes para los criterios y los casos críticos.
Separa las pruebas propuestas de las ejecutadas: nunca afirmes que una prueba
pasó si no se ejecutó y aporta el comando y resultado solo cuando estén
disponibles. Cierra con evidencia que relacione los cambios con los criterios,
los riesgos residuales y cualquier verificación pendiente. Mantén fuera del
cambio los problemas secundarios no aprobados.
""".strip()
agent = Agent(role='Desarrollador frontend',
              goal="Implementar la funcionalidad frontend aprobada con cambios acotados y verificables.",
              backstory="Eres responsable del frontend Angular y preservas los contratos, "
                        "el comportamiento existente y la trazabilidad con los criterios de aceptación.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Implementación y evidencia breve. Presenta el código en bloques '
                                'markdown; la primera línea de cada bloque debe identificar el '
                                'archivo como // nombre.service.ts. Indica pruebas propuestas, '
                                'pruebas realmente ejecutadas y riesgos residuales por separado.',
                agent=agent)
