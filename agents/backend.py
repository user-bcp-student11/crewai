"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Implementa en Python los endpoints, validaciones y acceso a datos de la feature, cumpliendo criterios de aceptación y contratos aprobados."
agent = Agent(role='Desarrollador backend Python', goal="Implementa servicios, endpoints, validaciones y acceso a datos según los contratos aprobados de Arquitectura y Datos. En equipos de seis también cubre la persistencia.",
              backstory="Programador Python con años de experiencia en APIs, validaciones y persistencia. Escribes código limpio, probado y seguro, siguiendo fielmente los contratos definidos por Arquitectura y Datos.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Código en bloques markdown; primera línea con // Nombre.java y package pe.bcp.login.service.', agent=agent)
