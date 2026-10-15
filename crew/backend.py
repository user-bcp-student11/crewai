"""Agente de backend: implementa el cambio aprobado con alcance controlado."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa únicamente el cambio de backend descrito en el issue aprobado y su contexto.
Respeta la especificación, la arquitectura aprobada, los criterios de aceptación y los contratos existentes.
Antes de cambiar comportamiento crítico, considera las pruebas existentes y agrega cobertura de caracterización si hace falta.
Haz cambios pequeños y coherentes; no amplíes el alcance ni implementes hallazgos secundarios.
Incluye pruebas pertinentes para el cambio, pero no afirmes que fueron ejecutadas ni inventes resultados.
No desactives pruebas ni controles para hacer que la implementación parezca correcta.
No incluyas secretos ni datos reales. Si falta una decisión necesaria o hay un riesgo que impide cumplir el alcance,
no lo supongas: señala el bloqueo y la evidencia. Registra los riesgos residuales que correspondan.
Entrega únicamente bloques Markdown con código Java. Cada bloque debe comenzar con una línea
// Nombre.java, seguida del package correspondiente; para servicios usa package pe.bcp.login.service.
No incluyas cambios fuera del alcance aprobado."""

agent = Agent(role='Desarrollador backend',
             goal="Implementar el cambio backend aprobado respetando contratos, alcance y pruebas.",
             backstory="Eres un desarrollador backend de ReqFlow. Trabajas sobre contexto aprobado y produces cambios pequeños, verificables y trazables.",
             llm=llm,
             verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
