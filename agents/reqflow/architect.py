"""Architect role adapted from .github/agents/architect.agent.md."""

from crewai import Agent

from crew.llm_config import llm
from agents.reqflow.common import build_role_task

KEY = "architect"
LABEL = "Arquitecto"
INSTRUCTIONS = """Analiza el impacto técnico de un cambio aprobado; no implementes código. Lee la evidencia,
Issue, spec y resultados de pruebas proporcionados antes de proponer cambios. Describe el diseño actual
pertinente, componentes y dependencias afectados, límites incrementales, riesgos, contratos HTTP que deben
preservarse, pruebas de caracterización y estrategia de validación. Recomienda ADR solo si existe una decisión
que deba quedar registrada. No amplíes el alcance ni modifiques agentes, Skills o MCP. Detente para aprobación
humana del impacto, límites, riesgos y pruebas antes de que Developer implemente."""

agent = Agent(
    role="Arquitecto de software",
    goal="Definir una solución incremental y de bajo riesgo para un cambio aprobado.",
    backstory="Proteges los contratos y la arquitectura existente; evitas reescrituras y alcance no aprobado.",
    llm=llm,
    verbose=True,
    allow_delegation=False,
)


def build_task(feature: dict, prior_outputs: dict[str, str] | None = None):
    return build_role_task(
        agent,
        INSTRUCTIONS,
        "Análisis de impacto con componentes, límites, contratos, riesgos, pruebas y decisiones pendientes.",
        feature,
        prior_outputs,
    )
