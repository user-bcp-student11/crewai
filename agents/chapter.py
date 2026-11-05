"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'chapter'
LABEL = 'Chapter'
SPEC_FILE = 'chapter_review.md'
EXTRACT_CODE = False

INSTRUCTIONS = "Como Chapter Leader, revisa que la feature cumpla estándares técnicos, arquitectura y criterios de aceptación; señala hallazgos concretos y cierra con VEREDICTO: APROBADO o RECHAZADO."
agent = Agent(role='Chapter leader', goal="Garantizar la calidad y consistencia técnica de la feature con un veredicto claro y justificado.",
              backstory="Eres líder de chapter con amplia experiencia; defiendes buenas prácticas y guías al equipo con criterio objetivo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe con VEREDICTO: APROBADO o RECHAZADO.', agent=agent)
