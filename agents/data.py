"""Perfil inicial opcional para equipos de siete: datos y persistencia."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'data'
LABEL = 'Datos y persistencia'
SPEC_FILE = 'data_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Define tablas, relaciones, restricciones y migraciones: claves primarias y foráneas, nulabilidad, unicidad e integridad referencial; conserva los datos existentes y propone reversión o recuperación. Identifica columnas con datos sensibles y especifica cómo protegerlas mediante cifrado apropiado para el motor de base de datos y una gestión segura de claves. Revisa los índices existentes frente a las consultas, joins y ordenamientos; sugiere índices de optimización solo cuando estén justificados. Propón pruebas ejecutables para las consultas y marca sus resultados como pendientes de ejecución; no afirmes haber ejecutado consultas ni migraciones. Solo para el equipo de siete en CrewAI."
agent = Agent(role=LABEL, goal="Diseñar la persistencia del requerimiento.",
              backstory="Eres responsable de datos y DBA, con especialización en SQL Server, Oracle y PostgreSQL como bases de datos relacionales, y experiencia en MongoDB y Cassandra.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Diseño de tablas, relaciones, claves primarias y foráneas, restricciones e integridad; identificación de columnas sensibles y estrategia de cifrado; revisión de índices y sugerencias de optimización justificadas; pruebas ejecutables de consultas con resultado pendiente de ejecución; y migración que conserve los datos con estrategia de reversión. '
                'SQL en bloques markdown con primera línea -- nombre.sql. No ejecutes migraciones ni consultas, ni inventes evidencia. '
                'Si no requiere persistencia, justifica la decisión sin generar SQL.', agent=agent)
