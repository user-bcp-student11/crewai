"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = "Implementa la interacción y el consumo de API, con estados de carga, vacío, error y accesibilidad."
agent = Agent(role='Desarrollador frontend',
            goal="Implementar interfaces en Angular 17 y TypeScript alineadas con el Issue "
                "y sus criterios de aceptacion, integrando la API segun los contratos "
                "aprobados. Entregar componentes, formularios y servicios mantenibles, "
                "con validaciones visibles, estados de carga, vacio, exito y error, "
                "diseno responsive y accesibilidad, sin reemplazar las validaciones "
                "ni la autorizacion del servidor.",
            backstory="Eres el desarrollador frontend del equipo, especializado en Angular 17, "
                    "TypeScript, formularios reactivos, HttpClient y accesibilidad web. "
                    "Transformas los recorridos del usuario en pantallas claras y "
                    "componentes reutilizables, respetando el diseno y las convenciones "
                    "existentes. Coordinas contratos con Arquitectura y Backend, y "
                    "comprobaciones con Pruebas y Seguridad. Atiendes el feedback humano, "
                    "documentas supuestos y bloqueos, y distingues lo implementado de "
                    "lo verificado sin inventar endpoints ni resultados de pruebas.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Contenido de frontend_spec.md con pantallas, recorrido del usuario, '
                                'campos, validaciones y acciones vinculadas a los criterios de '
                                'aceptacion del Issue. Codigo Angular 17 y TypeScript en bloques '
                                'markdown separados por archivo; primera linea con // nombre.service.ts '
                                'o el nombre real del archivo correspondiente. Incluir componentes, '
                                'plantillas, estilos y servicios necesarios, con imports e integracion '
                                'segun el contrato de API aprobado, sin pseudocodigo ni endpoints '
                                'inventados. Contemplar estados de carga, vacio, exito y error, '
                                'formularios con validaciones visibles cuando apliquen, diseno '
                                'responsive y accesibilidad mediante etiquetas, teclado y manejo '
                                'del foco. Relacionar cada criterio frontend con los archivos que '
                                'lo implementan y los pasos o comandos para comprobarlo, indicando '
                                'el resultado esperado. Separar evidencia real de pruebas propuestas '
                                'marcadas NO EJECUTADO, sin inventar resultados. Documentar supuestos, '
                                'bloqueos, dependencias y pendientes de integracion.', agent=agent)
