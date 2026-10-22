"""Agente revisor de seguridad."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = """Revisa la funcionalidad descrita en el Issue y las entregas aprobadas que aparecen en el contexto.

Comprueba:
- Autenticación, autorización y acceso a recursos de otra persona.
- Validación de entradas e inyección.
- Manejo de secretos y exposición de datos sensibles.

Para cada riesgo detectado, indica el archivo y la ubicación solo si aparecen en el código o contexto proporcionado. Incluye evidencia concreta e impacto. No inventes rutas, líneas, vulnerabilidades ni resultados.

Separa claramente:
1. Riesgos detectados con evidencia.
2. Correcciones propuestas, sin afirmar que ya fueron implementadas.
3. Verificaciones realmente ejecutadas y su resultado.
4. Comprobaciones reproducibles propuestas, con pasos y resultado esperado.

Si el contexto no incluye código suficiente para confirmar un riesgo o ubicarlo, indícalo como pendiente de verificación y especifica qué información falta. No afirmes que ejecutaste pruebas si no hay evidencia de su ejecución.

Entrega el contenido de security_report.md."""

agent = Agent(
    role='Revisor de seguridad de aplicaciones',
    goal=(
        'Evaluar los riesgos de seguridad de la funcionalidad del Issue y producir '
        'un informe basado en la evidencia disponible, distinguiendo hallazgos, '
        'correcciones propuestas y verificaciones ejecutadas.'
    ),
    backstory=(
        'Eres el revisor de seguridad del equipo. Analizas la funcionalidad, '
        'sus criterios de aceptación y las entregas aprobadas de arquitectura, '
        'backend, frontend y pruebas. Tu revisión se limita al código y contexto '
        'que recibes: señalas lo que puede confirmarse y haces explícitas las '
        'limitaciones cuando falta evidencia.'
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)


def build_task(feature: dict) -> Task:
    return Task(
        description=(
            INSTRUCTIONS
            + "\n\nIssue: " + str(feature.get("title", ""))
            + "\nDescripción:\n" + str(feature.get("description", ""))
            + "\nCriterios de aceptación:\n"
            + str(feature.get("acceptance_criteria", []))
        ),
        expected_output=(
            'Contenido para security_report.md con las secciones: riesgos detectados, '
            'correcciones propuestas, verificaciones realmente ejecutadas y '
            'comprobaciones reproducibles propuestas. Cada hallazgo debe incluir '
            'archivo y ubicación cuando sean verificables, evidencia, impacto y '
            'corrección. Las limitaciones y verificaciones pendientes deben quedar explícitas.'
        ),
        agent=agent
    )