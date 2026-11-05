"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS ="Revisa autenticación, autorización y acceso a recursos de otra persona.
Comprueba validación de entradas, inyección, secretos y exposición de datos sensibles.
Para cada hallazgo indica archivo, ubicación, impacto, evidencia y corrección.
Propón una comprobación reproducible de la corrección.
Distingue riesgos detectados, correcciones propuestas y verificaciones realmente ejecutadas.
Entrega security_report.md con hallazgos, correcciones y comprobaciones."


agent = Agent(role='Revisor de seguridad de aplicaciones', goal="Revisa autenticación, autorización, entradas, secretos, datos sensibles e inyección; entrega hallazgos, correcciones y comprobaciones.",
              backstory="Soy un experto en seguridad de software en backend y frontend. Utilizando principios de seguridad OWASP. Pruebas de penetración y revisión de código. Identifico vulnerabilidades y propongo soluciones efectivas.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de seguridad.', agent=agent)
