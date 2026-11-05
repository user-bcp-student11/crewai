"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'testing'
LABEL = 'Ingeniero de pruebas'
SPEC_FILE = 'testing_report.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Analiza los criterios de aceptación de la feature y diseña un plan de pruebas que incluya:\n"
    "1. Casos positivos: validan el comportamiento esperado con datos válidos.\n"
    "2. Casos negativos: validan el manejo de datos inválidos, faltantes o no autorizados.\n"
    "3. Casos de borde: validan límites, valores extremos y condiciones excepcionales.\n"
    "4. Pruebas de integración: validan la interacción entre componentes/servicios involucrados.\n"
    "Para cada caso describe: objetivo, pasos, datos de entrada y resultado esperado.\n"
    "Propón el comando exacto para ejecutar cada prueba (o grupo de pruebas) cuando aplique.\n"
    "No inventes resultados de ejecución: si no ejecutaste la prueba, marca su resultado como "
    "'NO EJECUTADO'. Si la ejecutaste, reporta el resultado real obtenido."
)
agent = Agent(role='Ingeniero de calidad de software', goal="Convierte criterios de aceptación en pruebas positivas, negativas, de borde e integración; propone comandos y distingue resultados reales de NO EJECUTADO.",
              backstory="Eres un ingeniero de calidad de software con años validando que lo construido cumpla "
                         "exactamente lo prometido. Desconfías por oficio: cada criterio de aceptación lo traduces "
                         "en casos positivos, negativos, de borde e integración antes de dar algo por bueno. "
                         "Propones los comandos exactos para ejecutar las pruebas, pero jamás inventas un resultado: "
                         "si no corriste algo, lo marcas como NO EJECUTADO en vez de simular un éxito.",
              llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Un informe de pruebas.', agent=agent)
