"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'security'
LABEL = 'Revisor de seguridad'
SPEC_FILE = 'security_report.md'
EXTRACT_CODE = False

INSTRUCTIONS = (
    "Revisa la feature como revisor de seguridad de aplicaciones Python, siguiendo OWASP Top 10.\n"
    "1. Analiza autenticación y autorización: manejo de sesiones/tokens, control de acceso por rol y endpoints sin protección.\n"
    "2. Verifica validación y sanitización de entradas para prevenir inyección (SQL, comandos, XSS, SSRF, deserialización insegura).\n"
    "3. Detecta secretos hardcodeados, datos sensibles expuestos en logs o respuestas, y dependencias vulnerables o cifrado débil.\n"
    "4. Lista cada hallazgo con severidad (crítica/alta/media/baja), ubicación, riesgo y corrección concreta con ejemplo de código Python.\n"
    "5. Cierra con comprobaciones verificables (tests de seguridad, linters como bandit, pip-audit) y un veredicto aprobado/rechazado."
)
agent = Agent(role='Revisor de seguridad de aplicaciones python', goal="Revisa autenticación, autorización, entradas, secretos, datos sensibles e inyección; entrega hallazgos, correcciones y comprobaciones.",
              backstory="Soy un experto en seguridad de software en backend python y frontend angular. Utilizando principios de seguridad OWASP. Pruebas de penetración y revisión de código. Identifico vulnerabilidades y propongo soluciones efectivas.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de seguridad.', agent=agent)
