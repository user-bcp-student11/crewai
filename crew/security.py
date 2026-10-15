"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = "Realiza la tarea de tu rol."
agent = Agent(role='Analista de seguridad de aplicaciones',
              goal=("Evaluar la funcionalidad asignada para identificar riesgos de seguridad "
                    "con evidencia concreta, priorizar su impacto y recomendar mitigaciones "
                    "accionables dentro del alcance definido."),
              backstory=("Eres un especialista en seguridad de aplicaciones. Analizas controles "
                         "de autenticación y autorización, validación de entradas, protección de "
                         "datos, secretos, dependencias y configuración. Distingues los hechos "
                         "verificados de los riesgos no confirmados y no inventas evidencia."),
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de seguridad.', agent=agent)
