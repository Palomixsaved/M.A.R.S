import sys
import os
import json
from datetime import datetime
import pygame
import math
import random

# 1. INICIALIZACIÓN DE PYGAME Y PANTALLA
pygame.init()

ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("M.A.R.S. - Mission Ares Risk Simulator")

directorio_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(directorio_script)
ARCHIVO_FINALES = os.path.join(directorio_script, "finales_desbloqueados.json")

reloj = pygame.time.Clock()
FPS = 60

# COLORES
NEGRO_ESPACIAL = (10, 14, 23)
BLANCO = (240, 240, 240)
NARANJA_MARTE = (226, 88, 34)
AZUL_UI = (20, 110, 190)
VERDE_OK = (46, 204, 113)
VERDE_BRILLANTE = (0, 255, 120)
ROJO_ALERTA = (231, 76, 60)
GRIS_OSCURO = (25, 30, 42)
GRIS_MEDIO = (50, 55, 70)
GRIS_DESHABILITADO = (35, 40, 50)
TEXTO_DESHABILITADO = (110, 115, 125)
AMARILLO = (241, 196, 15)
DORADO_MANDO = (255, 215, 0)  # Color especial para el Mando Superior

# Traducciones de interfaz y contenido visible. Los nombres internos de misiones
# se conservan en español para no alterar la lógica del simulador.
TRADUCCIONES_UI = dict([
    ("M.A.R.S. - Mission Ares Risk Simulator", "M.A.R.S. - Mission Ares Risk Simulator"),
    ("M.A.R.S. - SIMULADOR", "M.A.R.S. - SIMULATOR"), ("ANTES DE DESPEGAR", "BEFORE LAUNCH"),
    ("Completa tu ficha de astronauta junior", "Complete your junior astronaut profile"),
    ("Soy...", "I am..."), ("Y tengo... años (de 1 a 105)", "And I am... years old (1 to 105)"),
    ("Continuar", "Continue"), ("Haz clic en un campo para escribir. Usa Tab para cambiar de campo.", "Click a field to type. Press Tab to switch fields."),
    ("Escribe tu nombre para presentarte.", "Enter your name to introduce yourself."),
    ("La edad debe ser un número entero entre 1 y 105.", "Age must be a whole number from 1 to 105."),
    ("[ TRANSMISIÓN ENTRANTE... ]", "[ INCOMING TRANSMISSION... ]"),
    ("Saltar Texto", "Skip Text"), ("Continuar [Espacio]", "Continue [Space]"),
    ("Partidas guardadas", "Saved Games"), ("Tus partidas guardadas aparecerán aquí.", "Your saved games will appear here."),
    ("fecha desconocida", "unknown date"), ("Guardada: ", "Saved: "), ("  ·  Clic para reanudar", "  ·  Click to resume"),
    ("Página ", "Page "), ("Volver", "Back"), ("Volver al menú", "Return to Menu"),
    ("FALLASTE", "MISSION FAILED"), ("Se agotó un recurso vital de la base.", "A critical base resource ran out."),
    ("REGRESO A CASA", "RETURNING HOME"),
    ("La NASA canceló la expedición por misiones pendientes.", "NASA canceled the expedition because missions were left incomplete."),
    ("Galería de Finales", "Endings Gallery"), ("DÍA ", "DAY "), (" TERMINADO", " COMPLETE"),
    ("Completaste todas tus misiones.", "You completed all your missions."),
    ("La tripulación asegura la base para pasar a la siguiente jornada.", "The crew is securing the base for the next day."),
    ("Iniciar jornada", "Start Day"), ("Iniciar misión", "Start Mission"), ("Iniciar Misión", "Start Mission"),
    ("Enciclopedia de misión", "Mission Encyclopedia"), ("Conceptos descubiertos: ", "Concepts discovered: "),
    ("SALAS", "ROOMS"), ("General", "General"), ("Objetos", "Objects"),
    ("Sala aún no explorada", "Room not explored yet"),
    ("Entra en esta sala durante la misión para desbloquear su descripción.", "Enter this room during a mission to unlock its description."),
    ("La descripción de esta sala se añadirá próximamente.", "A description for this room will be added later."),
    ("DEFINICIÓN GENERAL", "ROOM OVERVIEW"),
    ("Los objetos de esta sala se incorporarán cuando recibamos sus fichas.", "Objects will be added to this room when their entries are available."),
    ("FICHA DEL OBJETO", "OBJECT ENTRY"), ("Concepto bloqueado", "Concept locked"),
    ("Interactúa con este equipo e inicia su minijuego para descubrir la ficha.", "Interact with this equipment and start its minigame to unlock this entry."),
    ("Elige una ficha para leer su definición.", "Choose an entry to read its definition."),
    ("MISIÓN EN PAUSA", "MISSION PAUSED"),
    ("Catálogo de Compañeros", "Crewmate Roster"), (" Elegidos", " Selected"),
    ("NOMBRE:", "NAME:"), ("EDAD:", "AGE:"), ("Edad", "Age"), ("GÉNERO:", "GENDER:"), ("GUSTOS:", "LIKES:"),
    ("OCUPACIÓN:", "ROLE:"), ("VENTAJA:", "PERK:"), ("DESVENTAJA:", "DRAWBACK:"),
    ("Candidato ", "Crewmate "), ("Añadir a Misión", "Add to Mission"),
    ("Quitar de Misión", "Remove from Mission"), ("Límite alcanzado (Max 2)", "Limit reached (Max 2)"),
    ("MISIÓN", "MISSION"), ("Tocar:", "Click:"), ("Módulo:", "Module:"),
    ("Haz CLIC sobre los equipos del fondo para interactuar", "CLICK the equipment in the room to interact"),
    ("Día ", "Day "), ("Tiempo:", "Time:"), ("Alim:", "Food:"), ("Rad:", "Radiation:"),
    ("O2: OK", "O2: OK"), ("Cerrar ▲", "Close ▲"), ("Misiones (9) ▼", "Missions (9) ▼"),
    ("TAREAS DÍA ", "DAY "), (" · Fallos ", " · Missed days "), ("Extra: ", "Extra: "),
    ("Mantén ESPACIO 5 s para saltar el tutorial", "Hold SPACE for 5 seconds to skip the tutorial"),
    ("Siguiente", "Next"), ("Saltar texto", "Skip text"), ("John y Jane · Ayuda rápida", "John & Jane · Quick Help"),
    ("[JOHN] Indicadores", "[JOHN] Resource bars"), ("[JANE] Misiones", "[JANE] Missions"),
    ("[JOHN] Objetos y salas", "[JOHN] Objects and rooms"), ("[JANE] Si necesitas parar", "[JANE] Need a break?"),
    ("Oxígeno, comida y radiación aparecen arriba. Durante el tutorial no bajan; en el día 1 no caen de 30%. Desde el día 2 consumen con normalidad.", "Oxygen, food, and radiation are shown at the top. They stay steady during the tutorial and will not drop below 30% on Day 1. Normal consumption starts on Day 2."),
    ("Abre Misiones. Completa primero las urgentes rojas y después las secundarias grises. El tiempo sigue corriendo mientras trabajas.", "Open Missions. Complete the red urgent tasks first, then the gray secondary tasks. The clock keeps running while you work."),
    ("Pasa el cursor por el equipo y toca el círculo para iniciar su minijuego. Usa A/D o las flechas para cambiar de sala; desde Exterior también puedes tocar los módulos.", "Hover over equipment and click its circle to start a minigame. Use A/D or the arrow keys to change rooms; you can also click the modules from Outside."),
    ("Pulsa ESC para pausar y guardar. Si una barra llega a cero, la misión termina; cuatro días seguidos sin completar las tareas provocan el regreso a casa.", "Press ESC to pause and save. If any bar reaches zero, the mission ends; four consecutive days without completing all tasks send you home."),
    ("Minijuego [", "Minigame ["), ("]: ", "]: "),
    ("Temperatura:", "Temperature:"), ("Objetivo: Equilibrar exactamente en 21.0 °C", "Goal: Set the temperature to exactly 21.0 °C"),
    ("+ Calefacción", "+ Heat"), ("- Aire Acond.", "- A/C"),
    ("Sincroniza el Circadiano: Activa los botones 1 y 3", "Sync the circadian lights: activate buttons 1 and 3"),
    ("Haz Clic sobre las manchas (", "Click the dust spots ("), (" restantes)", " remaining)"),
    ("Arrastra cada Ración a su contenedor por Color", "Drag each food packet to the matching color bin"),
    ("Alinea las 3 barras al centro (50%)", "Align all 3 bars to the center (50%)"),
    ("¡Haz CLIC repetido en el botón para presurizar el Tanque O2!", "CLICK the button repeatedly to pressurize the O2 tank!"),
    ("GIRAR VÁLVULA", "TURN VALVE"), ("Ajusta N2 a ~78% y O2 a ~21%", "Set N2 to ~78% and O2 to ~21%"),
    ("N2:", "N2:"), ("O2:", "O2:"), ("Arrastra y suelta el parche centrado sobre la fuga", "Drag and drop the patch over the leak"),
    ("FUGA SELLADA", "LEAK SEALED"), ("ORIFICIO", "HOLE"), ("PARCHE", "PATCH"),
    ("Centra el parche sobre el orificio rojo.", "Center the patch over the red hole."),
    ("¡Fuga sellada! Buen trabajo.", "Leak sealed! Nice work."), ("OK", "OK"),
    ("Purga en secuencia: Presiona [1] -> [2] -> [3]", "Purge sequence: press [1] -> [2] -> [3]"),
    ("1. Haz Clic en el Cartucho Usado | 2. Clic en la Ranura", "1. Click the used cartridge | 2. Click the slot"),
    ("SATURADO", "SATURATED"), ("¡Ahora haz clic aquí!", "Click here now!"),
    ("Haz Clic en un conector de la izq y luego en su mismo color a la der", "Click a connector on the left, then its matching color on the right"),
    ("MICROIMAGEN 20×  |  Clasifica por tamaño y morfología", "20× MICROSCOPY  |  Classify by size and shape"),
    ("MUESTRA ", "SAMPLE "), ("   ·   Errores: ", "   ·   Errors: "),
    ("¡Buen análisis!", "Good analysis!"), ("¡Clasificación correcta!", "Correct classification!"),
    ("Morfología identificada.", "Shape identified."), ("No coincide. Mira el tamaño y la forma de los granos.", "Not a match. Check the grain size and shape."),
    ("¡Muestras clasificadas!", "Samples classified!"),
    ("Arrastra cada muestra de roca a su caja contenedora", "Drag each rock sample into its container"),
    ("Memoriza y repite la secuencia de colores:", "Memorize and repeat the color sequence:"),
    ("SECUENCIA: [ ", "SEQUENCE: [ "), (" ]", " ]"),
    ("Ajusta las gotas purificadoras hasta equilibrar el pH en 6.5", "Adjust the purifier drops to bring the pH to 6.5"),
    ("pH Cultivo:", "Crop pH:"), ("+ Gotas", "+ Drops"), ("- Gotas", "- Drops"),
    ("Introduce los 3 testigos de suelo en la cámara sellada", "Place all 3 soil cores into the sealed chamber"),
    ("MUESTRAS PROCESADAS:", "SAMPLES PROCESSED:"), ("CÁMARA SELLADA", "SEALED CHAMBER"),
    ("Mueve la Garra con los botones hasta encajar en el marco", "Move the robotic arm with the buttons until it fits the frame"),
    ("Presiona el botón de Carga hasta llegar al 100%", "Press the charge button until it reaches 100%"),
    ("CARGAR", "CHARGE"), ("Ajusta la presión de aire a la zona verde (30 a 35 PSI)", "Adjust air pressure to the green zone (30–35 PSI)"),
    ("Presión:", "Pressure:"), ("+ Inflar", "+ Inflate"), ("- Desinflar", "- Deflate"),
    ("Pasa el escáner sobre las manchas (", "Scan the dust spots ("),
    ("Arrastra las cajas de minerales al depósito de la base", "Drag the mineral boxes to the base storage"),
    ("DEPÓSITO", "STORAGE"), ("Secuencia: [Válvula] -> [Bomba] -> [Puerta]", "Sequence: [Valve] -> [Pump] -> [Door]"),
    ("Arrastra el Parche Térmico sobre la fisura del traje", "Drag the thermal patch over the suit tear"),
    ("Haz Clic en los 3 cierres para dejarlos en VERDE (Bloqueado)", "Click all 3 locks until they turn GREEN (Locked)"),
    ("Presiona el botón de Nitrógeno hasta cargar el Jetpack al 100%", "Press the nitrogen button until the jetpack reaches 100%"),
    ("INYECTAR N2", "INJECT N2"), ("Arrastra el Mosquetón de acero a la Guía de Seguridad", "Drag the steel carabiner to the safety guide"),
    ("GUÍA EVA", "EVA SAFETY GUIDE"), ("Ajusta el nivel de blindaje electromagnético a la zona verde (70-80%)", "Set electromagnetic shielding to the green zone (70–80%)"),
    ("Protección:", "Protection:"), ("Sintoniza la frecuencia de la antena exactamente en 95.0 MHz", "Tune the antenna to exactly 95.0 MHz"),
    ("Frecuencia:", "Frequency:"), ("+ Freq", "+ Freq"), ("- Freq", "- Freq"),
    ("Presiona repetidamente el freno magnético para estabilizar las paletas", "Press the magnetic brake repeatedly to stabilize the vanes"),
    ("FRENAR", "BRAKE"), ("Limpia el polvo marciano de los sensores solar (", "Clean Martian dust from the solar sensors ("),
    ("Sincroniza la medición barométrica: Presiona [1] -> [2] -> [3]", "Sync the barometric reading: press [1] -> [2] -> [3]"),
    ("Válvula", "Valve"), ("Bomba", "Pump"), ("Puerta", "Door"),
    ("Grano fino", "Fine grain"), ("Cristal", "Crystal"), ("Fragmento", "Fragment"),
    ("Geólogo Junior", "Junior Geologist"), ("Especialista ECLSS", "ECLSS Specialist"), ("Comandante", "Commander"),
    ("Rocas y minerales", "Rocks and minerals"), ("Mecánica", "Mechanical systems"), ("Estrategia", "Strategy"),
    ("Geología Planetaria", "Planetary Geology"), ("Comandante de Vuelo", "Flight Commander"),
    ("Elimina 3 misiones normales", "Removes 3 secondary missions"),
    ("Añade 1 urgencia aleatoria de oxígeno, comida o radiación", "Adds 1 random urgent oxygen, food, or radiation task"),
    ("Elimina la misión urgente de comida cada día", "Removes the urgent food task each day"),
    ("Reduce la jornada en 1 minuto", "Shortens the day by 1 minute"),
    ("+2 minutos por jornada", "+2 minutes per day"),
    ("Añade una misión normal que debes completar 3 veces", "Adds a secondary mission that must be completed 3 times"),
    ("Sala Común", "Common Room"), ("Soporte Vital", "Life Support"),
    ("Sala de Experimentos Geofísicos", "Geophysics Lab"), ("Exterior", "Outside"), ("Airlocks", "Airlocks"),
    ("Módulo ECLSS para regular la atmósfera y vigilar el entorno.", "ECLSS module for regulating the atmosphere and monitoring the surroundings."),
    ("Dispensador de raciones (inventario)", "Meal dispenser (inventory)"),
    ("Panel de ciclo de sueño y luces", "Sleep cycle and lighting panel"),
    ("Termostato de conservación de raciones", "Meal storage thermostat"),
    ("Filtro de polvo del rack ECLSS", "ECLSS rack dust filter"), ("Tanque de nitrógeno", "Nitrogen tank"),
    ("Tanque de oxígeno", "Oxygen tank"), ("Válvulas reguladoras y tubería ECLSS", "ECLSS regulator valves and piping"),
    ("Pantalla panorámica y telemetría", "Panoramic observation and telemetry display"),
    ("Cartucho de CO₂ del rack ECLSS", "ECLSS rack CO2 cartridge"),
    ("Muestras recolectadas", "Collected samples"), ("Cableado del brazo robótico automatizado", "Robotic arm wiring"),
    ("Cámara de ingestión de núcleos y suelo", "Core and soil intake chamber"), ("Suite de análisis y microimagen", "Analysis and micro-imaging suite"),
    ("Panel de presurización y despresurización", "Pressurization and depressurization panel"),
    ("Estación de inspección de trajes EVA", "EVA suit inspection station"), ("Casco del traje EVA", "EVA suit helmet"),
    ("Sala Común: dormir y alimentarse", "Common Room: sleep and eat"), ("Airlocks: entrar a la esclusa", "Airlocks: enter the airlock"),
    ("Escudo de radiación", "Radiation shield"), ("Antena telemétrica", "Telemetry antenna"),
    ("Anemómetro de superficie", "Surface anemometer"), ("Sensores solares del rover", "Rover solar sensors"),
    ("Racks de control ambiental", "Environmental control racks"), ("Tanques de gases a alta presión", "High-pressure gas tanks"),
    ("Tanque de nitrógeno", "Nitrogen tank"), ("Tanque de oxígeno", "Oxygen tank"),
    ("Válvulas reguladoras", "Regulator valves"), ("Centro de telemetría y blindaje", "Telemetry and shielding station"),
    ("Brazo robótico automatizado", "Automated robotic arm"), ("Suite de análisis y microimagen", "Analysis and micro-imaging suite"),
    ("El núcleo central del hábitat marciano. Cumple dos misiones conectadas: mantener las condiciones atmosféricas para la tripulación y vigilar el entorno exterior. La radiación varía con la hora local marciana; cuando alcanza niveles elevados, se suspenden las actividades fuera del hábitat y la tripulación se refugia aquí. Los tanques de agua, los suministros de gases y los sistemas vitales concentran masa en este módulo para ofrecer una zona de mayor protección ante eventos de partículas solares (SPE).", "The central core of the Mars habitat supports two connected functions: maintaining the crew's atmosphere and monitoring the outside environment. Radiation levels vary throughout the Martian day. When they rise, outdoor activity stops and the crew shelters here. Water tanks, gas supplies, and life-support systems add shielding mass against solar particle events (SPEs)."),
    ("La sala común reúne los espacios de descanso, alimentación y convivencia. La tripulación duerme aquí para recuperar energía y organiza sus raciones antes de cada jornada.", "The common room brings together crew rest, meals, and shared activities. The crew sleeps here and organizes meal supplies before each workday."),
    ("La sala de experimentos geofísicos recibe regolito y fragmentos de núcleo recogidos en Marte. Sus equipos permiten contener las muestras, prepararlas y observar sus características sin exponer a la tripulación al polvo marciano.", "The geophysics lab receives regolith and core fragments collected on Mars. Its equipment contains and prepares samples for examination while protecting the crew from Martian dust."),
    ("El airlock es una esclusa que separa el hábitat del exterior. Antes de una salida, permite ponerse el traje y controlar la despresurización; al regresar, se presuriza de nuevo para entrar con seguridad.", "The airlock separates the habitat from the outside. Before an excursion, the crew puts on suits and depressurizes the chamber. On return, the chamber is repressurized for a safe entry."),
    ("El exterior reúne el terreno marciano y los equipos expuestos al ambiente. Las salidas se planifican según la radiación y el clima, y se suspenden cuando las condiciones dejan de ser seguras.", "Outside includes the Martian terrain and equipment exposed to the environment. Excursions depend on radiation and weather conditions and stop when it is no longer safe."),
    ("Consolas y equipos del sistema ECLSS. Supervisan la presión y la composición de la atmósfera, y ayudan a mantener condiciones seguras dentro del hábitat.", "ECLSS consoles and equipment monitor atmospheric pressure and composition to help keep conditions safe inside the habitat."),
    ("Reservas presurizadas de oxígeno y nitrógeno. Permiten mantener la mezcla respirable y conservar suministro de emergencia ante una fuga o una avería.", "Pressurized oxygen and nitrogen reserves help maintain a breathable atmosphere and provide emergency supplies during a leak or failure."),
    ("Almacena nitrógeno presurizado, que forma parte de la atmósfera artificial del hábitat.", "Stores pressurized nitrogen, one of the gases in the habitat's artificial atmosphere."),
    ("Almacena oxígeno para sostener la atmósfera respirable y servir como reserva ante fallos del sistema.", "Stores oxygen for the breathable atmosphere and as a reserve in case of system failure."),
    ("Regulan el paso de gas desde los tanques y ayudan a controlar la presión y el equilibrio de la atmósfera interna.", "Control gas flow from the tanks and help regulate pressure and the balance of the internal atmosphere."),
    ("La pantalla grande reúne datos enviados desde la antena exterior mediante un pasamuros estanco. Aquí se vigilan la radiación ionizante y la meteorología de superficie para decidir cuándo es seguro salir.", "The large display gathers data from the outside antenna through a sealed bulkhead. It monitors ionizing radiation and surface weather to help determine when it is safe to go outside."),
    ("Bandejas donde se organizan las porciones de regolito y los fragmentos de núcleo que trae la tripulación. Mantenerlas clasificadas ayuda a no mezclar muestras de distintos lugares.", "Trays hold regolith portions and core fragments brought in by the crew. Keeping them sorted prevents samples from different locations from being mixed."),
    ("Mueve muestras entre las bandejas y los instrumentos de la sala. La manipulación automatizada reduce el contacto directo con el polvo y permite colocar cada muestra con precisión.", "Moves samples between trays and lab instruments. Automated handling limits direct contact with dust and places each sample precisely."),
    ("Compartimento transparente de contención donde se introducen fragmentos de núcleo y regolito. El sistema los procesa de forma controlada para limitar la dispersión de polvo y proteger los equipos y a la tripulación.", "A transparent containment chamber for core fragments and regolith. It processes samples in a controlled way to limit dust spread and protect equipment and crew."),
    ("Pantalla de alta resolución y bandejas de clasificación que permiten observar granos de polvo y arena, comparar su tamaño y estudiar la morfología y textura de los minerales.", "A high-resolution display and sorting trays show dust and sand grains so the crew can compare their size, shape, and mineral texture."),
    ("No hay novedades críticas en el parte matutino. Los recursos bajan a su ritmo habitual.", "No critical updates in the morning report. Resources are being used at their usual rate."),
    ("Un buen comienzo: Jane cambió un filtro anoche. Hoy el oxígeno se mantiene estable y no hay misiones de oxígeno.", "Good news: Jane changed a filter last night. Oxygen will stay stable today, so there are no oxygen missions."),
    ("Aviso de soporte vital: un filtro está muy sucio. El oxígeno se consumirá más rápido; revisa las misiones de la base.", "Life-support alert: a filter is very dirty. Oxygen will run low faster today; check the base missions."),
    ("Buenas noticias: revisaron las raciones y están en buen estado. La comida se mantiene estable y no hay misión de raciones hoy.", "Good news: the meal packs were checked and are in good condition. Food will stay stable, so there is no meal-supply mission today."),
    ("Parte de las raciones se echó a perder. La comida bajará más rápido hoy; prioriza la misión de suministros.", "Some meal packs spoiled. Food will run low faster today; prioritize the supply mission."),
    ("El pronóstico solar está tranquilo y el blindaje quedó revisado. La radiación se mantiene estable; no hay alerta solar hoy.", "Solar conditions are calm and the shielding has been checked. Radiation will stay stable, with no solar alert today."),
    ("El pronóstico marciano marca un pico de radiación. La exposición aumentará más rápido; limita las salidas y atiende el escudo.", "The Martian forecast shows a radiation spike. Exposure will rise faster; limit excursions and check the shield."),
    ("Partida guardada correctamente.", "Game saved successfully."), ("No se pudo guardar: ", "Could not save: "),
    ("Tutorial omitido. ¡Buena suerte en la misión!", "Tutorial skipped. Good luck on the mission!"),
    ("Estación revisada. Sin misiones pendientes aquí.", "Station checked. No pending missions here."),
    ("No hay una misión disponible para este objeto ahora mismo.", "There is no mission available for this object right now."),
    ("Ese equipo no corresponde a la misión elegida. Busca el círculo amarillo que está parpadeando.", "That equipment is not linked to your selected mission. Look for the flashing yellow circle."),
    ("Four días seguidos con misiones pendientes. La NASA cancela la expedición y vuelves a casa.", "Four consecutive days with unfinished missions. NASA cancels the expedition and sends you home."),
    ("La misión terminó con tareas pendientes. La NASA cancela la expedición y vuelves a casa.", "The mission ended with unfinished tasks. NASA cancels the expedition and sends you home."),
    ("Fallaste: se agotó la barra de ", "Mission failed: the "), ("Jornada incompleta (", "Day incomplete ("),
    (")/4). La racha se reinicia si completas todas las misiones de un día.", ")/4). The streak resets when you complete every mission in a day."),
    ("MISIÓN COMPLETADA", "MISSION COMPLETE"), ("Misión Completada!:", "Mission complete:"),
    ("Ronda ", "Round "), (" lista. Repite la misión para completar la tarea extra.", " complete. Repeat the mission to finish the extra task."),
    ("Sin novedades críticas", "No critical updates"), ("Ingresando a:", "Entering:"),
    ("Entrando a ", "Entering "), ("Navegando a ", "Heading to "), (" para: ", " for: "),
    ("Día", "Day"), ("día", "day"), ("misiones", "missions"), ("misión", "mission"),
    ("urgentes", "urgent"), ("urgente", "urgent"), ("secundarias", "secondary"),
    ("comida", "food"), ("oxígeno", "oxygen"), ("radiación", "radiation"),
    ("Módulo", "Module"), ("Ración", "Meal"), ("raciones", "meal packs"),
    ("raciones", "meal packs"), ("Regolito", "Regolith"), ("núcleos", "cores"), ("suelo", "soil"),
    ("Airlock", "Airlock"), ("despresurización", "depressurization"), ("presurización", "pressurization"),
    ("EVA", "EVA"), ("robotico", "robotic"), ("robótico", "robotic"), ("geofísicos", "geophysics"),
    ("Muestras", "Samples"), ("muestras", "samples"), ("Oxígeno", "Oxygen"),
    ("Tanque", "Tank"), ("tanque", "tank"), ("Filtro", "Filter"), ("filtros", "filters"),
    ("Antena", "Antenna"), ("suelo", "soil"), ("Presión", "Pressure"), ("Radiación", "Radiation"),
    ("Inventario", "Inventory"), ("Raciones", "Meal supplies"), ("Sueño", "Sleep"), ("Luces", "Lights"),
    ("Completaste", "You completed"), ("Completada", "Completed"), ("Completado", "Completed"),
    ("Correcto", "Correct"), ("correcta", "correct"), ("Fallaste", "Failed"),
    ("minutos", "minutes"), ("minuto", "minute"), ("restantes", "remaining"),
    ("Aire", "Air"), ("Cámara", "Chamber"), ("cámara", "chamber"), ("Casco", "Helmet"),
    ("Misión", "Mission"), ("misión", "mission"), ("MISIONES", "MISSIONS"),
    ("Urgencia", "Urgent"), ("SECUNDARIA", "SECONDARY"), ("URGENCIA", "URGENT"),
    ("Extra", "Extra"), ("Elegidos", "Selected"), ("ELEGIDOS", "SELECTED"),
    ("DÍA", "DAY"), ("TERMINADO", "COMPLETE"), ("Aún no", "Not yet"),
    ("Presiona", "Press"), ("presiona", "press"), ("Presiona el botón", "Press the button"),
    ("Haz Clic", "Click"), ("Haz clic", "Click"), ("haz clic", "click"), ("Arrastra", "Drag"),
    ("Arrastra y suelta", "Drag and drop"), ("Ajusta", "Adjust"), ("Alinea", "Align"),
    ("Activa", "Activate"), ("Memoriza", "Memorize"), ("repite", "repeat"),
    ("correctamente", "successfully"), ("desconocida", "unknown"), ("Día", "Day"),
])
TRADUCCIONES_UI.update({
    "Iniciar Partida": "Start Game", "Finales": "Endings", "Enciclopedia": "Encyclopedia",
    "Reanudar": "Resume", "Guardar partida": "Save Game", "No hay partidas guardadas todavía.": "There are no saved games yet.",
    "Elige una partida para continuar.": "Choose a saved game to continue.",
    "Partida guardada correctamente.": "Game saved successfully.", "Astronauta": "Astronaut",
    "Guardada:": "Saved:", "Clic para reanudar": "Click to resume",
    "Four días seguidos con misiones pendientes. La NASA cancela la expedición y vuelves a casa.": "Four consecutive days with unfinished missions. NASA cancels the expedition and sends you home.",
    "Día incompleto": "Incomplete day", "Fallaste": "Mission failed",
    "Elige una partida para continuar.": "Choose a saved game to continue.",
    "Muestra ": "Sample ", " sellada en la cámara.": " sealed in the chamber.",
    "Muestra procesada:": "Sample processed:", "Alinea la muestra con la cámara de contención.": "Align the sample with the containment chamber.",
    "La muestra está lista para procesarse.": "The sample is ready for processing.",
    "Conexión completada.": "Connection complete.", "Cable conectado.": "Cable connected.",
    "Tiempo agotado.": "Time's up.", "Buen trabajo.": "Nice work.",
    "No coincide.": "Not a match.", "Clasificación correcta.": "Correct classification.",
    "misión": "mission", "misiones": "missions", "Misión": "Mission", "Misiones": "Missions",
    "MISIÓN": "MISSION", "MISIÓN EN PAUSA": "MISSION PAUSED",
    "Área común de descanso, alimentación y convivencia de la tripulación.": "Shared crew space for rest, meals, and daily life.",
    "Recepción segura y análisis microscópico de regolito y núcleos.": "Safe handling and microscopic analysis of regolith and core samples.",
    "Cámara de esclusa donde se iguala o reduce la presión antes de ponerse los trajes y salir al exterior.": "An airlock chamber where pressure is equalized or lowered before the crew suits up and goes outside.",
    "Monitoreo de radiación solar y viento marciano.": "Monitoring solar radiation and Martian winds.",
    "Es el núcleo central del hábitat marciano. Cumple dos misiones conectadas: mantener las condiciones atmosféricas para la tripulación y vigilar el entorno exterior. La radiación varía con la hora local marciana; cuando alcanza niveles elevados, se suspenden las actividades fuera del hábitat y la tripulación se refugia aquí. Los tanques de agua, los suministros de gases y los sistemas vitales concentran masa en este módulo para ofrecer una zona de mayor protección ante eventos de partículas solares (SPE).": "This is the central core of the Mars habitat, serving two connected roles: maintaining the crew's atmosphere and monitoring the outside environment. Radiation levels vary throughout the Martian day. When they rise, outdoor activity stops and the crew shelters here. Water tanks, gas supplies, and life-support systems add shielding mass against solar particle events (SPEs).",
    "Es el núcleo central del hábitat marciano. Cumple dos misiones conectadas: mantener las condiciones atmosféricas para la tripulación y vigilar el entorno exterior. La radiación varía con la hora local marciana; cuando alcanza niveles elevados, se suspenden las actividades fuera del hábitat y la tripulación se refugia aquí. Los tanques de agua, los suministros de gases y los sistemas vitales concentran masa en este módulo para ofrecer una zona de mayor protección ante eventos de partículas solares (SPE).": "The central core of the Mars habitat supports two connected functions: maintaining the crew's atmosphere and monitoring the outside environment. Radiation levels vary throughout the Martian day. When they rise, outdoor activity stops and the crew shelters here. Water tanks, gas supplies, and life-support systems add shielding mass against solar particle events (SPEs).",
    "Recarga Tanque O2": "Refill the O2 Tank", "Ración Nutricional Vital": "Critical Meal Supply",
    "Ajuste Escudo Radiación": "Adjust Radiation Shield", "Ciclo de Sueño y Luces": "Sleep and Lighting Cycle",
    "Limpieza Filtros de Polvo": "Clean Dust Filters", "Inventario de Raciones": "Meal Inventory",
    "Equilibrio N2/O2": "Balance N2/O2", "Fuga en Tubería": "Repair Pipe Leak",
    "Reemplazo Cartuchos CO2": "Replace CO2 Cartridges", "Conexión de Cables": "Reconnect Robotic Arm Cables",
    "Microscopio de Muestras": "Analyze Samples under the Microscope", "Ingreso de Núcleos y Suelo": "Process Core and Soil Samples",
    "Secuencia Despresurización": "Depressurization Sequence", "Inspección de Trajes": "Inspect EVA Suits",
    "Sellado de Casco": "Seal the Helmet", "Sintonizar Antena": "Tune the Antenna",
    "Calibración Anemómetro": "Calibrate the Anemometer", "Limpieza Sensores Solares": "Clean the Solar Sensors",
    "Día {dia_actual}/14 - Tiempo: {minutos:02d}:{segundos:02d}": "Day {dia_actual}/14 - Time: {minutos:02d}:{segundos:02d}",
    "TAREAS DÍA ": "DAY ", " · Fallos ": " · Missed days ",
    "FINAL FELIZ": "HAPPY ENDING", "FINAL REGRESO": "RETURN ENDING", "FINAL FATAL": "FATAL ENDING",
    "DESBLOQUEADO": "UNLOCKED", "BLOQUEADO": "LOCKED", "Estación Meteorológica": "Weather Station",
    "Aún": "Still", "NOMBRE": "NAME", "DÍA": "DAY", "TERMINADO": "COMPLETE",
    "FINAL DE": "ENDING ", "MISIÓN EN PAUSA": "MISSION PAUSED",
    "Texto bloqueado": "Entry locked", "BLOQ.": "LOCKED", "Astronauta": "Astronaut",
    "Extra del comandante": "Commander's extra mission", "Repeticiones:": "Repetitions:",
    "¡Misión Completada!:": "Mission complete:", "Misión Completada!:": "Mission complete:",
    "¡Misión Completada!: ": "Mission complete: ",
    "4 días seguidos con misiones pendientes. La NASA cancela la expedición y vuelves a casa.": "Four consecutive days with unfinished missions. NASA cancels the expedition and sends you home.",
    "Cuatro días seguidos con misiones pendientes. La NASA cancela la expedición y vuelves a casa.": "Four consecutive days with unfinished missions. NASA cancels the expedition and sends you home.",
    "The time is up": "The time is up",
    "GRANO FINO": "FINE GRAIN", "CRISTAL": "CRYSTAL", "FRAGMENTO": "FRAGMENT",
    "BASALTO": "BASALT", "SULFATO": "SULFATE", "REGOLITO": "REGOLITH",
    "Toca el botón naranja «Misiones»": "Click the orange Missions button",
    "¡Buen trabajo!": "Great job!", "Buen trabajo,": "Nice work,",
    "Guardada:": "Saved:", "Partida guardada ": "Saved game ", "No se pudo guardar:": "Could not save:",
    "Sin novedades críticas en el parte matutino. Los recursos bajan a su ritmo habitual.": "No critical updates in the morning report. Resources are being used at their usual rate.",
    "Un buen comienzo: Jane cambió un filtro anoche. Hoy el oxígeno se mantiene estable y no hay misiones de oxígeno.": "Good news: Jane changed a filter last night. Oxygen will stay stable today, so there are no oxygen missions.",
    "Aviso de soporte vital: un filtro está muy sucio. El oxígeno se consumirá más rápido; revisa las misiones de la base.": "Life-support alert: a filter is very dirty. Oxygen will run low faster today; check the base missions.",
    "Buenas noticias: revisaron las raciones y están en buen estado. La comida se mantiene estable y no hay misión de raciones hoy.": "Good news: the meal packs were checked and are in good condition. Food will stay stable, so there is no meal-supply mission today.",
    "Parte de las raciones se echó a perder. La comida bajará más rápido hoy; prioriza la misión de suministros.": "Some meal packs spoiled. Food will run low faster today; prioritize the supply mission.",
    "El pronóstico solar está tranquilo y el blindaje quedó revisado. La radiación se mantiene estable; no hay alerta solar hoy.": "Solar conditions are calm and the shielding has been checked. Radiation will stay stable, with no solar alert today.",
    "El pronóstico marciano marca un pico de radiación. La exposición aumentará más rápido; limita las salidas y atiende el escudo.": "The Martian forecast shows a radiation spike. Exposure will rise faster; limit excursions and check the shield.",
})
TRADUCCIONES_UI_ORDENADAS = sorted(TRADUCCIONES_UI.items(), key=lambda item: len(item[0]), reverse=True)

def traducir_texto(texto):
    texto = str(texto)
    if texto in TRADUCCIONES_UI:
        return TRADUCCIONES_UI[texto]
    for original, traducido in TRADUCCIONES_UI_ORDENADAS:
        if original in texto:
            texto = texto.replace(original, traducido)
    return texto

class FuenteUI:
    def __init__(self, fuente):
        self.fuente = fuente

    def render(self, texto, *args, **kwargs):
        return self.fuente.render(traducir_texto(texto), *args, **kwargs)

    def size(self, texto):
        return self.fuente.size(traducir_texto(texto))

    def __getattr__(self, nombre):
        return getattr(self.fuente, nombre)

# FUENTES
fuente_titulo = FuenteUI(pygame.font.SysFont("arial", 26, bold=True))
fuente_hud = FuenteUI(pygame.font.SysFont("arial", 15))
fuente_menu = FuenteUI(pygame.font.SysFont("arial", 21, bold=True))
fuente_ficha = FuenteUI(pygame.font.SysFont("arial", 15))
fuente_ficha_bold = FuenteUI(pygame.font.SysFont("arial", 15, bold=True))
fuente_robotica = FuenteUI(pygame.font.SysFont("couriernew", 18, bold=True))

# 2. CARGA DE IMÁGENES SEGURA
def cargar_imagen_segura(nombre):
    try:
        return pygame.image.load(nombre).convert_alpha()
    except Exception:
        surf = pygame.Surface((180, 270))
        surf.fill(GRIS_MEDIO)
        return surf

img_comodin1 = cargar_imagen_segura("Comodin1.PNG")
img_comodin2 = cargar_imagen_segura("Comodin2.PNG")
img_comodin3 = cargar_imagen_segura("Comodin3.PNG")

comodines_catalogo = [
    pygame.transform.smoothscale(img_comodin1, (180, 270)),
    pygame.transform.smoothscale(img_comodin2, (180, 270)),
    pygame.transform.smoothscale(img_comodin3, (180, 270))
]

comodines_modulo = [
    pygame.transform.smoothscale(img_comodin1, (120, 180)),
    pygame.transform.smoothscale(img_comodin2, (120, 180)),
    pygame.transform.smoothscale(img_comodin3, (120, 180))
]

def cargar_fondo(nombre_corto, nombre_largo):
    try:
        img = pygame.image.load(nombre_corto).convert()
    except:
        try:
            img = pygame.image.load(nombre_largo).convert()
        except:
            img = pygame.Surface((ANCHO, ALTO))
            img.fill(GRIS_OSCURO)
    return pygame.transform.smoothscale(img, (ANCHO, ALTO))

def buscar_asset(carpeta, contiene):
    """Busca un asset por nombre dentro de assets_nuevos, incluso si llegó sin extensión."""
    raiz = os.path.join(directorio_script, "assets_nuevos", carpeta)
    clave = contiene.casefold()
    for ruta_actual, _, archivos in os.walk(raiz):
        for archivo in archivos:
            if clave in archivo.casefold():
                return os.path.join(ruta_actual, archivo)
    return None

def cargar_fondo_asset(carpeta, contiene, respaldo):
    ruta = buscar_asset(carpeta, contiene)
    try:
        imagen = pygame.image.load(ruta if ruta else respaldo).convert()
        return pygame.transform.smoothscale(imagen, (ANCHO, ALTO))
    except Exception:
        return pygame.Surface((ANCHO, ALTO))

def cargar_overlay_asset(carpeta, contiene):
    ruta = buscar_asset(carpeta, contiene)
    if not ruta:
        return None
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
        # Las piezas vienen exportadas sobre un lienzo transparente; se conserva su posición relativa.
        return pygame.transform.scale(imagen, (ANCHO, ALTO))
    except Exception:
        return None

def limites_de_superficie(superficie, respaldo):
    """Calcula el área visible directamente desde el canal alfa de un sprite."""
    limites = superficie.get_bounding_rect(min_alpha=1)
    return limites if limites.width and limites.height else respaldo.copy()

fondos_modulos = [
    cargar_fondo("WhatsApp Image 2026-10-15 at 21.11.59.jpeg", "FondoCabina.jpeg"),
    cargar_fondo("fondo_o2.jpeg", "WhatsApp Image 2026-10-15 at 21.12.00.jpeg"),
    cargar_fondo("fondo_laboratorio_muestras.jpeg", "WhatsApp Image 2026-10-15 at 21.12.01.jpeg"),
    cargar_fondo("fondo_rover.jpeg", "WhatsApp Image 2026-10-15 at 21.12.05.jpeg"),
    cargar_fondo("fondo_eva.jpeg", "WhatsApp Image 2026-10-15 at 21.12.02.jpeg"),
    cargar_fondo("fondo_exterior.jpeg", "WhatsApp Image 2026-10-15 at 26.12.01.jpeg")
]

# Fondos nuevos y piezas transparentes recibidas para los sectores.
fondos_modulos[1] = cargar_fondo_asset("soporte_vital", "support_vital_background", "fondo_o2.jpeg")
fondos_modulos[2] = cargar_fondo_asset("geofisica", "05_56_31", "fondo_laboratorio_muestras.jpeg")
fondos_modulos[3] = cargar_fondo_asset("airlocks", "05_51_46", "fondo_rover.jpeg")
fondos_modulos[5] = cargar_fondo_asset("exterior", "exterior_background", "fondo_exterior.jpeg")

overlays_modulos = {
    3: [cargar_overlay_asset("airlocks", "05_51_33")],
    1: [
        cargar_overlay_asset("soporte_vital", "Tanque de Nitrógeno"),
        cargar_overlay_asset("soporte_vital", "Tanque de Oxígeno"),
        cargar_overlay_asset("soporte_vital", "Pantalla de Observación")
    ],
    2: [
        cargar_overlay_asset("geofisica", "Muestras recolectadas"),
        cargar_overlay_asset("geofisica", "Brazo robótico"),
        cargar_overlay_asset("geofisica", "Cámara de ingestión"),
        cargar_overlay_asset("geofisica", "Suite de Análisis")
    ],
    5: [
        cargar_overlay_asset("exterior", "Antena_"),
        cargar_overlay_asset("exterior", "Untitled.png"),
        cargar_overlay_asset("exterior", "Untitled5.png"),
        cargar_overlay_asset("exterior", "Untitled6.png"),
        cargar_overlay_asset("exterior", "Cuarto para dormir"),
        cargar_overlay_asset("exterior", "Sala de Soporte Vital"),
        cargar_overlay_asset("exterior", "Sala de experimentos geofísicos")
    ]
}

datos_catalogo = [
    {
        "id": 0, "nombre": "John Doe", "edad": "42", "genero": "M", "gustos": "Rocas y minerales",
        "ocupacion": "Geología Planetaria",
        "buff": "Elimina 3 misiones normales",
        "nerf": "Añade 1 urgencia aleatoria de oxígeno, comida o radiación"
    },
    {
        "id": 1, "nombre": "Jane Doe", "edad": "35", "genero": "F", "gustos": "Mecánica",
        "ocupacion": "Soporte Vital",
        "buff": "Elimina la misión urgente de comida cada día",
        "nerf": "Reduce la jornada en 1 minuto"
    },
    {
        "id": 2, "nombre": "Jensen Doe", "edad": "48", "genero": "M", "gustos": "Estrategia",
        "ocupacion": "Comandante de Vuelo",
        "buff": "+2 minutos por jornada",
        "nerf": "Añade una misión normal que debes completar 3 veces"
    }
]

# 3. MÓDULOS CON ZONAS INTERACTUABLES
modulos = [
    {
        "id": 0, "nombre": "Sala Común", "tipo": "COMUN",
        "desc": "Área común de descanso, alimentación y convivencia de la tripulación.",
        "comodin_id": None, "pos_comodin": None,
        "hotspots": [
            {"rect": pygame.Rect(500, 350, 200, 150), "etiqueta": "Dispensador de raciones (inventario)", "mision": "Inventario de Raciones"},
            {"rect": pygame.Rect(560, 260, 170, 150), "etiqueta": "Panel de ciclo de sueño y luces", "mision": "Ciclo de Sueño y Luces"},
            {"rect": pygame.Rect(270, 350, 200, 150), "etiqueta": "Termostato de conservación de raciones", "mision": "Ración Nutricional Vital"}
        ]
    },
    {
        "id": 1, "nombre": "Soporte Vital", "tipo": "O2",
        "desc": "Módulo ECLSS para regular la atmósfera y vigilar el entorno.",
        "comodin_id": 1, "pos_comodin": (150, 250),
        "hotspots": [
            {"rect": pygame.Rect(15, 100, 55, 155), "etiqueta": "Filtro de polvo del rack ECLSS", "objetos": ["racks_eclss"], "mision": "Limpieza Filtros de Polvo"},
            {"rect": pygame.Rect(53, 202, 107, 80), "etiqueta": "Tanque de nitrógeno", "objetos": ["tanque_nitrogeno", "tanques_gases"], "mision": "Equilibrio N2/O2"},
            {"rect": pygame.Rect(182, 202, 111, 80), "etiqueta": "Tanque de oxígeno", "objetos": ["tanque_oxigeno", "tanques_gases"], "mision": "Recarga Tanque O2"},
            {"rect": pygame.Rect(75, 163, 190, 38), "etiqueta": "Válvulas reguladoras y tubería ECLSS", "objetos": ["valvulas_reguladoras"], "mision": "Fuga en Tubería"},
            {"rect": pygame.Rect(290, 165, 255, 260), "etiqueta": "Pantalla panorámica y telemetría", "objetos": ["pantalla_telemetria"]},
            {"rect": pygame.Rect(15, 265, 125, 110), "etiqueta": "Cartucho de CO₂ del rack ECLSS", "mision": "Reemplazo Cartuchos CO2"}
        ]
    },
    {
        "id": 2, "nombre": "Sala de Experimentos Geofísicos", "tipo": "GEOFISICA",
        "desc": "Recepción segura y análisis microscópico de regolito y núcleos.",
        "comodin_id": None, "pos_comodin": None,
        "hotspots": [
            {"rect": pygame.Rect(57, 224, 237, 245), "etiqueta": "Muestras recolectadas", "objetos": ["muestras_recolectadas"]},
            {"rect": pygame.Rect(233, 135, 228, 240), "etiqueta": "Cableado del brazo robótico automatizado", "objetos": ["brazo_robotico"], "mision": "Conexión de Cables"},
            {"rect": pygame.Rect(497, 125, 193, 255), "etiqueta": "Cámara de ingestión de núcleos y suelo", "objetos": ["camara_ingestion"], "mision": "Ingreso de Núcleos y Suelo"},
            {"rect": pygame.Rect(672, 94, 215, 375), "etiqueta": "Suite de análisis y microimagen", "objetos": ["suite_microimagen"], "mision": "Microscopio de Muestras"}
        ]
    },
    {
        "id": 3, "nombre": "Airlocks", "tipo": "AIRLOCK",
        "desc": "Cámara de esclusa donde se iguala o reduce la presión antes de ponerse los trajes y salir al exterior.",
        "comodin_id": None, "pos_comodin": None,
        "hotspots": [
            {"rect": pygame.Rect(320, 180, 260, 200), "etiqueta": "Panel de presurización y despresurización", "mision": "Secuencia Despresurización"},
            {"rect": pygame.Rect(100, 320, 140, 120), "etiqueta": "Estación de inspección de trajes EVA", "mision": "Inspección de Trajes"},
            {"rect": pygame.Rect(580, 300, 180, 150), "etiqueta": "Casco del traje EVA", "mision": "Sellado de Casco"}
        ]
    },
    {
        "id": 4, "nombre": "Airlocks", "tipo": "EVA",
        "desc": "Revisión de trajes y equipos de seguridad antes de una actividad extravehicular.",
        "comodin_id": None, "pos_comodin": None,
        "hotspots": [
            {"rect": pygame.Rect(200, 200, 150, 220), "etiqueta": "Rack de Trajes"},
            {"rect": pygame.Rect(550, 220, 160, 180), "etiqueta": "Compuerta EVA"}
        ]
    },
    {
        "id": 5, "nombre": "Exterior", "tipo": "CLIMA",
        "desc": "Monitoreo de radiación solar y viento marciano.",
        "comodin_id": None, "pos_comodin": None,
        "hotspots": [
            {"rect": pygame.Rect(0, 0, ANCHO, ALTO), "etiqueta": "Sala Común: dormir y alimentarse", "destino_modulo": 0},
            {"rect": pygame.Rect(0, 0, ANCHO, ALTO), "etiqueta": "Soporte Vital", "destino_modulo": 1},
            {"rect": pygame.Rect(0, 0, ANCHO, ALTO), "etiqueta": "Sala de Experimentos Geofísicos", "destino_modulo": 2},
            {"rect": pygame.Rect(60, 425, 210, 155), "etiqueta": "Airlocks: entrar a la esclusa", "destino_modulo": 3},
            {"rect": pygame.Rect(180, 220, 200, 150), "etiqueta": "Escudo de radiación", "mision": "Ajuste Escudo Radiación"},
            {"rect": pygame.Rect(520, 180, 220, 180), "etiqueta": "Antena telemétrica", "mision": "Sintonizar Antena"},
            {"rect": pygame.Rect(520, 410, 200, 120), "etiqueta": "Anemómetro de superficie", "mision": "Calibración Anemómetro"},
            {"rect": pygame.Rect(720, 410, 150, 120), "etiqueta": "Sensores solares del rover", "mision": "Limpieza Sensores Solares"}
        ]
    }
]

OBJETOS_POR_MISION = {
    "Recarga Tanque O2": "Tanque de oxígeno",
    "Ración Nutricional Vital": "Termostato de conservación de raciones",
    "Ajuste Escudo Radiación": "Escudo de radiación",
    "Ciclo de Sueño y Luces": "Panel de ciclo de sueño y luces",
    "Limpieza Filtros de Polvo": "Filtro de polvo del rack ECLSS",
    "Inventario de Raciones": "Dispensador de raciones (inventario)",
    "Equilibrio N2/O2": "Tanque de nitrógeno",
    "Fuga en Tubería": "Válvulas reguladoras y tubería ECLSS",
    "Reemplazo Cartuchos CO2": "Cartucho de CO₂ del rack ECLSS",
    "Conexión de Cables": "Cableado del brazo robótico automatizado",
    "Microscopio de Muestras": "Suite de análisis y microimagen",
    "Ingreso de Núcleos y Suelo": "Cámara de ingestión de núcleos y suelo",
    "Secuencia Despresurización": "Panel de presurización y despresurización",
    "Inspección de Trajes": "Estación de inspección de trajes EVA",
    "Sellado de Casco": "Casco del traje EVA",
    "Sintonizar Antena": "Antena telemétrica",
    "Calibración Anemómetro": "Anemómetro de superficie",
    "Limpieza Sensores Solares": "Sensores solares del rover"
}

bibliografia_salas = {
    0: {
        "general": "La sala común reúne los espacios de descanso, alimentación y convivencia. La tripulación duerme aquí para recuperar energía y organiza sus raciones antes de cada jornada.",
        "objetos": []
    },
    1: {
        "general": (
            "Es el núcleo central del hábitat marciano. Cumple dos misiones conectadas: mantener las condiciones "
            "atmosféricas para la tripulación y vigilar el entorno exterior. La radiación varía con la hora local "
            "marciana; cuando alcanza niveles elevados, se suspenden las actividades fuera del hábitat y la tripulación se refugia aquí. Los tanques "
            "de agua, los suministros de gases y los sistemas vitales concentran masa en este módulo para ofrecer "
            "una zona de mayor protección ante eventos de partículas solares (SPE)."
        ),
        "objetos": [
            {
                "id": "racks_eclss", "nombre": "Racks de control ambiental",
                "definicion": "Consolas y equipos del sistema ECLSS. Supervisan la presión y la composición de la atmósfera, y ayudan a mantener condiciones seguras dentro del hábitat."
            },
            {
                "id": "tanques_gases", "nombre": "Tanques de gases a alta presión",
                "definicion": "Reservas presurizadas de oxígeno y nitrógeno. Permiten mantener la mezcla respirable y conservar suministro de emergencia ante una fuga o una avería."
            },
            {
                "id": "tanque_nitrogeno", "nombre": "Tanque de nitrógeno",
                "definicion": "Almacena nitrógeno presurizado, que forma parte de la atmósfera artificial del hábitat."
            },
            {
                "id": "tanque_oxigeno", "nombre": "Tanque de oxígeno",
                "definicion": "Almacena oxígeno para sostener la atmósfera respirable y servir como reserva ante fallos del sistema."
            },
            {
                "id": "valvulas_reguladoras", "nombre": "Válvulas reguladoras",
                "definicion": "Regulan el paso de gas desde los tanques y ayudan a controlar la presión y el equilibrio de la atmósfera interna."
            },
            {
                "id": "pantalla_telemetria", "nombre": "Centro de telemetría y blindaje",
                "definicion": "La pantalla grande reúne datos enviados desde la antena exterior mediante un pasamuros estanco. Aquí se vigilan la radiación ionizante y la meteorología de superficie para decidir cuándo es seguro salir."
            }
        ]
    },
    2: {
        "general": (
            "La sala de experimentos geofísicos recibe regolito y fragmentos de núcleo recogidos en Marte. Sus equipos permiten "
            "contener las muestras, prepararlas y observar sus características sin exponer a la tripulación "
            "al polvo marciano."
        ),
        "objetos": [
            {
                "id": "muestras_recolectadas", "nombre": "Muestras recolectadas",
                "definicion": "Bandejas donde se organizan las porciones de regolito y los fragmentos de núcleo que trae la tripulación. Mantenerlas clasificadas ayuda a no mezclar muestras de distintos lugares."
            },
            {
                "id": "brazo_robotico", "nombre": "Brazo robótico automatizado",
                "definicion": "Mueve muestras entre las bandejas y los instrumentos de la sala. La manipulación automatizada reduce el contacto directo con el polvo y permite colocar cada muestra con precisión."
            },
            {
                "id": "camara_ingestion", "nombre": "Cámara de ingestión de núcleos y suelo",
                "definicion": "Compartimento transparente de contención donde se introducen fragmentos de núcleo y regolito. El sistema los procesa de forma controlada para limitar la dispersión de polvo y proteger los equipos y a la tripulación."
            },
            {
                "id": "suite_microimagen", "nombre": "Suite de análisis y microimagen",
                "definicion": "Pantalla de alta resolución y bandejas de clasificación que permiten observar granos de polvo y arena, comparar su tamaño y estudiar la morfología y textura de los minerales."
            }
        ]
    },
    3: {
        "general": "El airlock es una esclusa que separa el hábitat del exterior. Antes de una salida, permite ponerse el traje y controlar la despresurización; al regresar, se presuriza de nuevo para entrar con seguridad.",
        "objetos": []
    },
    5: {
        "general": "El exterior reúne el terreno marciano y los equipos expuestos al ambiente. Las salidas se planifican según la radiación y el clima, y se suspenden cuando las condiciones dejan de ser seguras.",
        "objetos": []
    }
}
SALAS_BIBLIOGRAFIA_VISIBLES = [3, 5, 2, 1, 0]
MODULO_AIRLOCK_LEGACY = 4

def adjuntar_overlay(modulo_id, termino_archivo, etiqueta):
    imagen = cargar_overlay_asset("soporte_vital" if modulo_id == 1 else "geofisica", termino_archivo)
    if imagen is None:
        return
    zona = pygame.Rect(0, 0, ANCHO, ALTO)
    for hs in modulos[modulo_id]["hotspots"]:
        if etiqueta.casefold() in hs["etiqueta"].casefold():
            hs["sprite"] = imagen
            hs["mask"] = pygame.mask.from_surface(imagen)
            bounds = limites_de_superficie(imagen, zona)
            hs["rect"] = bounds if bounds.width and bounds.height else zona.copy()
            return

adjuntar_overlay(1, "Tanque de Nitrógeno", "nitrógeno")
adjuntar_overlay(1, "Tanque de Oxígeno", "oxígeno")
adjuntar_overlay(1, "Pantalla de Observación", "pantalla panorámica")
adjuntar_overlay(2, "Muestras recolectadas", "muestras recolectadas")
adjuntar_overlay(2, "Brazo robótico", "brazo robótico")
adjuntar_overlay(2, "Cámara de ingestión", "cámara de ingestión")
adjuntar_overlay(2, "Suite de Análisis", "suite de análisis")

# Las piezas transparentes de los sectores del exterior son accesos clicables.
for hs in modulos[5]["hotspots"][:3]:
    indice_sector = {0: 4, 1: 5, 2: 6}[hs["destino_modulo"]]
    hs["sprite"] = overlays_modulos[5][indice_sector]
    if hs["sprite"] is not None:
        hs["mask"] = pygame.mask.from_surface(hs["sprite"])
        bounds = limites_de_superficie(hs["sprite"], hs["rect"])
        if bounds.width and bounds.height:
            hs["rect"] = bounds

conceptos_desbloqueados = {"salas": [], "objetos": []}

# 4. VARIABLES DE ESTADO Y TUTORIAL
estado_juego = "MENU_PRINCIPAL"
estado_anterior_pausa = "JUGANDO"
nombre_jugador = ""
edad_jugador = ""
campo_formulario_activo = "nombre"
indice_catalogo = 0
comodines_elegidos = []

texto_historia_completo = ""
texto_intro_indice = 0.0
VELOCIDAD_TEXTO = 25.0
btn_continuar_intro = pygame.Rect(ANCHO // 2 - 100, ALTO - 90, 200, 45)
campo_nombre_rect = pygame.Rect(ANCHO // 2 - 170, 245, 340, 48)
campo_edad_rect = pygame.Rect(ANCHO // 2 - 170, 325, 340, 48)
btn_confirmar_datos = pygame.Rect(ANCHO // 2 - 120, 410, 240, 48)
mensaje_formulario = ""

# El tutorial habla con los astronautas adultos que el jugador eligió.
def astronautas_tutorial():
    elegidos = [persona for persona in datos_catalogo if persona["id"] in comodines_elegidos]
    # Compatibilidad con partidas antiguas o entrada directa al tutorial sin selección.
    elegidos = elegidos or [datos_catalogo[0], datos_catalogo[1]]
    # En dúos mixtos, el astronauta varón presenta primero y Jane responde después.
    return sorted(elegidos, key=lambda persona: (persona["genero"] != "M", persona["id"]))

def dialogos_tutorial_actuales():
    equipo = astronautas_tutorial()
    textos = [
        "Hey, {nombre}! I'm {first}. Welcome to Mars. It's your first day at the base, so we'll take it one step at a time.",
        "Your three status bars are at the top left: oxygen, food, and radiation. If any one hits zero, we're in serious trouble.",
        "No worries: your resources won't drop while we walk you through things. On Day 1, they won't go below 30%. Starting on Day 2, they drain at the normal rate.",
        "When you complete an urgent mission, we'll restore its critical resource and keep it stable for the rest of the day. Pretty useful, right?",
        "The orange button at the top right opens Missions. Red tasks are urgent, so do those first. Then you can take care of the secondary tasks."
    ]
    return [
        f"[{equipo[i % len(equipo)]['nombre'].upper()}]: " + texto.format(
            nombre=nombre_jugador.strip(), first=equipo[i % len(equipo)]["nombre"].split()[0]
        )
        for i, texto in enumerate(textos)
    ]

def mensajes_tutorial_actuales():
    equipo = astronautas_tutorial()
    textos = {
        "elegir_urgente": "Tap the orange Missions button and choose a red URGENT task. We can't leave those for later.",
        "explicar_urgente": "Red missions handle important base problems. Completing one restores the critical resource it affects. Let's take care of this one first.",
        "hacer_urgente": "You're in the right room. Hover until you find the glowing circle, then click the equipment to start.",
        "elegir_secundaria": "Urgent task done! Now open Missions and choose a gray task. That's a secondary mission.",
        "explicar_secundaria": "Secondary missions help keep the base in good shape. We handle urgent tasks first, then these. Look for the equipment we need in that room.",
        "hacer_secundaria": "That's it! Hover until you find the glowing circle, then click the equipment to start its minigame.",
        "final": "Great work! Urgent tasks first, then the rest. If you get stuck, tap JJ next to Missions to call us. Good luck out there!"
    }
    orden = ["elegir_urgente", "explicar_urgente", "hacer_urgente", "elegir_secundaria", "explicar_secundaria", "hacer_secundaria", "final"]
    return {
        fase: f"[{equipo[(i + 1) % len(equipo)]['nombre'].upper()}]: {textos[fase]}"
        for i, fase in enumerate(orden)
    }

# Cantidad fija de pasos; nombres y voces se resuelven según la tripulación elegida.
DIALOGOS_TUTORIAL_TOTAL = 5
paso_tutorial = 0
texto_tutorial_indice = 0.0
tutorial_activo = True
tutorial_fase = "dialogos"
mision_tutorial_seleccionada = None

bibliografia_seccion = "GENERAL"
bibliografia_modulo = 0
bibliografia_objeto = None
btn_siguiente_tutorial = pygame.Rect(ANCHO - 190, ALTO - 65, 170, 35)
btn_jj = pygame.Rect(670, 10, 48, 35)
btn_cerrar_ayuda_jj = pygame.Rect(ANCHO // 2 + 205, 135, 42, 36)
ayuda_jj_abierta = False

creditos = 5
oxigeno = 100.0
oxigeno_congelado = False
comida = 100.0
comida_congelado = False
radiacion = 100.0
radiacion_congelado = False

dia_actual = 1
DURACION_BASE_DIA = 240.0
duracion_dia_actual = DURACION_BASE_DIA
tiempo_dia = duracion_dia_actual

dias_ignorados_acumulados = 0
panel_misiones_abierto = False

finales_desbloqueados = {
    "FELIZ": False,
    "REGRESO": False,
    "MUERTE": False
}
try:
    with open(ARCHIVO_FINALES, "r", encoding="utf-8") as archivo_finales:
        finales_guardados = json.load(archivo_finales)
    for nombre_final in finales_desbloqueados:
        finales_desbloqueados[nombre_final] = bool(finales_guardados.get(nombre_final, False))
except (OSError, json.JSONDecodeError, AttributeError, TypeError):
    pass

def desbloquear_final(nombre_final):
    if nombre_final not in finales_desbloqueados:
        return
    finales_desbloqueados[nombre_final] = True
    try:
        with open(ARCHIVO_FINALES, "w", encoding="utf-8") as archivo_finales:
            json.dump(finales_desbloqueados, archivo_finales, ensure_ascii=False, indent=2)
    except OSError:
        pass

misiones_del_dia = []
modulo_actual = 0
evento_dia_mensaje = ""
misiones_omitidas_evento = []
multiplicador_oxigeno_dia = 1.0
multiplicador_comida_dia = 1.0
multiplicador_radiacion_dia = 1.0

minijuego_activo = False
mision_en_curso = None
modulo_minijuego_activo = 0
id_minijuego = 1

# Minijuegos Módulo 1
temp_actual = 12.0
btn_calef = pygame.Rect(ANCHO // 2 - 140, ALTO // 2 + 30, 120, 40)
btn_aire = pygame.Rect(ANCHO // 2 + 20, ALTO // 2 + 30, 120, 40)
tiempo_en_target = 0.0

luces_estado = [False, False, False, False]
luces_rects = [pygame.Rect(ANCHO // 2 - 150 + i * 75, ALTO // 2 - 10, 60, 60) for i in range(4)]
manchas_polvo = []
paquetes = []
cajas_destino = []
paquete_arrastrando = None
eq_niveles = [10, 90, 20]
eq_rects = [pygame.Rect(ANCHO // 2 - 100 + i * 80, ALTO // 2 - 50, 40, 120) for i in range(3)]

# Minijuegos Módulo 2
progreso_valvula = 0.0
btn_presionar_valvula = pygame.Rect(ANCHO // 2 - 80, ALTO // 2 + 20, 160, 45)
n2_nivel = 50.0
o2_nivel = 50.0
eq_gas_rects = [pygame.Rect(ANCHO // 2 - 80, ALTO // 2 - 40, 40, 120), pygame.Rect(ANCHO // 2 + 40, ALTO // 2 - 40, 40, 120)]
fuga_rect = pygame.Rect(0, 0, 0, 0)
parche_rect = pygame.Rect(ANCHO // 2 - 160, ALTO // 2 + 50, 50, 50)
parche_arrastrando = False
fuga_reparada = False
feedback_fuga = ""
temporizador_feedback_fuga = 0.0
botones_drenaje = []
secuencia_drenaje_usuario = []
cartucho_saturado = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 - 20, 60, 80)
cartucho_ranura = pygame.Rect(ANCHO // 2 + 60, ALTO // 2 - 20, 60, 80)
estado_co2 = 0

# Minijuegos Módulo 3
cables_izq = []
cables_der = []
conexion_cable_seleccionado = None
conexiones_hechas = []
enfoque_microscopio = 10.0
tiempo_en_enfoque = 0.0
ingesta_muestras = []
ingesta_arrastrando = None
camara_ingesta_rect = pygame.Rect(ANCHO // 2 + 65, ALTO // 2 - 50, 135, 125)
progreso_ingesta = 0
ingesta_procesando = False
temporizador_ingesta = 0.0
feedback_ingesta = ""
temporizador_feedback_ingesta = 0.0
analisis_muestras = []
indice_analisis = 0
errores_analisis = 0
feedback_analisis = ""
temporizador_feedback_analisis = 0.0
rocas = []
cajas_rocas = []
roca_arrastrando = None
secuencia_bio_objetivo = []
secuencia_bio_usuario = []
botones_bio = []
ph_actual = 4.0
btn_ph_mas = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 + 30, 100, 40)
btn_ph_menos = pygame.Rect(ANCHO // 2 + 20, ALTO // 2 + 30, 100, 40)
botones_clasificacion = [
    {"rect": pygame.Rect(ANCHO // 2 - 225 + i * 150, ALTO // 2 + 115, 140, 42), "clase": clase, "lbl": etiqueta}
    for i, (clase, etiqueta) in enumerate((("GRANO FINO", "Grano fino"), ("CRISTAL", "Cristal"), ("FRAGMENTO", "Fragmento")))
]

# Minijuegos Módulo 4
garra_pos = [ANCHO // 2 - 120, ALTO // 2 - 80]
puerto_target = pygame.Rect(ANCHO // 2 + 40, ALTO // 2 - 30, 60, 60)
btn_garra_izq = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 40, 50, 40)
btn_garra_der = pygame.Rect(ANCHO // 2 - 90, ALTO // 2 + 40, 50, 40)
btn_garra_up = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 - 10, 50, 40)
carga_rover = 0.0
btn_cargar_rover = pygame.Rect(ANCHO // 2 - 80, ALTO // 2 + 20, 160, 45)
psi_neumatico = 15.0
btn_psi_mas = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 30, 80, 40)
btn_psi_menos = pygame.Rect(ANCHO // 2 + 20, ALTO // 2 + 30, 80, 40)
manchas_uv = []
cajas_rover = []
deposito_base = pygame.Rect(ANCHO // 2 + 40, ALTO // 2 - 60, 100, 120)
caja_rover_arrastrando = None

# Minijuegos Módulo 5
secuencia_eva_usuario = []
botones_eva = [
    {"rect": pygame.Rect(ANCHO // 2 - 140, ALTO // 2 - 20, 80, 50), "val": 1, "lbl": "Válvula"},
    {"rect": pygame.Rect(ANCHO // 2 - 40, ALTO // 2 - 20, 80, 50), "val": 2, "lbl": "Bomba"},
    {"rect": pygame.Rect(ANCHO // 2 + 60, ALTO // 2 - 20, 80, 50), "val": 3, "lbl": "Puerta"}
]
fisura_traje = pygame.Rect(0, 0, 0, 0)
parche_eva_rect = pygame.Rect(ANCHO // 2 - 160, ALTO // 2 + 50, 50, 50)
parche_eva_arrastrando = False
cierres_casco = [False, False, False]
cierres_rects = [pygame.Rect(ANCHO // 2 - 120 + i * 80, ALTO // 2 - 10, 60, 60) for i in range(3)]
carga_jetpack = 0.0
btn_cargar_jetpack = pygame.Rect(ANCHO // 2 - 80, ALTO // 2 + 20, 160, 45)
mosqueton_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 30, 50, 50)
guia_seguridad = pygame.Rect(ANCHO // 2 + 30, ALTO // 2 - 40, 110, 100)
mosqueton_arrastrando = False

# Minijuegos Módulo 6
nivel_escudo_rad = 20.0
frecuencia_antena = 88.0
btn_freq_mas = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 30, 80, 40)
btn_freq_menos = pygame.Rect(ANCHO // 2 + 20, ALTO // 2 + 30, 80, 40)
freno_viento = 0.0
btn_freno_viento = pygame.Rect(ANCHO // 2 - 80, ALTO // 2 + 20, 160, 45)
polvo_sensores = []
secuencia_press_usuario = []
botones_press = [
    {"rect": pygame.Rect(ANCHO // 2 - 110, ALTO // 2 - 10, 60, 60), "val": 1},
    {"rect": pygame.Rect(ANCHO // 2 - 30, ALTO // 2 - 10, 60, 60), "val": 2},
    {"rect": pygame.Rect(ANCHO // 2 + 50, ALTO // 2 - 10, 60, 60), "val": 3}
]

# Botones UI
btn_lengueta = pygame.Rect(ANCHO - 170, 10, 160, 35)
btn_iniciar = pygame.Rect(ANCHO // 2 - 120, 200, 240, 50)
btn_continuar = pygame.Rect(ANCHO // 2 - 120, 270, 240, 50)
btn_finales = pygame.Rect(ANCHO // 2 - 120, 340, 240, 50)
btn_volver = pygame.Rect(30, ALTO - 70, 120, 40)
btn_reanudar = pygame.Rect(ANCHO // 2 - 120, 250, 240, 50)
btn_menu_pausa = pygame.Rect(ANCHO // 2 - 120, 320, 240, 50)
btn_guardar_pausa = pygame.Rect(ANCHO // 2 - 120, 390, 240, 50)
btn_dia_terminado = pygame.Rect(ANCHO // 2 - 155, 430, 310, 54)
btn_nuevo_dia = pygame.Rect(ANCHO // 2 - 155, 430, 310, 54)
rects_partidas = [pygame.Rect(150, 130 + i * 62, 600, 52) for i in range(6)]
btn_pagina_anterior = pygame.Rect(620, 530, 50, 38)
btn_pagina_siguiente = pygame.Rect(680, 530, 50, 38)
pagina_partidas = 0
btn_bibliografia = pygame.Rect(ANCHO // 2 - 120, 410, 240, 50)
btn_volver_bibliografia = pygame.Rect(25, 535, 150, 42)
tab_bibliografia_general = pygame.Rect(275, 105, 150, 40)
tab_bibliografia_objetos = pygame.Rect(435, 105, 150, 40)
rects_bibliografia_salas = [pygame.Rect(20, 100 + i * 68, 225, 58) for i in range(len(SALAS_BIBLIOGRAFIA_VISIBLES))]
rects_bibliografia_objetos = [pygame.Rect(270, 166 + i * 34, 230, 30) for i in range(10)]
mensaje_guardado = ""
mensaje_partidas = ""
partidas_guardadas = []
tiempo_espacio_tutorial = 0.0
PROGRESO_SALTO_TUTORIAL = 5.0

btn_flecha_izq = pygame.Rect(50, 260, 45, 60)
btn_flecha_der = pygame.Rect(805, 260, 45, 60)
btn_seleccionar_comodin = pygame.Rect(350, 480, 200, 45)
btn_confirmar_mision = pygame.Rect(600, 480, 200, 45)

def obtener_lineas_texto(texto, fuente, ancho_maximo):
    texto = traducir_texto(texto)
    lineas = []
    parrafos = texto.split("\n")
    for parrafo in parrafos:
        if not parrafo.strip():
            lineas.append("")
            continue
        palabras = parrafo.split(" ")
        linea_actual = ""
        for palabra in palabras:
            test_linea = linea_actual + (" " if linea_actual else "") + palabra
            if fuente.size(test_linea)[0] <= ancho_maximo:
                linea_actual = test_linea
            else:
                if linea_actual:
                    lineas.append(linea_actual)
                linea_actual = palabra
        if linea_actual:
            lineas.append(linea_actual)
    return lineas


def desbloquear_sala(modulo_id):
    if modulo_id == MODULO_AIRLOCK_LEGACY:
        modulo_id = 3
    if modulo_id not in conceptos_desbloqueados["salas"]:
        conceptos_desbloqueados["salas"].append(modulo_id)

def siguiente_sala_visible(modulo_id, direccion):
    if modulo_id == MODULO_AIRLOCK_LEGACY:
        modulo_id = 3
    orden = [3, 5, 2, 1, 0]
    indice = orden.index(modulo_id) if modulo_id in orden else 0
    return orden[(indice + direccion) % len(orden)]


def desbloquear_objeto(objeto_id):
    if objeto_id and objeto_id not in conceptos_desbloqueados["objetos"]:
        conceptos_desbloqueados["objetos"].append(objeto_id)


def dibujar_microimagen(rect, clase, semilla):
    pygame.draw.rect(pantalla, (7, 16, 28), rect, border_radius=4)
    pygame.draw.rect(pantalla, (70, 110, 130), rect, width=2, border_radius=4)
    interior = rect.inflate(-12, -12)
    pygame.draw.rect(pantalla, (12, 25, 37), interior)
    clip_previo = pantalla.get_clip()
    pantalla.set_clip(interior)
    rng = random.Random(semilla)

    if clase == "GRANO FINO":
        for _ in range(48):
            x = rng.randint(interior.left + 4, interior.right - 4)
            y = rng.randint(interior.top + 4, interior.bottom - 4)
            radio = rng.choice((1, 2, 3))
            color = rng.choice(((191, 164, 119), (218, 191, 143), (130, 119, 105)))
            pygame.draw.circle(pantalla, color, (x, y), radio)
    elif clase == "CRISTAL":
        for _ in range(9):
            x = rng.randint(interior.left + 15, interior.right - 15)
            y = rng.randint(interior.top + 12, interior.bottom - 12)
            ancho = rng.randint(7, 15)
            alto = rng.randint(8, 20)
            forma = [(x, y - alto), (x + ancho, y - 2), (x + ancho // 2, y + alto), (x - ancho, y + 3)]
            pygame.draw.polygon(pantalla, rng.choice(((165, 206, 205), (205, 221, 190), (133, 180, 194))), forma)
            pygame.draw.line(pantalla, (225, 239, 220), forma[0], forma[2], 1)
    else:
        for _ in range(7):
            x = rng.randint(interior.left + 15, interior.right - 15)
            y = rng.randint(interior.top + 12, interior.bottom - 12)
            radio = rng.randint(7, 17)
            puntos = []
            for angulo in range(0, 360, 60):
                distancia = radio * rng.uniform(0.65, 1.15)
                rad = math.radians(angulo)
                puntos.append((int(x + math.cos(rad) * distancia), int(y + math.sin(rad) * distancia)))
            pygame.draw.polygon(pantalla, rng.choice(((117, 91, 73), (148, 112, 83), (94, 88, 79))), puntos)
            pygame.draw.polygon(pantalla, (194, 151, 108), puntos, width=1)

    # Marcas de escala y retícula de medición del microscopio.
    pygame.draw.line(pantalla, (90, 180, 190), (interior.left + 8, interior.bottom - 8), (interior.left + 42, interior.bottom - 8), 2)
    pygame.draw.line(pantalla, (90, 180, 190), (interior.left + 8, interior.bottom - 11), (interior.left + 8, interior.bottom - 5), 1)
    pantalla.set_clip(clip_previo)


ARCHIVO_PARTIDAS = os.path.join(directorio_script, "partidas_guardadas.json")
VARIABLES_GUARDABLES = [
    "nombre_jugador", "edad_jugador", "comodines_elegidos", "creditos", "oxigeno", "oxigeno_congelado",
    "comida", "comida_congelado", "radiacion", "radiacion_congelado", "dia_actual", "duracion_dia_actual",
    "tiempo_dia", "dias_ignorados_acumulados", "misiones_del_dia", "modulo_actual", "tutorial_activo",
    "modulo_minijuego_activo", "id_minijuego",
    "paso_tutorial", "texto_tutorial_indice", "tutorial_fase", "panel_misiones_abierto", "temp_actual",
    "tiempo_en_target", "luces_estado", "manchas_polvo", "paquetes", "cajas_destino", "paquete_arrastrando",
    "eq_niveles", "progreso_valvula", "n2_nivel", "o2_nivel", "fuga_rect", "parche_rect", "parche_arrastrando",
    "fuga_reparada", "feedback_fuga", "temporizador_feedback_fuga",
    "botones_drenaje", "secuencia_drenaje_usuario", "estado_co2", "cables_izq", "cables_der",
    "conexion_cable_seleccionado", "conexiones_hechas", "enfoque_microscopio", "tiempo_en_enfoque", "rocas",
    "ingesta_muestras", "camara_ingesta_rect", "progreso_ingesta", "ingesta_procesando", "temporizador_ingesta",
    "feedback_ingesta", "temporizador_feedback_ingesta", "analisis_muestras", "indice_analisis", "errores_analisis",
    "feedback_analisis", "temporizador_feedback_analisis", "botones_clasificacion",
    "cajas_rocas", "roca_arrastrando", "secuencia_bio_objetivo", "secuencia_bio_usuario", "botones_bio", "ph_actual",
    "garra_pos", "carga_rover", "psi_neumatico", "manchas_uv", "cajas_rover", "caja_rover_arrastrando",
    "secuencia_eva_usuario", "fisura_traje", "parche_eva_rect", "parche_eva_arrastrando", "cierres_casco",
    "carga_jetpack", "mosqueton_rect", "mosqueton_arrastrando", "nivel_escudo_rad", "frecuencia_antena",
    "freno_viento", "polvo_sensores", "secuencia_press_usuario", "finales_desbloqueados", "conceptos_desbloqueados",
    "evento_dia_mensaje", "misiones_omitidas_evento", "multiplicador_oxigeno_dia", "multiplicador_comida_dia",
    "multiplicador_radiacion_dia"
]


def convertir_para_json(valor):
    if isinstance(valor, pygame.Rect):
        return {"__pygame_rect__": [valor.x, valor.y, valor.width, valor.height]}
    if isinstance(valor, dict):
        return {str(k): convertir_para_json(v) for k, v in valor.items()}
    if isinstance(valor, (list, tuple)):
        return [convertir_para_json(v) for v in valor]
    return valor


def convertir_desde_json(valor):
    if isinstance(valor, dict):
        if "__pygame_rect__" in valor:
            return pygame.Rect(valor["__pygame_rect__"])
        return {k: convertir_desde_json(v) for k, v in valor.items()}
    if isinstance(valor, list):
        return [convertir_desde_json(v) for v in valor]
    return valor


def leer_partidas_guardadas():
    try:
        with open(ARCHIVO_PARTIDAS, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
        return contenido if isinstance(contenido, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def guardar_partida():
    global partidas_guardadas, mensaje_guardado
    try:
        estado_reanudable = estado_anterior_pausa
        datos = {clave: convertir_para_json(globals()[clave]) for clave in VARIABLES_GUARDABLES}
        datos["estado_juego"] = estado_reanudable
        datos["mision_en_curso_idx"] = next((i for i, m in enumerate(misiones_del_dia) if m is mision_en_curso), None)
        datos["mision_seleccionada_idx"] = next((i for i, m in enumerate(misiones_del_dia) if m is mision_tutorial_seleccionada), None)
        ahora = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
        partida = {
            "id": datetime.now().strftime("%Y%m%d-%H%M%S-%f"),
            "titulo": f"{nombre_jugador or 'Astronauta'} · Día {dia_actual}/14 · {ahora}",
            "fecha": ahora,
            "datos": datos
        }
        partidas_guardadas = leer_partidas_guardadas()
        partidas_guardadas.insert(0, partida)
        with open(ARCHIVO_PARTIDAS, "w", encoding="utf-8") as archivo:
            json.dump(partidas_guardadas, archivo, ensure_ascii=False, indent=2)
        mensaje_guardado = "Partida guardada correctamente."
    except (OSError, TypeError, ValueError) as error:
        mensaje_guardado = f"No se pudo guardar: {error}"


def cargar_partida(partida):
    global estado_juego, estado_anterior_pausa, mision_en_curso, mision_tutorial_seleccionada
    global minijuego_activo, paquete_arrastrando, roca_arrastrando, caja_rover_arrastrando
    global parche_arrastrando, parche_eva_arrastrando, mosqueton_arrastrando, ingesta_arrastrando
    global tiempo_espacio_tutorial
    datos = partida.get("datos", {})
    for clave in VARIABLES_GUARDABLES:
        if clave in datos:
            valor_cargado = convertir_desde_json(datos[clave])
            if clave == "finales_desbloqueados" and isinstance(valor_cargado, dict):
                for nombre_final, desbloqueado in valor_cargado.items():
                    if desbloqueado:
                        desbloquear_final(nombre_final)
            else:
                globals()[clave] = valor_cargado
    # Las partidas creadas antes de la Enciclopedia no incluyen sus desbloqueos.
    if "conceptos_desbloqueados" not in datos:
        globals()["conceptos_desbloqueados"] = {"salas": [], "objetos": []}
    estado_reanudable = datos.get("estado_juego", "JUGANDO")
    estado_anterior_pausa = estado_reanudable
    estado_juego = estado_reanudable
    idx_mision = datos.get("mision_en_curso_idx")
    idx_seleccionada = datos.get("mision_seleccionada_idx")
    mision_en_curso = misiones_del_dia[idx_mision] if isinstance(idx_mision, int) and 0 <= idx_mision < len(misiones_del_dia) else None
    mision_tutorial_seleccionada = misiones_del_dia[idx_seleccionada] if isinstance(idx_seleccionada, int) and 0 <= idx_seleccionada < len(misiones_del_dia) else None
    minijuego_activo = estado_juego == "MINIJUEGO"
    paquete_arrastrando = None
    roca_arrastrando = None
    caja_rover_arrastrando = None
    parche_arrastrando = False
    parche_eva_arrastrando = False
    mosqueton_arrastrando = False
    ingesta_arrastrando = None
    tiempo_espacio_tutorial = 0.0

def preparar_evento_nuevo_dia():
    global evento_dia_mensaje, misiones_omitidas_evento
    global multiplicador_oxigeno_dia, multiplicador_comida_dia, multiplicador_radiacion_dia
    global oxigeno_congelado, comida_congelado, radiacion_congelado

    oxigeno_congelado = comida_congelado = radiacion_congelado = False
    multiplicador_oxigeno_dia = 1.0
    multiplicador_comida_dia = 1.0
    multiplicador_radiacion_dia = 1.0
    misiones_omitidas_evento = []

    eventos = [
        ("oxigeno_ok", "Un buen comienzo: Jane cambió un filtro anoche. Hoy el oxígeno se mantiene estable y no hay misiones de oxígeno.", 0.0),
        ("oxigeno_alto", "Aviso de soporte vital: un filtro está muy sucio. El oxígeno se consumirá más rápido; revisa las misiones de la base.", 1.7),
        ("comida_ok", "Buenas noticias: revisaron las raciones y están en buen estado. La comida se mantiene estable y no hay misión de raciones hoy.", 0.0),
        ("comida_alta", "Parte de las raciones se echó a perder. La comida bajará más rápido hoy; prioriza la misión de suministros.", 1.7),
        ("radiacion_ok", "El pronóstico solar está tranquilo y el blindaje quedó revisado. La radiación se mantiene estable; no hay alerta solar hoy.", 0.0),
        ("radiacion_alta", "El pronóstico marciano marca un pico de radiación. La exposición aumentará más rápido; limita las salidas y atiende el escudo.", 1.8)
    ]
    if dia_actual == 1 or random.random() >= 0.48:
        evento_dia_mensaje = "Sin novedades críticas en el parte matutino. Los recursos bajan a su ritmo habitual."
        return

    evento, mensaje, multiplicador = random.choice(eventos)
    evento_dia_mensaje = mensaje
    if evento.startswith("oxigeno"):
        if evento.endswith("_ok"):
            oxigeno_congelado = True
            misiones_omitidas_evento.extend(("Recarga Tanque O2", "Equilibrio N2/O2", "Fuga en Tubería", "Reemplazo Cartuchos CO2"))
        else:
            multiplicador_oxigeno_dia = multiplicador
    elif evento.startswith("comida"):
        if evento.endswith("_ok"):
            comida_congelado = True
            misiones_omitidas_evento.extend(("Ración Nutricional Vital", "Inventario de Raciones"))
        else:
            multiplicador_comida_dia = multiplicador
    else:
        if evento.endswith("_ok"):
            radiacion_congelado = True
            misiones_omitidas_evento.extend(("Ajuste Escudo Radiación", "Limpieza Sensores Solares"))
        else:
            multiplicador_radiacion_dia = multiplicador


def generar_misiones_diarias():
    misiones = []
    urgencias_fijas = [
        {"nombre": "Recarga Tanque O2", "modulo_id": 1, "tipo": "URGENCIA", "desc": f"Soporte Vital: {OBJETOS_POR_MISION['Recarga Tanque O2']}.", "completada": False},
        {"nombre": "Ración Nutricional Vital", "modulo_id": 0, "tipo": "URGENCIA", "desc": f"Sala Común: {OBJETOS_POR_MISION['Ración Nutricional Vital']}.", "completada": False},
        {"nombre": "Ajuste Escudo Radiación", "modulo_id": 5, "tipo": "URGENCIA", "desc": f"Exterior: {OBJETOS_POR_MISION['Ajuste Escudo Radiación']}.", "completada": False}
    ]
    if 1 in comodines_elegidos:
        urgencias_fijas = [m for m in urgencias_fijas if m["nombre"] != "Ración Nutricional Vital"]
    urgencias_fijas = [m for m in urgencias_fijas if m["nombre"] not in misiones_omitidas_evento]
    misiones.extend(urgencias_fijas)
    secundarias_pool = [
        {"nombre": "Ciclo de Sueño y Luces", "modulo_id": 0},
    {"nombre": "Limpieza Filtros de Polvo", "modulo_id": 1},
        {"nombre": "Inventario de Raciones", "modulo_id": 0},
        {"nombre": "Equilibrio N2/O2", "modulo_id": 1},
        {"nombre": "Fuga en Tubería", "modulo_id": 1},
        {"nombre": "Reemplazo Cartuchos CO2", "modulo_id": 1},
        {"nombre": "Conexión de Cables", "modulo_id": 2},
        {"nombre": "Microscopio de Muestras", "modulo_id": 2},
        {"nombre": "Ingreso de Núcleos y Suelo", "modulo_id": 2},
        {"nombre": "Secuencia Despresurización", "modulo_id": 4},
        {"nombre": "Inspección de Trajes", "modulo_id": 4},
        {"nombre": "Sellado de Casco", "modulo_id": 4},
        {"nombre": "Sintonizar Antena", "modulo_id": 5},
        {"nombre": "Calibración Anemómetro", "modulo_id": 5},
        {"nombre": "Limpieza Sensores Solares", "modulo_id": 5}
    ]
    secundarias_pool = [m for m in secundarias_pool if m["nombre"] not in misiones_omitidas_evento]

    # El geólogo reduce las tareas normales y duplica una urgencia de recursos.
    if 0 in comodines_elegidos:
        recursos_urgentes = [m for m in urgencias_fijas if m["nombre"] in ("Recarga Tanque O2", "Ración Nutricional Vital", "Ajuste Escudo Radiación")]
        if recursos_urgentes:
            urgente_extra = random.choice(recursos_urgentes).copy()
            urgente_extra["extra_geologo"] = True
            urgente_extra["desc"] = f"Misión extra: {OBJETOS_POR_MISION.get(urgente_extra['nombre'], urgente_extra['nombre'])}."
            misiones.append(urgente_extra)
        cantidad_normales = 3
    else:
        cantidad_normales = 6

    sec_elegidas = random.sample(secundarias_pool, min(cantidad_normales, len(secundarias_pool)))
    for tarea in sec_elegidas:
        secundarias_pool.remove(tarea)
    for s in sec_elegidas:
        s["tipo"] = "SECUNDARIA"
        s["desc"] = f"{modulos[s['modulo_id']]['nombre']}: {OBJETOS_POR_MISION.get(s['nombre'], s['nombre'])}."
        s["completada"] = False
        misiones.append(s)

    # El comandante añade una misión normal aleatoria repetible tres veces.
    if 2 in comodines_elegidos and secundarias_pool:
        repetible = random.choice(secundarias_pool)
        repetible["tipo"] = "SECUNDARIA"
        repetible["desc"] = f"{OBJETOS_POR_MISION.get(repetible['nombre'], repetible['nombre'])} · Repeticiones: 0/3"
        repetible["completada"] = False
        repetible["repeticiones_requeridas"] = 3
        repetible["repeticiones_completadas"] = 0
        repetible["mision_repetible"] = True
        misiones.append(repetible)
    return misiones

def preparar_minijuego(mision):
    global minijuego_activo, mision_en_curso, modulo_minijuego_activo, id_minijuego
    global temp_actual, tiempo_en_target, luces_estado, manchas_polvo, paquetes, cajas_destino, eq_niveles
    global progreso_valvula, n2_nivel, o2_nivel, fuga_rect, parche_rect, parche_arrastrando, fuga_reparada, feedback_fuga, temporizador_feedback_fuga, botones_drenaje, secuencia_drenaje_usuario, estado_co2
    global cables_izq, cables_der, conexion_cable_seleccionado, conexiones_hechas, enfoque_microscopio, tiempo_en_enfoque
    global ingesta_muestras, ingesta_arrastrando, camara_ingesta_rect, progreso_ingesta, ingesta_procesando, temporizador_ingesta
    global feedback_ingesta, temporizador_feedback_ingesta, analisis_muestras, indice_analisis, errores_analisis
    global feedback_analisis, temporizador_feedback_analisis
    global rocas, cajas_rocas, roca_arrastrando, secuencia_bio_objetivo, secuencia_bio_usuario, botones_bio, ph_actual
    global garra_pos, carga_rover, psi_neumatico, manchas_uv, cajas_rover, caja_rover_arrastrando
    global secuencia_eva_usuario, fisura_traje, parche_eva_rect, parche_eva_arrastrando, cierres_casco, carga_jetpack, mosqueton_rect, mosqueton_arrastrando
    global nivel_escudo_rad, frecuencia_antena, freno_viento, polvo_sensores, secuencia_press_usuario

    mision_en_curso = mision
    minijuego_activo = True
    nombre = mision["nombre"]
    mod_id = mision["modulo_id"]
    modulo_minijuego_activo = mod_id

    if mod_id == 0:
        if "Ración Nutricional" in nombre or "Termostato" in nombre:
            id_minijuego = 1
            temp_actual = float(random.randint(10, 35))
            tiempo_en_target = 0.0
        elif "Ciclo" in nombre or "Luces" in nombre:
            id_minijuego = 2
            luces_estado = [False, False, False, False]
        elif "Limpieza" in nombre or "Filtros" in nombre:
            id_minijuego = 3
            manchas_polvo = [pygame.Rect(random.randint(300, 550), random.randint(220, 350), 35, 35) for _ in range(8)]
        elif "Inventario" in nombre:
            id_minijuego = 4
            paquetes = [
                {"rect": pygame.Rect(300, 380, 40, 40), "col": ROJO_ALERTA, "tipo": 0},
                {"rect": pygame.Rect(360, 380, 40, 40), "col": VERDE_OK, "tipo": 1},
                {"rect": pygame.Rect(420, 380, 40, 40), "col": AMARILLO, "tipo": 2}
            ]
            cajas_destino = [
                {"rect": pygame.Rect(300, 240, 60, 60), "col": ROJO_ALERTA, "tipo": 0},
                {"rect": pygame.Rect(420, 240, 60, 60), "col": VERDE_OK, "tipo": 1},
                {"rect": pygame.Rect(540, 240, 60, 60), "col": AMARILLO, "tipo": 2}
            ]
        elif "Calibración" in nombre or "Alertas" in nombre:
            id_minijuego = 5
            eq_niveles = [random.randint(10, 30), random.randint(70, 90), random.randint(10, 30)]

    elif mod_id == 1:
        if "Recarga Tanque" in nombre or "Válvula" in nombre:
            id_minijuego = 1
            progreso_valvula = 0.0
        elif "Equilibrio N2/O2" in nombre:
            id_minijuego = 2
            n2_nivel = float(random.randint(30, 60))
            o2_nivel = float(random.randint(40, 80))
        elif "Fuga" in nombre or "Tubería" in nombre:
            id_minijuego = 3
            fuga_rect = pygame.Rect(random.randint(390, 500), random.randint(270, 315), 64, 64)
            parche_rect = pygame.Rect(ANCHO // 2 - 175, ALTO // 2 + 50, 54, 54)
            parche_arrastrando = False
            fuga_reparada = False
            feedback_fuga = ""
            temporizador_feedback_fuga = 0.0
        elif "Drenaje" in nombre:
            id_minijuego = 4
            secuencia_drenaje_usuario = []
            botones_drenaje = [
                {"rect": pygame.Rect(ANCHO // 2 - 110, ALTO // 2 - 10, 60, 60), "val": 1},
                {"rect": pygame.Rect(ANCHO // 2 - 30, ALTO // 2 - 10, 60, 60), "val": 2},
                {"rect": pygame.Rect(ANCHO // 2 + 50, ALTO // 2 - 10, 60, 60), "val": 3}
            ]
        elif "Reemplazo" in nombre or "CO2" in nombre:
            id_minijuego = 5
            estado_co2 = 0

    elif mod_id == 2:
        if "Cables" in nombre:
            id_minijuego = 1
            cables_izq = [
                {"rect": pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 60, 30, 30), "col": ROJO_ALERTA, "id": 1},
                {"rect": pygame.Rect(ANCHO // 2 - 150, ALTO // 2, 30, 30), "col": AZUL_UI, "id": 2},
                {"rect": pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 60, 30, 30), "col": VERDE_OK, "id": 3}
            ]
            cables_der = [
                {"rect": pygame.Rect(ANCHO // 2 + 120, ALTO // 2 - 60, 30, 30), "col": VERDE_OK, "id": 3},
                {"rect": pygame.Rect(ANCHO // 2 + 120, ALTO // 2, 30, 30), "col": ROJO_ALERTA, "id": 1},
                {"rect": pygame.Rect(ANCHO // 2 + 120, ALTO // 2 + 60, 30, 30), "col": AZUL_UI, "id": 2}
            ]
            conexion_cable_seleccionado = None
            conexiones_hechas = []
        elif "Microscopio" in nombre:
            id_minijuego = 2
            clases_muestra = ["GRANO FINO", "CRISTAL", "FRAGMENTO"]
            analisis_muestras = [
                {"clase": random.choice(clases_muestra), "semilla": random.randint(0, 999999)}
                for _ in range(4)
            ]
            indice_analisis = 0
            errores_analisis = 0
            feedback_analisis = ""
            temporizador_feedback_analisis = 0.0
        elif "Núcleos" in nombre or "Suelo" in nombre or "Rocas" in nombre or "Basalto" in nombre:
            id_minijuego = 6
            camara_ingesta_rect = pygame.Rect(ANCHO // 2 + 65, ALTO // 2 - 50, 135, 125)
            tipos_core = [("BASALTO", GRIS_MEDIO), ("SULFATO", AMARILLO), ("REGOLITO", NARANJA_MARTE)]
            ingesta_muestras = []
            for i, (tipo_core, color_core) in enumerate(tipos_core):
                rect_core = pygame.Rect(ANCHO // 2 - 190 + i * 75, ALTO // 2 + 75, 42, 34)
                ingesta_muestras.append({
                    "rect": rect_core, "origen": rect_core.topleft, "tipo": tipo_core,
                    "col": color_core, "semilla": random.randint(0, 999999), "procesando": False
                })
            ingesta_arrastrando = None
            progreso_ingesta = 0
            ingesta_procesando = False
            temporizador_ingesta = 0.0
            feedback_ingesta = ""
            temporizador_feedback_ingesta = 0.0
        elif "Bioquímica" in nombre or "Secuencia" in nombre:
            id_minijuego = 4
            secuencia_bio_objetivo = [random.randint(1, 4) for _ in range(4)]
            secuencia_bio_usuario = []
            botones_bio = [
                {"rect": pygame.Rect(ANCHO // 2 - 140, ALTO // 2, 50, 50), "val": 1, "col": ROJO_ALERTA},
                {"rect": pygame.Rect(ANCHO // 2 - 70, ALTO // 2, 50, 50), "val": 2, "col": AZUL_UI},
                {"rect": pygame.Rect(ANCHO // 2, ALTO // 2, 50, 50), "val": 3, "col": VERDE_OK},
                {"rect": pygame.Rect(ANCHO // 2 + 70, ALTO // 2, 50, 50), "val": 4, "col": AMARILLO}
            ]
        elif "PH" in nombre or "Hydro" in nombre:
            id_minijuego = 5
            ph_actual = float(random.choice([3.5, 4.0, 8.5, 9.0]))

    elif mod_id == 3:
        if "Garra" in nombre or "Alineación" in nombre:
            id_minijuego = 1
            garra_pos = [ANCHO // 2 - 140, ALTO // 2 - 30]
        elif "Baterías" in nombre or "Carga" in nombre:
            id_minijuego = 2
            carga_rover = 0.0
        elif "Neumáticos" in nombre and "Presión" in nombre:
            id_minijuego = 3
            psi_neumatico = 12.0
        elif "Desinfección" in nombre:
            id_minijuego = 4
            manchas_uv = [pygame.Rect(random.randint(320, 520), random.randint(230, 330), 30, 30) for _ in range(6)]
        elif "Transferencia" in nombre or "Carga" in nombre:
            id_minijuego = 5
            cajas_rover = [
                {"rect": pygame.Rect(ANCHO // 2 - 150, ALTO // 2 - 40, 45, 45)},
                {"rect": pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 15, 45, 45)}
            ]
            caja_rover_arrastrando = None

    elif mod_id == 4:
        if "Secuencia" in nombre or "Despresurización" in nombre:
            id_minijuego = 1
            secuencia_eva_usuario = []
        elif "Inspección" in nombre or "Trajes" in nombre:
            id_minijuego = 2
            fisura_traje = pygame.Rect(random.randint(360, 520), random.randint(220, 320), 40, 40)
            parche_eva_rect = pygame.Rect(ANCHO // 2 - 160, ALTO // 2 + 50, 50, 50)
            parche_eva_arrastrando = False
        elif "Casco" in nombre or "Sellado" in nombre:
            id_minijuego = 3
            cierres_casco = [False, False, False]
        elif "Jetpack" in nombre or "Recarga" in nombre:
            id_minijuego = 4
            carga_jetpack = 0.0
        elif "Anclaje" in nombre or "Seguridad" in nombre:
            id_minijuego = 5
            mosqueton_rect = pygame.Rect(ANCHO // 2 - 150, ALTO // 2 + 30, 50, 50)
            mosqueton_arrastrando = False

    elif mod_id == 5:
        if "Escudo Radiación" in nombre or "Ajuste" in nombre:
            id_minijuego = 1
            nivel_escudo_rad = 20.0
        elif "Antena" in nombre or "Sintonizar" in nombre:
            id_minijuego = 2
            frecuencia_antena = 88.0
        elif "Anemómetro" in nombre or "Calibración" in nombre:
            id_minijuego = 3
            freno_viento = 0.0
        elif "Sensores Solares" in nombre or "Limpieza" in nombre:
            id_minijuego = 4
            polvo_sensores = [pygame.Rect(random.randint(320, 520), random.randint(230, 330), 30, 30) for _ in range(6)]
        elif "Presión" in nombre or "Barómetro" in nombre:
            id_minijuego = 5
            secuencia_press_usuario = []

# 5. BUCLE PRINCIPAL
ejecutando = True
mencion_interaccion = ""

while ejecutando:
    dt = reloj.tick(FPS) / 1000.0

    # A. MANEJO DE EVENTOS
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            if estado_juego in ("JUGANDO", "MINIJUEGO"):
                estado_anterior_pausa = estado_juego
                estado_juego = "PAUSA"
            elif estado_juego == "PAUSA":
                estado_juego = estado_anterior_pausa

        if estado_juego == "PAUSA":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_reanudar.collidepoint(evento.pos):
                    estado_juego = estado_anterior_pausa
                elif btn_menu_pausa.collidepoint(evento.pos):
                    estado_juego = "MENU_PRINCIPAL"
                elif btn_guardar_pausa.collidepoint(evento.pos):
                    guardar_partida()
            continue

        if estado_juego == "MENU_PRINCIPAL":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos
                if btn_iniciar.collidepoint(mx, my):
                    creditos = 5
                    oxigeno = 100.0
                    comida = 100.0
                    radiacion = 100.0
                    oxigeno_congelado = False
                    comida_congelado = False
                    radiacion_congelado = False
                    dia_actual = 1
                    dias_ignorados_acumulados = 0
                    comodines_elegidos = []
                    modulo_actual = 0
                    conceptos_desbloqueados = {"salas": [], "objetos": []}
                    indice_catalogo = 0
                    texto_intro_indice = 0.0
                    paso_tutorial = 0
                    texto_tutorial_indice = 0.0
                    tutorial_activo = True
                    tutorial_fase = "dialogos"
                    mision_tutorial_seleccionada = None
                    nombre_jugador = ""
                    edad_jugador = ""
                    campo_formulario_activo = "nombre"
                    mensaje_formulario = ""
                    pygame.key.start_text_input()
                    estado_juego = "CAPTURA_JUGADOR"
                elif btn_continuar.collidepoint(mx, my):
                    partidas_guardadas = leer_partidas_guardadas()
                    pagina_partidas = 0
                    mensaje_partidas = "No hay partidas guardadas todavía." if not partidas_guardadas else "Elige una partida para continuar."
                    estado_juego = "CONTINUAR"
                elif btn_finales.collidepoint(mx, my):
                    estado_juego = "FINALES"
                elif btn_bibliografia.collidepoint(mx, my):
                    bibliografia_seccion = "GENERAL"
                    bibliografia_modulo = 0
                    bibliografia_objeto = None
                    estado_juego = "BIBLIOGRAFIA"

        elif estado_juego == "CAPTURA_JUGADOR":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if campo_nombre_rect.collidepoint(evento.pos):
                    campo_formulario_activo = "nombre"
                elif campo_edad_rect.collidepoint(evento.pos):
                    campo_formulario_activo = "edad"
                elif btn_confirmar_datos.collidepoint(evento.pos):
                    if not nombre_jugador.strip():
                        mensaje_formulario = "Escribe tu nombre para presentarte."
                    elif not edad_jugador.isdigit() or not 1 <= int(edad_jugador) <= 105:
                        mensaje_formulario = "La edad debe ser un número entero entre 1 y 105."
                    else:
                        texto_historia_completo = (
                            f"I'm {nombre_jugador.strip()} and I'm {int(edad_jugador)} years old.\n\n"
                            "I stood out among all the competitors and earned the chance to travel to Mars as a junior astronaut. Since this is a team mission, I can choose up to two junior crewmates to come with me; each one brings skills that can help the crew. "
                            "The crewmates I choose will guide me during my 14 days at the base. Each day, we'll complete urgent and regular missions, take care of the base resources, and work together. "
                            "This is my chance to prove I'm ready for the responsibility and worthy of future missions."
                        )
                        texto_intro_indice = 0.0
                        pygame.key.stop_text_input()
                        estado_juego = "INTRO"
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_TAB:
                    campo_formulario_activo = "edad" if campo_formulario_activo == "nombre" else "nombre"
                elif evento.key == pygame.K_BACKSPACE:
                    if campo_formulario_activo == "nombre":
                        nombre_jugador = nombre_jugador[:-1]
                    else:
                        edad_jugador = edad_jugador[:-1]
                elif evento.key == pygame.K_RETURN:
                    if not nombre_jugador.strip():
                        mensaje_formulario = "Escribe tu nombre para presentarte."
                    elif not edad_jugador.isdigit() or not 1 <= int(edad_jugador) <= 105:
                        mensaje_formulario = "La edad debe ser un número entero entre 1 y 105."
                    else:
                        texto_historia_completo = (
                            f"I'm {nombre_jugador.strip()} and I'm {int(edad_jugador)} years old.\n\n"
                            "I stood out among all the competitors and earned the chance to travel to Mars as a junior astronaut. Since this is a team mission, I can choose up to two junior crewmates to come with me; each one brings skills that can help the crew. "
                            "The crewmates I choose will guide me during my 14 days at the base. Each day, we'll complete urgent and regular missions, take care of the base resources, and work together. "
                            "This is my chance to prove I'm ready for the responsibility and worthy of future missions."
                        )
                        texto_intro_indice = 0.0
                        pygame.key.stop_text_input()
                        estado_juego = "INTRO"
            elif evento.type == pygame.TEXTINPUT:
                if campo_formulario_activo == "nombre":
                    nombre_jugador = (nombre_jugador + evento.text)[:20]
                elif evento.text.isdigit():
                    edad_jugador = (edad_jugador + evento.text)[:3]

        elif estado_juego == "INTRO":
            if evento.type == pygame.MOUSEBUTTONDOWN or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE):
                if int(texto_intro_indice) < len(texto_historia_completo):
                    texto_intro_indice = float(len(texto_historia_completo))
                else:
                    estado_juego = "SELECCION"

        elif estado_juego == "CONTINUAR":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver.collidepoint(evento.pos):
                    estado_juego = "MENU_PRINCIPAL"
                elif btn_pagina_anterior.collidepoint(evento.pos):
                    pagina_partidas = max(0, pagina_partidas - 1)
                elif btn_pagina_siguiente.collidepoint(evento.pos):
                    max_pagina = max(0, (len(partidas_guardadas) - 1) // len(rects_partidas))
                    pagina_partidas = min(max_pagina, pagina_partidas + 1)
                else:
                    for idx, rect_partida in enumerate(rects_partidas):
                        indice_partida = pagina_partidas * len(rects_partidas) + idx
                        if indice_partida < len(partidas_guardadas) and rect_partida.collidepoint(evento.pos):
                            cargar_partida(partidas_guardadas[indice_partida])
                            break

        elif estado_juego == "FINALES":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos
                if btn_volver.collidepoint(mx, my):
                    estado_juego = "MENU_PRINCIPAL"

        elif estado_juego in ("FINAL_MUERTE", "FINAL_REGRESO"):
            if evento.type == pygame.MOUSEBUTTONDOWN and btn_volver.collidepoint(evento.pos):
                estado_juego = "MENU_PRINCIPAL"

        elif estado_juego == "DIA_TERMINADO":
            if evento.type == pygame.MOUSEBUTTONDOWN and btn_dia_terminado.collidepoint(evento.pos):
                if dia_actual >= 14:
                    desbloquear_final("FELIZ")
                    estado_juego = "FINALES"
                else:
                    dia_actual += 1
                    tiempo_dia = duracion_dia_actual
                    preparar_evento_nuevo_dia()
                    misiones_del_dia = generar_misiones_diarias()
                    estado_juego = "NUEVO_DIA"

        elif estado_juego == "NUEVO_DIA":
            if evento.type == pygame.MOUSEBUTTONDOWN and btn_nuevo_dia.collidepoint(evento.pos):
                estado_juego = "JUGANDO"
                mencion_interaccion = evento_dia_mensaje

        elif estado_juego == "BIBLIOGRAFIA":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                estado_juego = "MENU_PRINCIPAL"
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver_bibliografia.collidepoint(evento.pos):
                    estado_juego = "MENU_PRINCIPAL"
                elif tab_bibliografia_general.collidepoint(evento.pos):
                    bibliografia_seccion = "GENERAL"
                    bibliografia_objeto = None
                elif tab_bibliografia_objetos.collidepoint(evento.pos):
                    bibliografia_seccion = "OBJETOS"
                    bibliografia_objeto = None
                else:
                    for idx_sala, rect_sala in enumerate(rects_bibliografia_salas):
                        if rect_sala.collidepoint(evento.pos):
                            bibliografia_modulo = SALAS_BIBLIOGRAFIA_VISIBLES[idx_sala]
                            bibliografia_objeto = None
                            break
                    else:
                        if bibliografia_seccion == "OBJETOS":
                            datos_sala = bibliografia_salas.get(bibliografia_modulo, {})
                            lista_objetos_sala = datos_sala.get("objetos", [])
                            for idx_objeto, rect_objeto in enumerate(rects_bibliografia_objetos):
                                if idx_objeto < len(lista_objetos_sala) and rect_objeto.collidepoint(evento.pos):
                                    bibliografia_objeto = lista_objetos_sala[idx_objeto]["id"]
                                    break

        elif estado_juego == "SELECCION":
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    indice_catalogo = (indice_catalogo - 1) % len(datos_catalogo)
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    indice_catalogo = (indice_catalogo + 1) % len(datos_catalogo)
                elif evento.key == pygame.K_SPACE:
                    if indice_catalogo in comodines_elegidos:
                        comodines_elegidos.remove(indice_catalogo)
                    elif len(comodines_elegidos) < 2:
                        comodines_elegidos.append(indice_catalogo)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos
                if btn_flecha_izq.collidepoint(mx, my):
                    indice_catalogo = (indice_catalogo - 1) % len(datos_catalogo)
                elif btn_flecha_der.collidepoint(mx, my):
                    indice_catalogo = (indice_catalogo + 1) % len(datos_catalogo)
                elif btn_seleccionar_comodin.collidepoint(mx, my):
                    if indice_catalogo in comodines_elegidos:
                        comodines_elegidos.remove(indice_catalogo)
                    elif len(comodines_elegidos) < 2:
                        comodines_elegidos.append(indice_catalogo)
                elif btn_confirmar_mision.collidepoint(mx, my) and len(comodines_elegidos) > 0:
                    duracion_dia_actual = 4 * 60.0
                    if 1 in comodines_elegidos:
                        duracion_dia_actual -= 60.0
                    if 2 in comodines_elegidos:
                        duracion_dia_actual += 120.0

                    tiempo_dia = duracion_dia_actual
                    preparar_evento_nuevo_dia()
                    misiones_del_dia = generar_misiones_diarias()
                    estado_juego = "JUGANDO"
                    desbloquear_sala(modulo_actual)

        elif estado_juego == "JUGANDO" and creditos > 0:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if ayuda_jj_abierta:
                    if btn_jj.collidepoint(evento.pos) or btn_cerrar_ayuda_jj.collidepoint(evento.pos):
                        ayuda_jj_abierta = False
                    continue
                if btn_jj.collidepoint(evento.pos):
                    ayuda_jj_abierta = True
                    continue
            elif ayuda_jj_abierta and evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ayuda_jj_abierta = False
                continue
            if ayuda_jj_abierta:
                continue

            # El tutorial permite únicamente la acción indicada en cada fase.
            if dia_actual == 1 and tutorial_activo and estado_juego == "JUGANDO":
                es_espacio = evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE
                if evento.type == pygame.MOUSEBUTTONDOWN or es_espacio:
                    mx, my = evento.pos if evento.type == pygame.MOUSEBUTTONDOWN else (-1, -1)
                    if tutorial_fase == "dialogos" and (es_espacio or btn_siguiente_tutorial.collidepoint(mx, my)):
                        msg_actual = dialogos_tutorial_actuales()[paso_tutorial]
                        if int(texto_tutorial_indice) < len(msg_actual):
                            texto_tutorial_indice = float(len(msg_actual))
                        else:
                            paso_tutorial += 1
                            texto_tutorial_indice = 0.0
                            if paso_tutorial >= DIALOGOS_TUTORIAL_TOTAL:
                                tutorial_fase = "elegir_urgente"
                    elif tutorial_fase in ("elegir_urgente", "elegir_secundaria") and btn_lengueta.collidepoint(mx, my):
                        panel_misiones_abierto = True
                    elif tutorial_fase == "elegir_urgente" and panel_misiones_abierto:
                        y_box = 95
                        for m in misiones_del_dia:
                            btn_mision = pygame.Rect(ANCHO - 330, y_box, 310, 40)
                            if btn_mision.collidepoint(mx, my) and m["tipo"] == "URGENCIA" and not m["completada"]:
                                modulo_actual = m["modulo_id"]
                                desbloquear_sala(modulo_actual)
                                mision_tutorial_seleccionada = m
                                panel_misiones_abierto = False
                                tutorial_fase = "explicar_urgente"
                                texto_tutorial_indice = 0.0
                                break
                            y_box += 44
                    elif tutorial_fase in ("explicar_urgente", "explicar_secundaria", "final") and (es_espacio or btn_siguiente_tutorial.collidepoint(mx, my)):
                        mensaje_actual = mensajes_tutorial_actuales()[tutorial_fase]
                        if int(texto_tutorial_indice) < len(mensaje_actual):
                            texto_tutorial_indice = float(len(mensaje_actual))
                        elif tutorial_fase == "explicar_urgente":
                            tutorial_fase = "hacer_urgente"
                        elif tutorial_fase == "explicar_secundaria":
                            tutorial_fase = "hacer_secundaria"
                        else:
                            tutorial_activo = False
                    elif tutorial_fase == "elegir_secundaria" and panel_misiones_abierto:
                        y_box = 95
                        for m in misiones_del_dia:
                            btn_mision = pygame.Rect(ANCHO - 330, y_box, 310, 40)
                            if btn_mision.collidepoint(mx, my) and m["tipo"] == "SECUNDARIA" and not m["completada"]:
                                modulo_actual = m["modulo_id"]
                                desbloquear_sala(modulo_actual)
                                mision_tutorial_seleccionada = m
                                panel_misiones_abierto = False
                                tutorial_fase = "explicar_secundaria"
                                texto_tutorial_indice = 0.0
                                break
                            y_box += 44

            if evento.type == pygame.MOUSEBUTTONDOWN and not (dia_actual == 1 and tutorial_activo and tutorial_fase not in ("hacer_urgente", "hacer_secundaria")):
                mx, my = evento.pos
                if btn_lengueta.collidepoint(mx, my):
                    panel_misiones_abierto = not panel_misiones_abierto
                elif panel_misiones_abierto:
                    y_box = 95
                    for m in misiones_del_dia:
                        btn_mision = pygame.Rect(ANCHO - 330, y_box, 310, 40)
                        if btn_mision.collidepoint(mx, my):
                            modulo_actual = m["modulo_id"]
                            desbloquear_sala(modulo_actual)
                            mision_tutorial_seleccionada = m
                            mencion_interaccion = f"Navegando a {modulos[modulo_actual]['nombre']} para: {m['nombre']}"
                            panel_misiones_abierto = False
                            break
                        y_box += 44
                else:
                    modulo_visual = 3 if modulo_actual == MODULO_AIRLOCK_LEGACY else modulo_actual
                    mod_info = modulos[modulo_visual]
                    misiones_pendientes_aqui = [m for m in misiones_del_dia if m["modulo_id"] == modulo_actual and not m["completada"]]
                    click_valido = False
                    hotspot_pulsado = None

                    for hs in mod_info.get("hotspots", []):
                        dentro_zona = hs["rect"].collidepoint(mx, my)
                        if dentro_zona and hs.get("mask") is not None:
                            dentro_zona = bool(hs["mask"].get_at((mx, my)))
                        if dentro_zona:
                            click_valido = True
                            hotspot_pulsado = hs
                            break

                    cid = mod_info["comodin_id"]
                    pos_comp = mod_info["pos_comodin"]
                    if cid is not None and cid in comodines_elegidos and pos_comp is not None:
                        px, py = pos_comp
                        if pygame.Rect(px, py, 120, 180).collidepoint(mx, my):
                            click_valido = True

                    if click_valido:
                        if hotspot_pulsado and hotspot_pulsado.get("destino_modulo") is not None:
                            modulo_actual = hotspot_pulsado["destino_modulo"]
                            desbloquear_sala(modulo_actual)
                            mencion_interaccion = f"Entrando a {modulos[modulo_actual]['nombre']}"
                            continue
                        if hotspot_pulsado:
                            for objeto_id in hotspot_pulsado.get("objetos", []):
                                desbloquear_objeto(objeto_id)
                        mision_destacada_en_sala = (
                            mision_tutorial_seleccionada in misiones_del_dia
                            and mision_tutorial_seleccionada["modulo_id"] == modulo_actual
                            and not mision_tutorial_seleccionada["completada"]
                        )
                        objetivo_incorrecto = False
                        if mision_destacada_en_sala:
                            if hotspot_pulsado and hotspot_pulsado.get("mision") == mision_tutorial_seleccionada["nombre"]:
                                mision_objetivo = mision_tutorial_seleccionada
                            else:
                                mision_objetivo = None
                                objetivo_incorrecto = True
                        elif hotspot_pulsado and hotspot_pulsado.get("mision"):
                            mision_objetivo = next((m for m in misiones_del_dia if m["nombre"] == hotspot_pulsado["mision"] and not m["completada"]), None)
                        else:
                            mision_objetivo = misiones_pendientes_aqui[0] if misiones_pendientes_aqui else None

                        if mision_objetivo:
                            mision_tutorial_seleccionada = mision_objetivo
                            preparar_minijuego(mision_objetivo)
                            estado_juego = "MINIJUEGO"
                        elif objetivo_incorrecto:
                            mencion_interaccion = "Ese equipo no corresponde a la misión elegida. Busca el círculo amarillo que está parpadeando."
                        elif hotspot_pulsado and hotspot_pulsado.get("mision"):
                            mencion_interaccion = "No hay una misión disponible para este objeto ahora mismo."
                        else:
                            mencion_interaccion = "Estación revisada. Sin misiones pendientes aquí."

            if evento.type == pygame.KEYDOWN and not (dia_actual == 1 and tutorial_activo):
                if evento.key in (pygame.K_LEFT, pygame.K_a):
                    modulo_actual = siguiente_sala_visible(modulo_actual, -1)
                    desbloquear_sala(modulo_actual)
                    mencion_interaccion = f"Ingresando a: {modulos[modulo_actual]['nombre']}"
                elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                    modulo_actual = siguiente_sala_visible(modulo_actual, 1)
                    desbloquear_sala(modulo_actual)
                    mencion_interaccion = f"Ingresando a: {modulos[modulo_actual]['nombre']}"

        elif estado_juego == "MINIJUEGO":
            if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                mx, my = evento.pos
            else:
                mx, my = pygame.mouse.get_pos()
            if modulo_minijuego_activo == 0:
                if id_minijuego == 1:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_calef.collidepoint(mx, my): temp_actual += 1.5
                        elif btn_aire.collidepoint(mx, my): temp_actual -= 1.5
                elif id_minijuego == 2:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for idx, r_luz in enumerate(luces_rects):
                            if r_luz.collidepoint(mx, my): luces_estado[idx] = not luces_estado[idx]
                elif id_minijuego == 3:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for m_polvo in manchas_polvo[:]:
                            if m_polvo.collidepoint(mx, my): manchas_polvo.remove(m_polvo)
                elif id_minijuego == 4:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for p in paquetes:
                            if p["rect"].collidepoint(mx, my): paquete_arrastrando = p; break
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        if paquete_arrastrando:
                            for c in cajas_destino:
                                if c["rect"].colliderect(paquete_arrastrando["rect"]) and c["tipo"] == paquete_arrastrando["tipo"]:
                                    paquete_arrastrando["rect"].center = c["rect"].center
                            paquete_arrastrando = None
                    elif evento.type == pygame.MOUSEMOTION and paquete_arrastrando:
                        paquete_arrastrando["rect"].center = (mx, my)
                elif id_minijuego == 5:
                    if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION) and (evento.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]):
                        for idx, eq_r in enumerate(eq_rects):
                            if eq_r.collidepoint(mx, my):
                                eq_niveles[idx] = int(100 - ((my - eq_r.y) / eq_r.height) * 100)
                                eq_niveles[idx] = max(0, min(100, eq_niveles[idx]))

            elif modulo_minijuego_activo == 1:
                if id_minijuego == 1:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_presionar_valvula.collidepoint(mx, my): progreso_valvula += 20.0
                elif id_minijuego == 2:
                    if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION) and (evento.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]):
                        if eq_gas_rects[0].collidepoint(mx, my):
                            n2_nivel = max(0, min(100, int(100 - ((my - eq_gas_rects[0].y) / eq_gas_rects[0].height) * 100)))
                        elif eq_gas_rects[1].collidepoint(mx, my):
                            o2_nivel = max(0, min(100, int(100 - ((my - eq_gas_rects[1].y) / eq_gas_rects[1].height) * 100)))
                elif id_minijuego == 3:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if parche_rect.collidepoint(mx, my): parche_arrastrando = True
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        if parche_arrastrando:
                            parche_arrastrando = False
                            parche_rect.center = (max(255, min(ANCHO - 255, mx)), max(205, min(ALTO - 205, my)))
                            distancia_parche = math.hypot(parche_rect.centerx - fuga_rect.centerx, parche_rect.centery - fuga_rect.centery)
                            if distancia_parche <= fuga_rect.width * 0.68:
                                parche_rect.center = fuga_rect.center
                                fuga_reparada = True
                                feedback_fuga = "¡Fuga sellada! Buen trabajo."
                            else:
                                parche_rect.topleft = (ANCHO // 2 - 175, ALTO // 2 + 50)
                                feedback_fuga = "Centra el parche sobre el orificio rojo."
                            temporizador_feedback_fuga = 2.0
                    elif evento.type == pygame.MOUSEMOTION and parche_arrastrando:
                        parche_rect.center = (max(255, min(ANCHO - 255, mx)), max(205, min(ALTO - 205, my)))
                elif id_minijuego == 4:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for b_dren in botones_drenaje:
                            if b_dren["rect"].collidepoint(mx, my): secuencia_drenaje_usuario.append(b_dren["val"])
                elif id_minijuego == 5:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if estado_co2 == 0 and cartucho_saturado.collidepoint(mx, my): estado_co2 = 1
                        elif estado_co2 == 1 and cartucho_ranura.collidepoint(mx, my): estado_co2 = 2

            elif modulo_minijuego_activo == 2:
                if id_minijuego == 1:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for c_i in cables_izq:
                            if c_i["rect"].collidepoint(mx, my) and c_i["id"] not in [par[0] for par in conexiones_hechas]:
                                conexion_cable_seleccionado = c_i
                                break
                        if conexion_cable_seleccionado:
                            for c_d in cables_der:
                                if c_d["rect"].collidepoint(mx, my):
                                    if c_d["id"] == conexion_cable_seleccionado["id"] and c_d["id"] not in [par[1] for par in conexiones_hechas]:
                                        conexiones_hechas.append((conexion_cable_seleccionado["id"], c_d["id"]))
                                        conexion_cable_seleccionado = None
                                    break
                elif id_minijuego == 2:
                    if evento.type == pygame.MOUSEBUTTONDOWN and indice_analisis < len(analisis_muestras):
                        for boton_clase in botones_clasificacion:
                            if boton_clase["rect"].collidepoint(mx, my):
                                clase_correcta = analisis_muestras[indice_analisis]["clase"]
                                if boton_clase["clase"] == clase_correcta:
                                    indice_analisis += 1
                                    feedback_analisis = random.choice(("¡Buen análisis!", "¡Clasificación correcta!", "Morfología identificada."))
                                    temporizador_feedback_analisis = 0.9
                                else:
                                    errores_analisis += 1
                                    feedback_analisis = "No coincide. Mira el tamaño y la forma de los granos."
                                    temporizador_feedback_analisis = 1.2
                                break
                elif id_minijuego == 3:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for r in rocas:
                            if r["rect"].collidepoint(mx, my): roca_arrastrando = r; break
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        if roca_arrastrando:
                            for c_r in cajas_rocas:
                                if c_r["rect"].colliderect(roca_arrastrando["rect"]) and c_r["tipo"] == roca_arrastrando["tipo"]:
                                    roca_arrastrando["rect"].center = c_r["rect"].center
                            roca_arrastrando = None
                    elif evento.type == pygame.MOUSEMOTION and roca_arrastrando:
                        roca_arrastrando["rect"].center = (mx, my)
                elif id_minijuego == 4:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for b_bio in botones_bio:
                            if b_bio["rect"].collidepoint(mx, my): secuencia_bio_usuario.append(b_bio["val"])
                elif id_minijuego == 5:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_ph_mas.collidepoint(mx, my): ph_actual = round(ph_actual + 0.5, 1)
                        elif btn_ph_menos.collidepoint(mx, my): ph_actual = round(ph_actual - 0.5, 1)
                elif id_minijuego == 6:
                    if evento.type == pygame.MOUSEBUTTONDOWN and not ingesta_procesando:
                        for muestra in ingesta_muestras:
                            if muestra["rect"].collidepoint(mx, my):
                                ingesta_arrastrando = muestra
                                break
                    elif evento.type == pygame.MOUSEMOTION and ingesta_arrastrando and not ingesta_procesando:
                        ingesta_arrastrando["rect"].center = (mx, my)
                    elif evento.type == pygame.MOUSEBUTTONUP and ingesta_arrastrando:
                        zona_ingesta_perdonadora = camara_ingesta_rect.inflate(52, 48)
                        if zona_ingesta_perdonadora.collidepoint(ingesta_arrastrando["rect"].center):
                            ingesta_arrastrando["rect"].center = camara_ingesta_rect.center
                            ingesta_arrastrando["procesando"] = True
                            ingesta_procesando = True
                            temporizador_ingesta = 0.0
                            feedback_ingesta = f"Muestra {ingesta_arrastrando['tipo']} sellada en la cámara."
                            temporizador_feedback_ingesta = 1.0
                        else:
                            ingesta_arrastrando["rect"].topleft = ingesta_arrastrando["origen"]
                            feedback_ingesta = "Alinea la muestra con la cámara de contención."
                            temporizador_feedback_ingesta = 1.0
                        ingesta_arrastrando = None

            elif modulo_minijuego_activo == 3:
                if id_minijuego == 1:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_garra_izq.collidepoint(mx, my): garra_pos[0] -= 15
                        elif btn_garra_der.collidepoint(mx, my): garra_pos[0] += 15
                        elif btn_garra_up.collidepoint(mx, my): garra_pos[1] -= 15
                elif id_minijuego == 2:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_cargar_rover.collidepoint(mx, my): carga_rover += 25.0
                elif id_minijuego == 3:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_psi_mas.collidepoint(mx, my): psi_neumatico += 3.0
                        elif btn_psi_menos.collidepoint(mx, my): psi_neumatico -= 3.0
                elif id_minijuego == 4:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for m_uv in manchas_uv[:]:
                            if m_uv.collidepoint(mx, my): manchas_uv.remove(m_uv)
                elif id_minijuego == 5:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for c_rover in cajas_rover:
                            if c_rover["rect"].collidepoint(mx, my): caja_rover_arrastrando = c_rover; break
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        if caja_rover_arrastrando:
                            if deposito_base.colliderect(caja_rover_arrastrando["rect"]):
                                caja_rover_arrastrando["rect"].center = deposito_base.center
                            caja_rover_arrastrando = None
                    elif evento.type == pygame.MOUSEMOTION and caja_rover_arrastrando:
                        caja_rover_arrastrando["rect"].center = (mx, my)

            elif modulo_minijuego_activo == 4:
                if id_minijuego == 1:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for b_eva in botones_eva:
                            if b_eva["rect"].collidepoint(mx, my): secuencia_eva_usuario.append(b_eva["val"])
                elif id_minijuego == 2:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if parche_eva_rect.collidepoint(mx, my): parche_eva_arrastrando = True
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        parche_eva_arrastrando = False
                    elif evento.type == pygame.MOUSEMOTION and parche_eva_arrastrando:
                        parche_eva_rect.center = (mx, my)
                elif id_minijuego == 3:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for idx, r_cierre in enumerate(cierres_rects):
                            if r_cierre.collidepoint(mx, my): cierres_casco[idx] = not cierres_casco[idx]
                elif id_minijuego == 4:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_cargar_jetpack.collidepoint(mx, my): carga_jetpack += 25.0
                elif id_minijuego == 5:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if mosqueton_rect.collidepoint(mx, my): mosqueton_arrastrando = True
                    elif evento.type == pygame.MOUSEBUTTONUP:
                        if mosqueton_arrastrando:
                            if guia_seguridad.colliderect(mosqueton_rect): mosqueton_rect.center = guia_seguridad.center
                            mosqueton_arrastrando = False
                    elif evento.type == pygame.MOUSEMOTION and mosqueton_arrastrando:
                        mosqueton_rect.center = (mx, my)

            elif modulo_minijuego_activo == 5:
                if id_minijuego == 1:
                    if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION) and (evento.type == pygame.MOUSEBUTTONDOWN or pygame.mouse.get_pressed()[0]):
                        rect_slider = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 + 30, 240, 20)
                        if rect_slider.collidepoint(mx, my):
                            nivel_escudo_rad = float(((mx - rect_slider.x) / rect_slider.width) * 100.0)
                elif id_minijuego == 2:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_freq_mas.collidepoint(mx, my): frecuencia_antena = round(frecuencia_antena + 1.0, 1)
                        elif btn_freq_menos.collidepoint(mx, my): frecuencia_antena = round(frecuencia_antena - 1.0, 1)
                elif id_minijuego == 3:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if btn_freno_viento.collidepoint(mx, my): freno_viento += 25.0
                elif id_minijuego == 4:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for p_sens in polvo_sensores[:]:
                            if p_sens.collidepoint(mx, my): polvo_sensores.remove(p_sens)
                elif id_minijuego == 5:
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        for b_press in botones_press:
                            if b_press["rect"].collidepoint(mx, my): secuencia_press_usuario.append(b_press["val"])

    # Mantener espacio cinco segundos permite saltar cualquier fase del tutorial.
    if tutorial_activo and dia_actual == 1 and estado_juego in ("JUGANDO", "MINIJUEGO") and not ayuda_jj_abierta:
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            tiempo_espacio_tutorial += dt
            if tiempo_espacio_tutorial >= PROGRESO_SALTO_TUTORIAL:
                tutorial_activo = False
                tutorial_fase = "omitido"
                tiempo_espacio_tutorial = 0.0
                mencion_interaccion = "Tutorial omitido. ¡Buena suerte en la misión!"
        else:
            tiempo_espacio_tutorial = 0.0
    else:
        tiempo_espacio_tutorial = 0.0

    # B. COMPROBACIÓN DE VICTORIA EN MINIJUEGOS
    if estado_juego == "MINIJUEGO":
        if modulo_minijuego_activo == 2 and id_minijuego == 6:
            temporizador_feedback_ingesta = max(0.0, temporizador_feedback_ingesta - dt)
            if ingesta_procesando:
                temporizador_ingesta += dt
                if temporizador_ingesta >= 0.7:
                    ingesta_muestras = [m for m in ingesta_muestras if not m["procesando"]]
                    progreso_ingesta += 1
                    ingesta_procesando = False
                    temporizador_ingesta = 0.0
                    feedback_ingesta = f"Muestra procesada: {progreso_ingesta}/3"
                    temporizador_feedback_ingesta = 1.1
        if modulo_minijuego_activo == 2 and id_minijuego == 2:
            temporizador_feedback_analisis = max(0.0, temporizador_feedback_analisis - dt)
        if modulo_minijuego_activo == 1 and id_minijuego == 3:
            temporizador_feedback_fuga = max(0.0, temporizador_feedback_fuga - dt)
        mision_completada_flag = False

        if modulo_minijuego_activo == 0:
            if id_minijuego == 1 and 20.0 <= temp_actual <= 22.0:
                tiempo_en_target += dt
                if tiempo_en_target >= 1.5: mision_completada_flag = True
            elif id_minijuego == 2 and luces_estado == [True, False, True, False]: mision_completada_flag = True
            elif id_minijuego == 3 and len(manchas_polvo) == 0: mision_completada_flag = True
            elif id_minijuego == 4:
                almacenados = sum(1 for p in paquetes for c in cajas_destino if c["rect"].contains(p["rect"]) and c["tipo"] == p["tipo"])
                if almacenados == len(paquetes): mision_completada_flag = True
            elif id_minijuego == 5 and all(45 <= n <= 55 for n in eq_niveles): mision_completada_flag = True

        elif modulo_minijuego_activo == 1:
            if id_minijuego == 1 and progreso_valvula >= 100.0: mision_completada_flag = True
            elif id_minijuego == 2 and (76 <= n2_nivel <= 80) and (19 <= o2_nivel <= 23): mision_completada_flag = True
            elif id_minijuego == 3 and fuga_reparada: mision_completada_flag = True
            elif id_minijuego == 4:
                if secuencia_drenaje_usuario == [1, 2, 3]: mision_completada_flag = True
                elif len(secuencia_drenaje_usuario) >= 3 and secuencia_drenaje_usuario != [1, 2, 3]: secuencia_drenaje_usuario = []
            elif id_minijuego == 5 and estado_co2 == 2: mision_completada_flag = True

        elif modulo_minijuego_activo == 2:
            if id_minijuego == 1 and len(conexiones_hechas) == 3: mision_completada_flag = True
            elif id_minijuego == 2 and indice_analisis >= len(analisis_muestras): mision_completada_flag = True
            elif id_minijuego == 3:
                almacenados = sum(1 for r in rocas for c_r in cajas_rocas if c_r["rect"].contains(r["rect"]) and c_r["tipo"] == r["tipo"])
                if almacenados == len(rocas): mision_completada_flag = True
            elif id_minijuego == 4:
                if secuencia_bio_usuario == secuencia_bio_objetivo: mision_completada_flag = True
                elif len(secuencia_bio_usuario) >= 4 and secuencia_bio_usuario != secuencia_bio_objetivo: secuencia_bio_usuario = []
            elif id_minijuego == 5 and ph_actual == 6.5: mision_completada_flag = True
            elif id_minijuego == 6 and progreso_ingesta >= 3: mision_completada_flag = True

        elif modulo_minijuego_activo == 3:
            if id_minijuego == 1:
                garra_rect = pygame.Rect(garra_pos[0], garra_pos[1], 50, 50)
                if puerto_target.contains(garra_rect): mision_completada_flag = True
            elif id_minijuego == 2 and carga_rover >= 100.0: mision_completada_flag = True
            elif id_minijuego == 3 and 30.0 <= psi_neumatico <= 35.0: mision_completada_flag = True
            elif id_minijuego == 4 and len(manchas_uv) == 0: mision_completada_flag = True
            elif id_minijuego == 5:
                almacenados = sum(1 for c_rover in cajas_rover if deposito_base.contains(c_rover["rect"]))
                if almacenados == len(cajas_rover): mision_completada_flag = True

        elif modulo_minijuego_activo == 4:
            if id_minijuego == 1:
                if secuencia_eva_usuario == [1, 2, 3]: mision_completada_flag = True
                elif len(secuencia_eva_usuario) >= 3 and secuencia_eva_usuario != [1, 2, 3]: secuencia_eva_usuario = []
            elif id_minijuego == 2 and fisura_traje.contains(parche_eva_rect): mision_completada_flag = True
            elif id_minijuego == 3 and all(cierres_casco): mision_completada_flag = True
            elif id_minijuego == 4 and carga_jetpack >= 100.0: mision_completada_flag = True
            elif id_minijuego == 5 and guia_seguridad.contains(mosqueton_rect): mision_completada_flag = True

        elif modulo_minijuego_activo == 5:
            if id_minijuego == 1 and 70.0 <= nivel_escudo_rad <= 80.0: mision_completada_flag = True
            elif id_minijuego == 2 and frecuencia_antena == 95.0: mision_completada_flag = True
            elif id_minijuego == 3 and freno_viento >= 100.0: mision_completada_flag = True
            elif id_minijuego == 4 and len(polvo_sensores) == 0: mision_completada_flag = True
            elif id_minijuego == 5:
                if secuencia_press_usuario == [1, 2, 3]: mision_completada_flag = True
                elif len(secuencia_press_usuario) >= 3 and secuencia_press_usuario != [1, 2, 3]: secuencia_press_usuario = []

        if mision_completada_flag and mision_en_curso and mision_en_curso.get("mision_repetible"):
            mision_en_curso["repeticiones_completadas"] += 1
            repeticiones_hechas = mision_en_curso["repeticiones_completadas"]
            repeticiones_necesarias = mision_en_curso["repeticiones_requeridas"]
            mision_en_curso["desc"] = f"Extra del comandante · Repeticiones: {repeticiones_hechas}/{repeticiones_necesarias}"
            if repeticiones_hechas < repeticiones_necesarias:
                mision_completada_flag = False
                minijuego_activo = False
                estado_juego = "JUGANDO"
                mencion_interaccion = f"Ronda {repeticiones_hechas}/3 lista. Repite la misión para completar la tarea extra."
                if mision_tutorial_seleccionada is mision_en_curso:
                    mision_tutorial_seleccionada = None
                mision_en_curso = None

        if mision_completada_flag:
            mision_en_curso["completada"] = True
            minijuego_activo = False
            mencion_interaccion = f"¡Misión Completada!: {mision_en_curso['nombre']}"
            if mision_tutorial_seleccionada is mision_en_curso:
                mision_tutorial_seleccionada = None

            if dia_actual == 1 and tutorial_activo:
                if tutorial_fase == "hacer_urgente":
                    tutorial_fase = "elegir_secundaria"
                    panel_misiones_abierto = False
                elif tutorial_fase == "hacer_secundaria":
                    tutorial_fase = "final"
                    texto_tutorial_indice = 0.0
            
            # Congelar barra de recursos cuando la misión correspondiente se completa
            if mision_en_curso["modulo_id"] == 0 and ("Ración" in mision_en_curso["nombre"] or "Inventario" in mision_en_curso["nombre"]): comida = 100.0; comida_congelado = True
            elif mision_en_curso["modulo_id"] == 1: oxigeno = 100.0; oxigeno_congelado = True
            elif mision_en_curso["modulo_id"] == 5 and "Escudo" in mision_en_curso["nombre"]: radiacion = 100.0; radiacion_congelado = True

            estado_juego = "JUGANDO"
            if misiones_del_dia and all(m["completada"] for m in misiones_del_dia):
                dias_ignorados_acumulados = 0
                estado_juego = "DIA_TERMINADO"
                mision_en_curso = None

    # C. LÓGICA DE DÍA Y BARRAS DE SUPERVIVENCIA
    if estado_juego in ("JUGANDO", "MINIJUEGO") and not ayuda_jj_abierta:
        if creditos > 0:
            # En el Día 1 las barras bajan a velocidad reducida (30% de la velocidad normal)
            mult_velocidad_dia = 0.3 if dia_actual == 1 else 1.0

            tutorial_bloquea_consumo = dia_actual == 1 and tutorial_activo
            if not tutorial_bloquea_consumo and not oxigeno_congelado:
                factor_o2 = 1.5
                oxigeno -= factor_o2 * multiplicador_oxigeno_dia * dt * mult_velocidad_dia
                if dia_actual == 1: oxigeno = max(30.0, oxigeno)
                else: oxigeno = max(0.0, oxigeno)

            if not tutorial_bloquea_consumo and not comida_congelado:
                comida -= 1.2 * multiplicador_comida_dia * dt * mult_velocidad_dia
                if dia_actual == 1: comida = max(30.0, comida)
                else: comida = max(0.0, comida)

            if not tutorial_bloquea_consumo and not radiacion_congelado:
                radiacion -= 1.3 * multiplicador_radiacion_dia * dt * mult_velocidad_dia
                if dia_actual == 1: radiacion = max(30.0, radiacion)
                else: radiacion = max(0.0, radiacion)

            if not tutorial_bloquea_consumo:
                tiempo_dia -= dt

            # MUERTE
            if oxigeno <= 0 or comida <= 0 or radiacion <= 0:
                creditos = 0
                desbloquear_final("MUERTE")
                barra_vacia = "oxígeno" if oxigeno <= 0 else ("comida" if comida <= 0 else "radiación")
                mencion_interaccion = f"Fallaste: se agotó la barra de {barra_vacia}."
                estado_juego = "FINAL_MUERTE"

            # FIN DEL DÍA
            if tiempo_dia <= 0 and creditos > 0 and estado_juego in ("JUGANDO", "MINIJUEGO"):
                dia_completo = bool(misiones_del_dia) and all(m["completada"] for m in misiones_del_dia)
                if dia_completo:
                    dias_ignorados_acumulados = 0
                else:
                    dias_ignorados_acumulados += 1

                if dias_ignorados_acumulados >= 4:
                    creditos = 0
                    desbloquear_final("REGRESO")
                    mencion_interaccion = "Cuatro días seguidos con misiones pendientes. La NASA cancela la expedición y vuelves a casa."
                    estado_juego = "FINAL_REGRESO"
                elif dia_actual >= 14 and not dia_completo:
                    creditos = 0
                    desbloquear_final("REGRESO")
                    mencion_interaccion = "La misión terminó con tareas pendientes. La NASA cancela la expedición y vuelves a casa."
                    estado_juego = "FINAL_REGRESO"
                elif dia_actual >= 14:
                    desbloquear_final("FELIZ")
                    estado_juego = "FINALES"
                else:
                    minijuego_activo = False
                    mision_en_curso = None
                    mision_tutorial_seleccionada = None
                    panel_misiones_abierto = False
                    if dias_ignorados_acumulados > 0:
                        mencion_interaccion = f"Jornada incompleta ({dias_ignorados_acumulados}/4). La racha se reinicia si completas todas las misiones de un día."
                    dia_actual += 1
                    tiempo_dia = duracion_dia_actual
                    preparar_evento_nuevo_dia()
                    misiones_del_dia = generar_misiones_diarias()
                    estado_juego = "NUEVO_DIA"

    # D. RENDERIZADO
    pantalla.fill(NEGRO_ESPACIAL)

    if estado_juego == "MENU_PRINCIPAL":
        txt_titulo = fuente_titulo.render("M.A.R.S. - SIMULADOR", True, NARANJA_MARTE)
        pantalla.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 80))

        for btn, texto in [(btn_iniciar, "Iniciar Partida"), (btn_continuar, "Continuar"), (btn_finales, "Finales"), (btn_bibliografia, "Enciclopedia")]:
            pygame.draw.rect(pantalla, AZUL_UI, btn, border_radius=8)
            pygame.draw.rect(pantalla, BLANCO, btn, width=2, border_radius=8)
            t = fuente_menu.render(texto, True, BLANCO)
            pantalla.blit(t, (btn.centerx - t.get_width() // 2, btn.centery - t.get_height() // 2))

    elif estado_juego == "CAPTURA_JUGADOR":
        titulo_datos = fuente_titulo.render("ANTES DE DESPEGAR", True, NARANJA_MARTE)
        pantalla.blit(titulo_datos, (ANCHO // 2 - titulo_datos.get_width() // 2, 95))
        subtitulo_datos = fuente_hud.render("Completa tu ficha de astronauta junior", True, BLANCO)
        pantalla.blit(subtitulo_datos, (ANCHO // 2 - subtitulo_datos.get_width() // 2, 155))

        etiqueta_nombre = fuente_menu.render("Soy...", True, VERDE_BRILLANTE)
        pantalla.blit(etiqueta_nombre, (campo_nombre_rect.x, campo_nombre_rect.y - 28))
        pygame.draw.rect(pantalla, GRIS_OSCURO, campo_nombre_rect, border_radius=6)
        pygame.draw.rect(pantalla, DORADO_MANDO if campo_formulario_activo == "nombre" else GRIS_MEDIO, campo_nombre_rect, width=2, border_radius=6)
        texto_nombre = nombre_jugador if nombre_jugador else "Escribe tu nombre"
        pantalla.blit(fuente_menu.render(texto_nombre, True, BLANCO if nombre_jugador else TEXTO_DESHABILITADO), (campo_nombre_rect.x + 12, campo_nombre_rect.y + 11))

        etiqueta_edad = fuente_menu.render("Y tengo... años (de 1 a 105)", True, VERDE_BRILLANTE)
        pantalla.blit(etiqueta_edad, (campo_edad_rect.x, campo_edad_rect.y - 28))
        pygame.draw.rect(pantalla, GRIS_OSCURO, campo_edad_rect, border_radius=6)
        pygame.draw.rect(pantalla, DORADO_MANDO if campo_formulario_activo == "edad" else GRIS_MEDIO, campo_edad_rect, width=2, border_radius=6)
        texto_edad = edad_jugador if edad_jugador else "Edad"
        pantalla.blit(fuente_menu.render(texto_edad, True, BLANCO if edad_jugador else TEXTO_DESHABILITADO), (campo_edad_rect.x + 12, campo_edad_rect.y + 11))

        pygame.draw.rect(pantalla, AZUL_UI, btn_confirmar_datos, border_radius=8)
        pygame.draw.rect(pantalla, BLANCO, btn_confirmar_datos, width=2, border_radius=8)
        texto_confirmar = fuente_menu.render("Continuar", True, BLANCO)
        pantalla.blit(texto_confirmar, (btn_confirmar_datos.centerx - texto_confirmar.get_width() // 2, btn_confirmar_datos.centery - texto_confirmar.get_height() // 2))
        if mensaje_formulario:
            error_datos = fuente_hud.render(mensaje_formulario, True, ROJO_ALERTA)
            pantalla.blit(error_datos, (ANCHO // 2 - error_datos.get_width() // 2, 480))
        pista_datos = fuente_hud.render("Haz clic en un campo para escribir. Usa Tab para cambiar de campo.", True, BLANCO)
        pantalla.blit(pista_datos, (ANCHO // 2 - pista_datos.get_width() // 2, 530))

    elif estado_juego == "INTRO":
        if texto_intro_indice < len(texto_historia_completo):
            texto_intro_indice += VELOCIDAD_TEXTO * dt
            if texto_intro_indice > len(texto_historia_completo):
                texto_intro_indice = float(len(texto_historia_completo))

        texto_a_mostrar = texto_historia_completo[:int(texto_intro_indice)]

        txt_sub = fuente_titulo.render("[ TRANSMISIÓN ENTRANTE... ]", True, NARANJA_MARTE)
        pantalla.blit(txt_sub, (ANCHO // 2 - txt_sub.get_width() // 2, 40))

        rect_intro = pygame.Rect(80, 95, 740, 390)
        pygame.draw.rect(pantalla, GRIS_OSCURO, rect_intro, border_radius=12)
        pygame.draw.rect(pantalla, VERDE_OK, rect_intro, width=2, border_radius=12)

        ANCHO_MAX_TEXTO = 680
        lineas_formateadas = obtener_lineas_texto(texto_a_mostrar, fuente_robotica, ANCHO_MAX_TEXTO)

        y_lin = 125
        for l in lineas_formateadas:
            if l:
                t_lin = fuente_robotica.render(l, True, VERDE_BRILLANTE)
                pantalla.blit(t_lin, (110, y_lin))
            y_lin += 30

        pygame.draw.rect(pantalla, AZUL_UI, btn_continuar_intro, border_radius=8)
        pygame.draw.rect(pantalla, BLANCO, btn_continuar_intro, width=2, border_radius=8)

        lbl_btn = "Continuar [Espacio]" if int(texto_intro_indice) >= len(texto_historia_completo) else "Saltar Texto"
        t_c = fuente_hud.render(lbl_btn, True, BLANCO)
        pantalla.blit(t_c, (btn_continuar_intro.centerx - t_c.get_width() // 2, btn_continuar_intro.centery - t_c.get_height() // 2))

    elif estado_juego == "CONTINUAR":
        txt = fuente_titulo.render("Partidas guardadas", True, NARANJA_MARTE)
        pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, 45))
        txt_info = fuente_hud.render(mensaje_partidas, True, BLANCO)
        pantalla.blit(txt_info, (ANCHO // 2 - txt_info.get_width() // 2, 88))

        if not partidas_guardadas:
            txt_vacio = fuente_menu.render("Tus partidas guardadas aparecerán aquí.", True, TEXTO_DESHABILITADO)
            pantalla.blit(txt_vacio, (ANCHO // 2 - txt_vacio.get_width() // 2, 250))
        else:
            total_paginas = max(1, (len(partidas_guardadas) + len(rects_partidas) - 1) // len(rects_partidas))
            inicio_pagina = pagina_partidas * len(rects_partidas)
            for idx, rect_partida in enumerate(rects_partidas):
                indice_partida = inicio_pagina + idx
                if indice_partida >= len(partidas_guardadas):
                    break
                partida = partidas_guardadas[indice_partida]
                pygame.draw.rect(pantalla, GRIS_OSCURO, rect_partida, border_radius=7)
                pygame.draw.rect(pantalla, AZUL_UI, rect_partida, width=2, border_radius=7)
                texto_partida = fuente_ficha_bold.render(partida.get("titulo", f"Partida guardada {indice_partida + 1}"), True, BLANCO)
                pantalla.blit(texto_partida, (rect_partida.x + 14, rect_partida.y + 7))
                detalle_partida = fuente_ficha.render(f"Guardada: {partida.get('fecha', 'fecha desconocida')}  ·  Clic para reanudar", True, TEXTO_DESHABILITADO)
                pantalla.blit(detalle_partida, (rect_partida.x + 14, rect_partida.y + 30))
            pygame.draw.rect(pantalla, GRIS_MEDIO, btn_pagina_anterior, border_radius=5)
            pygame.draw.rect(pantalla, GRIS_MEDIO if pagina_partidas + 1 >= total_paginas else AZUL_UI, btn_pagina_siguiente, border_radius=5)
            pantalla.blit(fuente_hud.render("<", True, BLANCO), (btn_pagina_anterior.centerx - 4, btn_pagina_anterior.y + 10))
            pantalla.blit(fuente_hud.render(">", True, BLANCO), (btn_pagina_siguiente.centerx - 4, btn_pagina_siguiente.y + 10))
            contador_paginas = fuente_hud.render(f"Página {pagina_partidas + 1}/{total_paginas}", True, BLANCO)
            pantalla.blit(contador_paginas, (ANCHO // 2 - contador_paginas.get_width() // 2, 540))

        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_volver, border_radius=5)
        t_vol = fuente_hud.render("Volver", True, BLANCO)
        pantalla.blit(t_vol, (btn_volver.centerx - t_vol.get_width() // 2, btn_volver.centery - t_vol.get_height() // 2))

    elif estado_juego == "FINAL_MUERTE":
        titulo_fatal = fuente_titulo.render("FALLASTE", True, ROJO_ALERTA)
        pantalla.blit(titulo_fatal, (ANCHO // 2 - titulo_fatal.get_width() // 2, 145))
        motivo_fatal = fuente_menu.render(mencion_interaccion or "Se agotó un recurso vital de la base.", True, BLANCO)
        pantalla.blit(motivo_fatal, (ANCHO // 2 - motivo_fatal.get_width() // 2, 230))
        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_volver, border_radius=5)
        texto_fin_menu = fuente_hud.render("Volver al menú", True, BLANCO)
        pantalla.blit(texto_fin_menu, (btn_volver.centerx - texto_fin_menu.get_width() // 2, btn_volver.centery - texto_fin_menu.get_height() // 2))

    elif estado_juego == "FINAL_REGRESO":
        titulo_regreso = fuente_titulo.render("REGRESO A CASA", True, AMARILLO)
        pantalla.blit(titulo_regreso, (ANCHO // 2 - titulo_regreso.get_width() // 2, 145))
        motivo_regreso = fuente_ficha.render(mencion_interaccion or "La NASA canceló la expedición por misiones pendientes.", True, BLANCO)
        pantalla.blit(motivo_regreso, (ANCHO // 2 - motivo_regreso.get_width() // 2, 230))
        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_volver, border_radius=5)
        texto_regreso_menu = fuente_hud.render("Volver al menú", True, BLANCO)
        pantalla.blit(texto_regreso_menu, (btn_volver.centerx - texto_regreso_menu.get_width() // 2, btn_volver.centery - texto_regreso_menu.get_height() // 2))

    elif estado_juego == "FINALES":
        txt = fuente_titulo.render("Galería de Finales", True, NARANJA_MARTE)
        pantalla.blit(txt, (ANCHO // 2 - txt.get_width() // 2, 50))

        f_feliz = "1. FINAL FELIZ · DESBLOQUEADO" if finales_desbloqueados["FELIZ"] else "1. FINAL FELIZ · BLOQUEADO"
        f_regreso = "2. FINAL REGRESO · DESBLOQUEADO" if finales_desbloqueados["REGRESO"] else "2. FINAL REGRESO · BLOQUEADO"
        f_muerte = "3. FINAL FATAL · DESBLOQUEADO" if finales_desbloqueados["MUERTE"] else "3. FINAL FATAL · BLOQUEADO"

        pantalla.blit(fuente_hud.render(f_feliz, True, VERDE_OK if finales_desbloqueados["FELIZ"] else BLANCO), (100, 180))
        pantalla.blit(fuente_hud.render(f_regreso, True, AMARILLO if finales_desbloqueados["REGRESO"] else BLANCO), (100, 240))
        pantalla.blit(fuente_hud.render(f_muerte, True, ROJO_ALERTA if finales_desbloqueados["MUERTE"] else BLANCO), (100, 300))

        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_volver, border_radius=5)
        t_vol = fuente_hud.render("Volver", True, BLANCO)
        pantalla.blit(t_vol, (btn_volver.centerx - t_vol.get_width() // 2, btn_volver.centery - t_vol.get_height() // 2))

    elif estado_juego == "DIA_TERMINADO":
        pygame.draw.rect(pantalla, NEGRO_ESPACIAL, (0, 0, ANCHO, ALTO))
        etiqueta_fin = fuente_titulo.render(f"DÍA {dia_actual} TERMINADO", True, NARANJA_MARTE)
        pantalla.blit(etiqueta_fin, (ANCHO // 2 - etiqueta_fin.get_width() // 2, 155))
        linea_fin = fuente_menu.render("Completaste todas tus misiones.", True, BLANCO)
        pantalla.blit(linea_fin, (ANCHO // 2 - linea_fin.get_width() // 2, 230))
        detalle_fin = fuente_ficha.render("La tripulación asegura la base para pasar a la siguiente jornada.", True, AZUL_UI)
        pantalla.blit(detalle_fin, (ANCHO // 2 - detalle_fin.get_width() // 2, 275))
        pygame.draw.rect(pantalla, AZUL_UI, btn_dia_terminado, border_radius=8)
        pygame.draw.rect(pantalla, BLANCO, btn_dia_terminado, width=2, border_radius=8)
        texto_fin_btn = "Ver resultado de misión" if dia_actual >= 14 else f"Preparar Día {dia_actual + 1}"
        texto_fin_btn = fuente_menu.render(texto_fin_btn, True, BLANCO)
        pantalla.blit(texto_fin_btn, (btn_dia_terminado.centerx - texto_fin_btn.get_width() // 2, btn_dia_terminado.centery - texto_fin_btn.get_height() // 2))

    elif estado_juego == "NUEVO_DIA":
        pygame.draw.rect(pantalla, NEGRO_ESPACIAL, (0, 0, ANCHO, ALTO))
        etiqueta_nuevo = fuente_titulo.render(f"DÍA {dia_actual}", True, NARANJA_MARTE)
        pantalla.blit(etiqueta_nuevo, (ANCHO // 2 - etiqueta_nuevo.get_width() // 2, 130))
        lineas_evento = obtener_lineas_texto(evento_dia_mensaje, fuente_menu, 700)
        y_evento = 220
        for linea_evento in lineas_evento:
            texto_evento = fuente_menu.render(linea_evento, True, BLANCO)
            pantalla.blit(texto_evento, (ANCHO // 2 - texto_evento.get_width() // 2, y_evento))
            y_evento += 34
        pygame.draw.rect(pantalla, AZUL_UI, btn_nuevo_dia, border_radius=8)
        pygame.draw.rect(pantalla, BLANCO, btn_nuevo_dia, width=2, border_radius=8)
        texto_inicio_dia = fuente_menu.render("Iniciar jornada", True, BLANCO)
        pantalla.blit(texto_inicio_dia, (btn_nuevo_dia.centerx - texto_inicio_dia.get_width() // 2, btn_nuevo_dia.centery - texto_inicio_dia.get_height() // 2))

    elif estado_juego == "BIBLIOGRAFIA":
        titulo_biblio = fuente_titulo.render("Enciclopedia de misión", True, NARANJA_MARTE)
        pantalla.blit(titulo_biblio, (ANCHO // 2 - titulo_biblio.get_width() // 2, 28))
        total_desbloqueados = len(conceptos_desbloqueados["salas"]) + len(conceptos_desbloqueados["objetos"])
        estado_progreso = fuente_hud.render(f"Conceptos descubiertos: {total_desbloqueados}", True, AZUL_UI)
        pantalla.blit(estado_progreso, (ANCHO - estado_progreso.get_width() - 25, 62))

        pygame.draw.rect(pantalla, GRIS_OSCURO, (18, 90, 230, 430), border_radius=9)
        pygame.draw.rect(pantalla, AZUL_UI, (18, 90, 230, 430), width=2, border_radius=9)
        etiqueta_salas = fuente_ficha_bold.render("SALAS", True, NARANJA_MARTE)
        pantalla.blit(etiqueta_salas, (32, 73))
        for idx_sala, rect_sala in enumerate(rects_bibliografia_salas):
            sala_id = SALAS_BIBLIOGRAFIA_VISIBLES[idx_sala]
            sala_desbloqueada = sala_id in conceptos_desbloqueados["salas"]
            seleccionada = sala_id == bibliografia_modulo
            color_sala = AZUL_UI if seleccionada else (GRIS_MEDIO if sala_desbloqueada else GRIS_DESHABILITADO)
            pygame.draw.rect(pantalla, color_sala, rect_sala, border_radius=6)
            pygame.draw.rect(pantalla, VERDE_OK if sala_desbloqueada else GRIS_MEDIO, rect_sala, width=2, border_radius=6)
            prefijo_sala = "✓ " if sala_desbloqueada else "· "
            lineas_nombre_sala = obtener_lineas_texto(prefijo_sala + modulos[sala_id]["nombre"], fuente_ficha_bold, rect_sala.width - 16)
            y_nombre_sala = rect_sala.y + (rect_sala.height - min(2, len(lineas_nombre_sala)) * 17) // 2
            for linea_nombre in lineas_nombre_sala[:2]:
                tex_sala = fuente_ficha_bold.render(linea_nombre, True, BLANCO if sala_desbloqueada or seleccionada else TEXTO_DESHABILITADO)
                pantalla.blit(tex_sala, (rect_sala.x + 8, y_nombre_sala))
                y_nombre_sala += 17

        pygame.draw.rect(pantalla, GRIS_OSCURO, (258, 90, 625, 430), border_radius=9)
        pygame.draw.rect(pantalla, AZUL_UI, (258, 90, 625, 430), width=2, border_radius=9)
        for boton_tab, etiqueta_tab, tab_id in (
            (tab_bibliografia_general, "General", "GENERAL"),
            (tab_bibliografia_objetos, "Objetos", "OBJETOS")
        ):
            activo = bibliografia_seccion == tab_id
            pygame.draw.rect(pantalla, AZUL_UI if activo else GRIS_MEDIO, boton_tab, border_radius=6)
            pygame.draw.rect(pantalla, BLANCO, boton_tab, width=1, border_radius=6)
            texto_tab = fuente_menu.render(etiqueta_tab, True, BLANCO)
            pantalla.blit(texto_tab, (boton_tab.centerx - texto_tab.get_width() // 2, boton_tab.centery - texto_tab.get_height() // 2))

        sala_info = bibliografia_salas.get(bibliografia_modulo, {})
        if bibliografia_seccion == "GENERAL":
            nombre_sala = fuente_menu.render(modulos[bibliografia_modulo]["nombre"], True, BLANCO)
            pantalla.blit(nombre_sala, (278, 165))
            if bibliografia_modulo not in conceptos_desbloqueados["salas"]:
                aviso_bloqueo = fuente_menu.render("Sala aún no explorada", True, TEXTO_DESHABILITADO)
                pantalla.blit(aviso_bloqueo, (278, 218))
                detalle_bloqueo = fuente_ficha.render("Entra en esta sala durante la misión para desbloquear su descripción.", True, BLANCO)
                pantalla.blit(detalle_bloqueo, (278, 255))
            elif "general" not in sala_info:
                pendiente_biblio = fuente_ficha.render("La descripción de esta sala se añadirá próximamente.", True, TEXTO_DESHABILITADO)
                pantalla.blit(pendiente_biblio, (278, 218))
            else:
                texto_general = fuente_ficha.render("DEFINICIÓN GENERAL", True, VERDE_OK)
                pantalla.blit(texto_general, (278, 210))
                lineas_general = obtener_lineas_texto(sala_info["general"], fuente_ficha, 565)
                y_general = 240
                for linea_general in lineas_general:
                    pantalla.blit(fuente_ficha.render(linea_general, True, BLANCO), (278, y_general))
                    y_general += 22
        else:
            objetos_sala = sala_info.get("objetos", [])
            if not objetos_sala:
                sin_objetos = fuente_ficha.render("Los objetos de esta sala se incorporarán cuando recibamos sus fichas.", True, TEXTO_DESHABILITADO)
                pantalla.blit(sin_objetos, (278, 170))
            else:
                for idx_objeto, objeto_info in enumerate(objetos_sala[:len(rects_bibliografia_objetos)]):
                    rect_objeto = rects_bibliografia_objetos[idx_objeto]
                    descubierto = objeto_info["id"] in conceptos_desbloqueados["objetos"]
                    seleccionado_objeto = bibliografia_objeto == objeto_info["id"]
                    color_objeto = AZUL_UI if seleccionado_objeto else (GRIS_MEDIO if descubierto else GRIS_DESHABILITADO)
                    pygame.draw.rect(pantalla, color_objeto, rect_objeto, border_radius=5)
                    pygame.draw.rect(pantalla, VERDE_OK if descubierto else GRIS_MEDIO, rect_objeto, width=1, border_radius=5)
                    prefijo_objeto = "✓ " if descubierto else "BLOQ. "
                    etiqueta_objeto = fuente_ficha_bold.render(prefijo_objeto + objeto_info["nombre"], True, BLANCO if descubierto or seleccionado_objeto else TEXTO_DESHABILITADO)
                    pantalla.blit(etiqueta_objeto, (rect_objeto.x + 8, rect_objeto.centery - etiqueta_objeto.get_height() // 2))

                if bibliografia_objeto:
                    objeto_actual = next((o for o in objetos_sala if o["id"] == bibliografia_objeto), None)
                else:
                    objeto_actual = None
                if objeto_actual:
                    if objeto_actual["id"] in conceptos_desbloqueados["objetos"]:
                        titulo_objeto = fuente_menu.render(objeto_actual["nombre"], True, BLANCO)
                        pantalla.blit(titulo_objeto, (520, 175))
                        subtitulo_objeto = fuente_ficha.render("FICHA DEL OBJETO", True, VERDE_OK)
                        pantalla.blit(subtitulo_objeto, (520, 210))
                        lineas_objeto = obtener_lineas_texto(objeto_actual["definicion"], fuente_ficha, 335)
                        y_objeto = 242
                        for linea_objeto in lineas_objeto:
                            pantalla.blit(fuente_ficha.render(linea_objeto, True, BLANCO), (520, y_objeto))
                            y_objeto += 22
                    else:
                        titulo_bloqueado = fuente_menu.render("Concepto bloqueado", True, TEXTO_DESHABILITADO)
                        pantalla.blit(titulo_bloqueado, (520, 175))
                        texto_desbloqueo = fuente_ficha.render("Interactúa con este equipo e inicia su minijuego para descubrir la ficha.", True, BLANCO)
                        lineas_desbloqueo = obtener_lineas_texto(texto_desbloqueo, fuente_ficha, 335)
                        y_objeto = 218
                        for linea_bloqueo in lineas_desbloqueo:
                            pantalla.blit(fuente_ficha.render(linea_bloqueo, True, TEXTO_DESHABILITADO), (520, y_objeto))
                            y_objeto += 22
                else:
                    elegir_objeto = fuente_ficha.render("Elige una ficha para leer su definición.", True, BLANCO)
                    pantalla.blit(elegir_objeto, (520, 175))

        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_volver_bibliografia, border_radius=5)
        txt_volver_biblio = fuente_hud.render("Volver al menú", True, BLANCO)
        pantalla.blit(txt_volver_biblio, (btn_volver_bibliografia.centerx - txt_volver_biblio.get_width() // 2, btn_volver_bibliografia.centery - txt_volver_biblio.get_height() // 2))

    elif estado_juego == "PAUSA":
        pygame.draw.rect(pantalla, NEGRO_ESPACIAL, (0, 0, ANCHO, ALTO))
        titulo_pausa = fuente_titulo.render("MISIÓN EN PAUSA", True, NARANJA_MARTE)
        pantalla.blit(titulo_pausa, (ANCHO // 2 - titulo_pausa.get_width() // 2, 150))
        for boton, etiqueta in ((btn_reanudar, "Reanudar"), (btn_menu_pausa, "Volver al menú"), (btn_guardar_pausa, "Guardar partida")):
            pygame.draw.rect(pantalla, AZUL_UI, boton, border_radius=8)
            pygame.draw.rect(pantalla, BLANCO, boton, width=2, border_radius=8)
            texto_boton = fuente_menu.render(etiqueta, True, BLANCO)
            pantalla.blit(texto_boton, (boton.centerx - texto_boton.get_width() // 2, boton.centery - texto_boton.get_height() // 2))
        if mensaje_guardado:
            txt_guardado = fuente_hud.render(mensaje_guardado, True, VERDE_OK if "correctamente" in mensaje_guardado else ROJO_ALERTA)
            pantalla.blit(txt_guardado, (ANCHO // 2 - txt_guardado.get_width() // 2, 465))

    elif estado_juego == "SELECCION":
        txt_sel = fuente_titulo.render(f"Catálogo de Compañeros ({len(comodines_elegidos)}/2 Elegidos)", True, NARANJA_MARTE)
        pantalla.blit(txt_sel, (ANCHO // 2 - txt_sel.get_width() // 2, 35))

        esta_elegido = indice_catalogo in comodines_elegidos
        deshabilitado = (not esta_elegido and len(comodines_elegidos) >= 2)

        color_marco_cat = GRIS_DESHABILITADO if deshabilitado else GRIS_OSCURO
        color_borde_cat = GRIS_MEDIO if deshabilitado else AZUL_UI

        rect_catalogo = pygame.Rect(110, 90, 680, 370)
        pygame.draw.rect(pantalla, color_marco_cat, rect_catalogo, border_radius=12)
        pygame.draw.rect(pantalla, color_borde_cat, rect_catalogo, width=2, border_radius=12)

        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_flecha_izq, border_radius=6)
        pygame.draw.rect(pantalla, GRIS_MEDIO, btn_flecha_der, border_radius=6)
        txt_f_izq = fuente_menu.render("<", True, BLANCO)
        txt_f_der = fuente_menu.render(">", True, BLANCO)
        pantalla.blit(txt_f_izq, (btn_flecha_izq.centerx - txt_f_izq.get_width() // 2, btn_flecha_izq.centery - txt_f_izq.get_height() // 2))
        pantalla.blit(txt_f_der, (btn_flecha_der.centerx - txt_f_der.get_width() // 2, btn_flecha_der.centery - txt_f_der.get_height() // 2))

        cand_actual = datos_catalogo[indice_catalogo]
        img_cand = comodines_catalogo[indice_catalogo].copy()

        if deshabilitado:
            s_oscuro = pygame.Surface(img_cand.get_size(), pygame.SRCALPHA)
            s_oscuro.fill((0, 0, 0, 150))
            img_cand.blit(s_oscuro, (0, 0))

        pantalla.blit(img_cand, (140, 120))
        pygame.draw.rect(pantalla, GRIS_MEDIO if deshabilitado else BLANCO, (140, 120, 180, 270), 2)

        x_text = 350
        y_text = 120
        espacio = 26

        color_t_tit = TEXTO_DESHABILITADO if deshabilitado else NARANJA_MARTE
        color_t_val = TEXTO_DESHABILITADO if deshabilitado else BLANCO
        color_t_ocu = TEXTO_DESHABILITADO if deshabilitado else AZUL_UI
        color_t_buff = TEXTO_DESHABILITADO if deshabilitado else VERDE_OK
        color_t_nerf = TEXTO_DESHABILITADO if deshabilitado else ROJO_ALERTA

        pantalla.blit(fuente_ficha_bold.render("NOMBRE:", True, color_t_tit), (x_text, y_text))
        pantalla.blit(fuente_ficha.render(cand_actual["nombre"], True, color_t_val), (x_text + 85, y_text))

        pantalla.blit(fuente_ficha_bold.render("EDAD:", True, color_t_tit), (x_text, y_text + espacio))
        pantalla.blit(fuente_ficha.render(cand_actual["edad"], True, color_t_val), (x_text + 65, y_text + espacio))

        pantalla.blit(fuente_ficha_bold.render("GÉNERO:", True, color_t_tit), (x_text, y_text + espacio * 2))
        pantalla.blit(fuente_ficha.render(cand_actual["genero"], True, color_t_val), (x_text + 85, y_text + espacio * 2))

        pantalla.blit(fuente_ficha_bold.render("GUSTOS:", True, color_t_tit), (x_text, y_text + espacio * 3))
        pantalla.blit(fuente_ficha.render(cand_actual["gustos"], True, color_t_val), (x_text + 85, y_text + espacio * 3))

        pygame.draw.line(pantalla, GRIS_MEDIO, (x_text, y_text + espacio * 4 + 5), (x_text + 410, y_text + espacio * 4 + 5), 1)

        pantalla.blit(fuente_ficha_bold.render("OCUPACIÓN:", True, color_t_ocu), (x_text, y_text + espacio * 5))
        pantalla.blit(fuente_ficha_bold.render(cand_actual["ocupacion"], True, color_t_val), (x_text + 110, y_text + espacio * 5))

        pantalla.blit(fuente_ficha_bold.render("VENTAJA:", True, color_t_buff), (x_text, y_text + espacio * 6 + 5))
        pantalla.blit(fuente_ficha.render(cand_actual["buff"], True, color_t_buff), (x_text + 85, y_text + espacio * 6 + 5))

        pantalla.blit(fuente_ficha_bold.render("DESVENTAJA:", True, color_t_nerf), (x_text, y_text + espacio * 7 + 10))
        pantalla.blit(fuente_ficha.render(cand_actual["nerf"], True, color_t_nerf), (x_text + 115, y_text + espacio * 7 + 10))

        txt_pag = fuente_hud.render(f"Candidato {indice_catalogo + 1} / {len(datos_catalogo)}", True, color_t_val)
        pantalla.blit(txt_pag, (180, 410))

        if esta_elegido:
            color_btn_sel = ROJO_ALERTA
            texto_btn_sel = "Quitar de Misión"
        elif deshabilitado:
            color_btn_sel = GRIS_DESHABILITADO
            texto_btn_sel = "Límite alcanzado (Max 2)"
        else:
            color_btn_sel = AZUL_UI
            texto_btn_sel = "Añadir a Misión"

        pygame.draw.rect(pantalla, color_btn_sel, btn_seleccionar_comodin, border_radius=8)
        t_sel = fuente_hud.render(texto_btn_sel, True, TEXTO_DESHABILITADO if deshabilitado else BLANCO)
        pantalla.blit(t_sel, (btn_seleccionar_comodin.centerx - t_sel.get_width() // 2, btn_seleccionar_comodin.centery - t_sel.get_height() // 2))

        color_btn_conf = VERDE_OK if len(comodines_elegidos) > 0 else GRIS_MEDIO
        pygame.draw.rect(pantalla, color_btn_conf, btn_confirmar_mision, border_radius=8)
        t_conf = fuente_menu.render("Iniciar Misión", True, BLANCO)
        pantalla.blit(t_conf, (btn_confirmar_mision.centerx - t_conf.get_width() // 2, btn_confirmar_mision.centery - t_conf.get_height() // 2))

    elif estado_juego == "JUGANDO":
        modulo_visual = 3 if modulo_actual == MODULO_AIRLOCK_LEGACY else modulo_actual
        mod_info = modulos[modulo_visual]
        pantalla.blit(fondos_modulos[modulo_visual], (0, 0))
        for imagen_overlay in overlays_modulos.get(modulo_visual, []):
            if imagen_overlay is not None:
                pantalla.blit(imagen_overlay, (0, 0))

        mx, my = pygame.mouse.get_pos()
        for hs in mod_info.get("hotspots", []):
            r = hs["rect"]
            esta_encima = r.collidepoint(mx, my)
            es_objetivo_seleccionado = (
                mision_tutorial_seleccionada in misiones_del_dia
                and mision_tutorial_seleccionada["modulo_id"] == modulo_actual
                and not mision_tutorial_seleccionada["completada"]
                and hs.get("mision") == mision_tutorial_seleccionada["nombre"]
            )
            if es_objetivo_seleccionado:
                pulso = (math.sin(pygame.time.get_ticks() / 135.0) + 1.0) / 2.0
                radio = 15 + int(8 * pulso)
                pygame.draw.circle(pantalla, (255, 166, 35), r.center, radio + 5, width=3)
                pygame.draw.circle(pantalla, AMARILLO, r.center, radio, width=4)
                pygame.draw.circle(pantalla, (255, 248, 190), r.center, 7, width=2)
                etiqueta_objetivo = fuente_ficha_bold.render("MISIÓN", True, AMARILLO)
                pantalla.blit(etiqueta_objetivo, (r.centerx - etiqueta_objetivo.get_width() // 2, r.centery + radio + 7))
            elif esta_encima:
                pygame.draw.circle(pantalla, VERDE_BRILLANTE, r.center, 11, width=2)
                texto_hover = fuente_ficha_bold.render(f"Tocar: {hs['etiqueta']}", True, BLANCO)
                caja_hover = pygame.Rect(mx + 14, my + 12, texto_hover.get_width() + 16, texto_hover.get_height() + 12)
                if caja_hover.right > ANCHO - 8:
                    caja_hover.right = mx - 14
                if caja_hover.bottom > ALTO - 65:
                    caja_hover.bottom = my - 12
                pygame.draw.rect(pantalla, (10, 14, 23), caja_hover, border_radius=6)
                pygame.draw.rect(pantalla, AZUL_UI, caja_hover, width=1, border_radius=6)
                pantalla.blit(texto_hover, (caja_hover.x + 8, caja_hover.y + 6))

        cid = mod_info["comodin_id"]
        pos_comp = mod_info["pos_comodin"]
        if cid is not None and cid in comodines_elegidos and pos_comp is not None:
            px, py = pos_comp
            pantalla.blit(comodines_modulo[cid], (px, py))
            pygame.draw.rect(pantalla, VERDE_OK, (px, py, 120, 180), width=2, border_radius=6)

        # HUD OVERLAY SUPERIOR
        superficie_hud = pygame.Surface((ANCHO, 85), pygame.SRCALPHA)
        superficie_hud.fill((10, 14, 23, 210))
        pantalla.blit(superficie_hud, (0, 0))

        txt_titulo = fuente_titulo.render("M.A.R.S.", True, NARANJA_MARTE)
        pantalla.blit(txt_titulo, (20, 10))

        minutos = int(tiempo_dia) // 60
        segundos = int(tiempo_dia) % 60
        txt_tiempo = fuente_hud.render(f"Día {dia_actual}/14 - Tiempo: {minutos:02d}:{segundos:02d}", True, BLANCO)
        pantalla.blit(txt_tiempo, (20, 45))

        col_o2 = VERDE_OK if oxigeno_congelado or oxigeno > 30 else ROJO_ALERTA
        pygame.draw.rect(pantalla, (50, 50, 50), (220, 48, 80, 14))
        pygame.draw.rect(pantalla, col_o2, (220, 48, int(0.8 * oxigeno), 14))
        pantalla.blit(fuente_hud.render("O2: OK" if oxigeno_congelado else f"O2: {int(oxigeno)}%", True, BLANCO), (220, 28))

        col_com = VERDE_OK if comida_congelado or comida > 30 else ROJO_ALERTA
        pygame.draw.rect(pantalla, (50, 50, 50), (330, 48, 80, 14))
        pygame.draw.rect(pantalla, col_com, (330, 48, int(0.8 * comida), 14))
        pantalla.blit(fuente_hud.render("Alim: OK" if comida_congelado else f"Alim: {int(comida)}%", True, BLANCO), (330, 28))

        col_rad = VERDE_OK if radiacion_congelado or radiacion > 30 else ROJO_ALERTA
        pygame.draw.rect(pantalla, (50, 50, 50), (440, 48, 80, 14))
        pygame.draw.rect(pantalla, col_rad, (440, 48, int(0.8 * radiacion), 14))
        pantalla.blit(fuente_hud.render("Rad: OK" if radiacion_congelado else f"Rad: {int(radiacion)}%", True, BLANCO), (440, 28))

        pygame.draw.rect(pantalla, NARANJA_MARTE if not panel_misiones_abierto else AZUL_UI, btn_lengueta, border_radius=6)
        txt_leng = fuente_hud.render("Misiones (9) ▼" if not panel_misiones_abierto else "Cerrar ▲", True, BLANCO)
        pantalla.blit(txt_leng, (btn_lengueta.centerx - txt_leng.get_width() // 2, btn_lengueta.centery - txt_leng.get_height() // 2))

        pygame.draw.rect(pantalla, (28, 72, 104), btn_jj, border_radius=9)
        pygame.draw.rect(pantalla, (125, 205, 255), btn_jj, width=2, border_radius=9)
        txt_jj = fuente_ficha_bold.render("JJ", True, BLANCO)
        pantalla.blit(txt_jj, (btn_jj.centerx - txt_jj.get_width() // 2, btn_jj.centery - txt_jj.get_height() // 2))

        if panel_misiones_abierto:
            rect_panel = pygame.Rect(ANCHO - 340, 50, 330, 480)
            s_p = pygame.Surface((330, 480), pygame.SRCALPHA)
            s_p.fill((10, 14, 23, 235))
            pantalla.blit(s_p, (ANCHO - 340, 50))
            pygame.draw.rect(pantalla, AZUL_UI, rect_panel, width=2, border_radius=8)

            txt_tit_p = fuente_ficha_bold.render(f"TAREAS DÍA {dia_actual} · Fallos {dias_ignorados_acumulados}/4", True, NARANJA_MARTE)
            pantalla.blit(txt_tit_p, (ANCHO - 325, 60))

            y_box = 95
            for m in misiones_del_dia:
                btn_mision = pygame.Rect(ANCHO - 330, y_box, 310, 40)
                col_btn_bg = VERDE_OK if m["completada"] else (ROJO_ALERTA if m["tipo"] == "URGENCIA" else GRIS_MEDIO)
                pygame.draw.rect(pantalla, col_btn_bg, btn_mision, border_radius=6)
                pygame.draw.rect(pantalla, BLANCO, btn_mision, width=1, border_radius=6)

                prefix = "✓ " if m["completada"] else ("! " if m["tipo"] == "URGENCIA" else "• ")
                nombre_mision_ui = f"{prefix}Extra: {m['nombre']}" if m.get("extra_geologo") else f"{prefix}{m['nombre']}"
                txt_m_item = fuente_ficha_bold.render(nombre_mision_ui, True, BLANCO)
                pantalla.blit(txt_m_item, (ANCHO - 320, y_box + 4))

                txt_m_sub = fuente_ficha.render(m['desc'], True, BLANCO if m["completada"] else TEXTO_DESHABILITADO)
                pantalla.blit(txt_m_sub, (ANCHO - 320, y_box + 20))
                y_box += 44

        s_nav = pygame.Surface((ANCHO, 60), pygame.SRCALPHA)
        s_nav.fill((10, 14, 23, 210))
        pantalla.blit(s_nav, (0, ALTO - 60))

        instruccion_nav = "Haz CLIC sobre los equipos del fondo para interactuar"
        txt_nav = fuente_hud.render(f"< [A] | Módulo: {mod_info['nombre']} | [D] >  | {instruccion_nav}", True, AZUL_UI)
        pantalla.blit(txt_nav, (20, ALTO - 50))

        if mencion_interaccion:
            txt_msg = fuente_hud.render(mencion_interaccion, True, VERDE_OK if creditos > 0 else ROJO_ALERTA)
            pantalla.blit(txt_msg, (20, ALTO - 25))

        # --- RECUADRO DE DIÁLOGO DEL TUTORIAL (MANDO SUPERIOR) ---
        if dia_actual == 1 and tutorial_activo:
            s_tut = pygame.Surface((ANCHO - 40, 120), pygame.SRCALPHA)
            s_tut.fill((10, 14, 23, 245))
            pantalla.blit(s_tut, (20, ALTO - 135))
            pygame.draw.rect(pantalla, DORADO_MANDO, (20, ALTO - 135, ANCHO - 40, 120), width=2, border_radius=8)
            pista_salto = fuente_hud.render("Mantén ESPACIO 5 s para saltar el tutorial", True, BLANCO)
            pantalla.blit(pista_salto, (35, ALTO - 155))
            pygame.draw.rect(pantalla, GRIS_MEDIO, (ANCHO - 250, ALTO - 155, 210, 8), border_radius=4)
            pygame.draw.rect(pantalla, VERDE_BRILLANTE, (ANCHO - 250, ALTO - 155, int(210 * min(1.0, tiempo_espacio_tutorial / PROGRESO_SALTO_TUTORIAL)), 8), border_radius=4)

            msg_completo = dialogos_tutorial_actuales()[paso_tutorial] if tutorial_fase == "dialogos" else mensajes_tutorial_actuales()[tutorial_fase]
            if not ayuda_jj_abierta and tutorial_fase in ("dialogos", "explicar_urgente", "explicar_secundaria", "final") and texto_tutorial_indice < len(msg_completo):
                texto_tutorial_indice += VELOCIDAD_TEXTO * dt
                if texto_tutorial_indice > len(msg_completo):
                    texto_tutorial_indice = float(len(msg_completo))

            msg_a_mostrar = msg_completo[:int(texto_tutorial_indice)]
            lineas_tut = obtener_lineas_texto(msg_a_mostrar, fuente_robotica, ANCHO - 80)

            y_t = ALTO - 125
            etiqueta_personaje = msg_completo.split("]:", 1)[0].lstrip("[")
            personaje_actual = next((p for p in datos_catalogo if p["nombre"].upper() == etiqueta_personaje), None)
            color_dialogo = (125, 205, 255) if personaje_actual and personaje_actual["genero"] == "M" else (255, 190, 220)
            for l_t in lineas_tut:
                t_r = fuente_robotica.render(l_t, True, color_dialogo)
                pantalla.blit(t_r, (35, y_t))
                y_t += 24

            if tutorial_fase in ("dialogos", "explicar_urgente", "explicar_secundaria", "final"):
                pygame.draw.rect(pantalla, AZUL_UI, btn_siguiente_tutorial, border_radius=6)
                pygame.draw.rect(pantalla, BLANCO, btn_siguiente_tutorial, width=1, border_radius=6)
                lbl_tut = "Siguiente" if int(texto_tutorial_indice) >= len(msg_completo) else "Saltar texto"
                t_btn_t = fuente_hud.render(lbl_tut, True, BLANCO)
                pantalla.blit(t_btn_t, (btn_siguiente_tutorial.centerx - t_btn_t.get_width() // 2, btn_siguiente_tutorial.centery - t_btn_t.get_height() // 2))

        if ayuda_jj_abierta:
            velo_ayuda = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            velo_ayuda.fill((4, 8, 16, 190))
            pantalla.blit(velo_ayuda, (0, 0))
            panel_ayuda = pygame.Rect(ANCHO // 2 - 230, 125, 460, 385)
            pygame.draw.rect(pantalla, GRIS_OSCURO, panel_ayuda, border_radius=12)
            pygame.draw.rect(pantalla, AZUL_UI, panel_ayuda, width=3, border_radius=12)
            titulo_ayuda = fuente_titulo.render("Crew · Quick Help", True, NARANJA_MARTE)
            pantalla.blit(titulo_ayuda, (panel_ayuda.x + 22, panel_ayuda.y + 18))
            pygame.draw.rect(pantalla, GRIS_MEDIO, btn_cerrar_ayuda_jj, border_radius=7)
            pygame.draw.rect(pantalla, BLANCO, btn_cerrar_ayuda_jj, width=1, border_radius=7)
            cerrar_txt = fuente_ficha_bold.render("X", True, BLANCO)
            pantalla.blit(cerrar_txt, (btn_cerrar_ayuda_jj.centerx - cerrar_txt.get_width() // 2, btn_cerrar_ayuda_jj.centery - cerrar_txt.get_height() // 2))

            consejos_base = [
                ("[NAME] Indicators", "Oxígeno, comida y radiación aparecen arriba. Durante el tutorial no bajan; en el día 1 no caen de 30%. Desde el día 2 consumen con normalidad."),
                ("[NAME] Missions", "Abre Misiones. Completa primero las urgentes rojas y después las secundarias grises. El tiempo sigue corriendo mientras trabajas."),
                ("[NAME] Objects and rooms", "Pasa el cursor por el equipo y toca el círculo para iniciar su minijuego. Usa A/D o las flechas para cambiar de sala; desde Exterior también puedes tocar los módulos."),
                ("[NAME] Need a break?", "Pulsa ESC para pausar y guardar. Si una barra llega a cero, la misión termina; cuatro días seguidos sin completar las tareas provocan el regreso a casa.")
            ]
            equipo_ayuda = astronautas_tutorial()
            consejos_jj = [
                (etiqueta.replace("[NAME]", f"[{equipo_ayuda[i % len(equipo_ayuda)]['nombre'].upper()}]"), texto)
                for i, (etiqueta, texto) in enumerate(consejos_base)
            ]
            y_consejo = panel_ayuda.y + 72
            for encabezado, detalle in consejos_jj:
                pantalla.blit(fuente_ficha_bold.render(encabezado, True, (125, 205, 255)), (panel_ayuda.x + 24, y_consejo))
                y_consejo += 23
                for linea in obtener_lineas_texto(detalle, fuente_ficha, panel_ayuda.width - 48):
                    pantalla.blit(fuente_ficha.render(linea, True, BLANCO), (panel_ayuda.x + 24, y_consejo))
                    y_consejo += 19
                y_consejo += 8

    elif estado_juego == "MINIJUEGO":
        s_bg = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        s_bg.fill((10, 14, 23, 240))
        pantalla.blit(s_bg, (0, 0))

        nom_mod = modulos[modulo_minijuego_activo]['nombre']
        txt_m = fuente_titulo.render(f"Minijuego [{nom_mod}]: {mision_en_curso['nombre']}", True, NARANJA_MARTE)
        pantalla.blit(txt_m, (ANCHO // 2 - txt_m.get_width() // 2, 45))
        if dia_actual == 1 and tutorial_activo:
            pista_salto = fuente_hud.render("Mantén ESPACIO 5 s para saltar el tutorial", True, BLANCO)
            pantalla.blit(pista_salto, (ANCHO // 2 - pista_salto.get_width() // 2, 78))
            pygame.draw.rect(pantalla, GRIS_MEDIO, (ANCHO // 2 - 105, 100, 210, 8), border_radius=4)
            pygame.draw.rect(pantalla, VERDE_BRILLANTE, (ANCHO // 2 - 105, 100, int(210 * min(1.0, tiempo_espacio_tutorial / PROGRESO_SALTO_TUTORIAL)), 8), border_radius=4)

        rect_juego = pygame.Rect(ANCHO // 2 - 220, ALTO // 2 - 120, 440, 260)
        pygame.draw.rect(pantalla, GRIS_OSCURO, rect_juego, border_radius=12)
        pygame.draw.rect(pantalla, AZUL_UI, rect_juego, width=3, border_radius=12)

        if modulo_minijuego_activo == 0:
            if id_minijuego == 1:
                txt_t = fuente_titulo.render(f"Temperatura: {temp_actual:.1f} °C", True, VERDE_OK if 20.0 <= temp_actual <= 22.0 else ROJO_ALERTA)
                pantalla.blit(txt_t, (ANCHO // 2 - txt_t.get_width() // 2, ALTO // 2 - 80))

                txt_target = fuente_hud.render("Objetivo: Equilibrar exactamente en 21.0 °C", True, BLANCO)
                pantalla.blit(txt_target, (ANCHO // 2 - txt_target.get_width() // 2, ALTO // 2 - 30))

                pygame.draw.rect(pantalla, ROJO_ALERTA, btn_calef, border_radius=6)
                pygame.draw.rect(pantalla, AZUL_UI, btn_aire, border_radius=6)
                pantalla.blit(fuente_hud.render("+ Calefacción", True, BLANCO), (btn_calef.x + 10, btn_calef.y + 10))
                pantalla.blit(fuente_hud.render("- Aire Acond.", True, BLANCO), (btn_aire.x + 10, btn_aire.y + 10))

            elif id_minijuego == 2:
                txt_i = fuente_hud.render("Sincroniza el Circadiano: Activa los botones 1 y 3", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                for idx, r_luz in enumerate(luces_rects):
                    col = VERDE_OK if luces_estado[idx] else GRIS_MEDIO
                    pygame.draw.rect(pantalla, col, r_luz, border_radius=8)
                    pygame.draw.rect(pantalla, BLANCO, r_luz, width=2, border_radius=8)
                    t_n = fuente_menu.render(str(idx + 1), True, BLANCO)
                    pantalla.blit(t_n, (r_luz.centerx - t_n.get_width() // 2, r_luz.centery - t_n.get_height() // 2))

            elif id_minijuego == 3:
                txt_i = fuente_hud.render(f"Haz Clic sobre las manchas ({len(manchas_polvo)} restantes)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                for m_polvo in manchas_polvo:
                    pygame.draw.ellipse(pantalla, NARANJA_MARTE, m_polvo)

            elif id_minijuego == 4:
                txt_i = fuente_hud.render("Arrastra cada Ración a su contenedor por Color", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 100))

                for c in cajas_destino:
                    pygame.draw.rect(pantalla, c["col"], c["rect"], width=3, border_radius=8)

                for p in paquetes:
                    pygame.draw.rect(pantalla, p["col"], p["rect"], border_radius=6)

            elif id_minijuego == 5:
                txt_i = fuente_hud.render("Alinea las 3 barras al centro (50%)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 100))

                for idx, eq_r in enumerate(eq_rects):
                    pygame.draw.rect(pantalla, GRIS_MEDIO, eq_r, border_radius=4)
                    y_fill = eq_r.y + int(eq_r.height * (1.0 - eq_niveles[idx] / 100.0))
                    pygame.draw.rect(pantalla, VERDE_OK, (eq_r.x, y_fill, eq_r.width, eq_r.y + eq_r.height - y_fill), border_radius=4)

        elif modulo_minijuego_activo == 1:
            if id_minijuego == 1:
                txt_i = fuente_hud.render("¡Haz CLIC repetido en el botón para presurizar el Tanque O2!", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                pygame.draw.rect(pantalla, (50, 50, 50), (ANCHO // 2 - 140, ALTO // 2 - 30, 280, 25), border_radius=6)
                pygame.draw.rect(pantalla, VERDE_OK, (ANCHO // 2 - 140, ALTO // 2 - 30, int(2.8 * progreso_valvula), 25), border_radius=6)

                pygame.draw.rect(pantalla, AZUL_UI, btn_presionar_valvula, border_radius=8)
                t_v = fuente_menu.render("GIRAR VÁLVULA", True, BLANCO)
                pantalla.blit(t_v, (btn_presionar_valvula.centerx - t_v.get_width() // 2, btn_presionar_valvula.centery - t_v.get_height() // 2))

            elif id_minijuego == 2:
                txt_i = fuente_hud.render("Ajusta N2 a ~78% y O2 a ~21%", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 95))

                pygame.draw.rect(pantalla, GRIS_MEDIO, eq_gas_rects[0], border_radius=4)
                y_n2 = eq_gas_rects[0].y + int(eq_gas_rects[0].height * (1.0 - n2_nivel / 100.0))
                pygame.draw.rect(pantalla, AZUL_UI, (eq_gas_rects[0].x, y_n2, eq_gas_rects[0].width, eq_gas_rects[0].y + eq_gas_rects[0].height - y_n2), border_radius=4)
                pantalla.blit(fuente_hud.render(f"N2: {int(n2_nivel)}%", True, BLANCO), (eq_gas_rects[0].x - 10, eq_gas_rects[0].y + 130))

                pygame.draw.rect(pantalla, GRIS_MEDIO, eq_gas_rects[1], border_radius=4)
                y_o2 = eq_gas_rects[1].y + int(eq_gas_rects[1].height * (1.0 - o2_nivel / 100.0))
                pygame.draw.rect(pantalla, VERDE_OK, (eq_gas_rects[1].x, y_o2, eq_gas_rects[1].width, eq_gas_rects[1].y + eq_gas_rects[1].height - y_o2), border_radius=4)
                pantalla.blit(fuente_hud.render(f"O2: {int(o2_nivel)}%", True, BLANCO), (eq_gas_rects[1].x - 10, eq_gas_rects[1].y + 130))

            elif id_minijuego == 3:
                txt_i = fuente_hud.render("Arrastra y suelta el parche centrado sobre la fuga", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                centro_fuga = fuga_rect.center
                pulso_fuga = 5 + int((pygame.time.get_ticks() // 180) % 7)
                color_fuga = VERDE_OK if fuga_reparada else ROJO_ALERTA
                pygame.draw.circle(pantalla, color_fuga, centro_fuga, fuga_rect.width // 2 + pulso_fuga, width=3)
                pygame.draw.circle(pantalla, (95, 20, 30) if not fuga_reparada else (20, 100, 65), centro_fuga, fuga_rect.width // 2)
                pygame.draw.circle(pantalla, NEGRO_ESPACIAL, centro_fuga, 18)
                if not fuga_reparada:
                    pygame.draw.circle(pantalla, ROJO_ALERTA, centro_fuga, 8)
                texto_objetivo = fuente_ficha_bold.render("FUGA SELLADA" if fuga_reparada else "ORIFICIO", True, color_fuga)
                pantalla.blit(texto_objetivo, (centro_fuga[0] - texto_objetivo.get_width() // 2, fuga_rect.y - 27))

                pygame.draw.rect(pantalla, VERDE_OK, parche_rect, border_radius=8)
                pygame.draw.rect(pantalla, BLANCO, parche_rect, width=2, border_radius=8)
                texto_parche = fuente_ficha.render("OK" if fuga_reparada else "PARCHE", True, BLANCO)
                pantalla.blit(texto_parche, (parche_rect.centerx - texto_parche.get_width() // 2, parche_rect.centery - texto_parche.get_height() // 2))
                if temporizador_feedback_fuga > 0 and feedback_fuga:
                    texto_feedback = fuente_ficha_bold.render(feedback_fuga, True, VERDE_OK if fuga_reparada else AMARILLO)
                    pantalla.blit(texto_feedback, (ANCHO // 2 - texto_feedback.get_width() // 2, ALTO // 2 + 125))

            elif id_minijuego == 4:
                txt_i = fuente_hud.render("Purga en secuencia: Presiona [1] -> [2] -> [3]", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                for b_dren in botones_drenaje:
                    pygame.draw.rect(pantalla, AZUL_UI, b_dren["rect"], border_radius=8)
                    pygame.draw.rect(pantalla, BLANCO, b_dren["rect"], width=2, border_radius=8)
                    t_n = fuente_menu.render(str(b_dren["val"]), True, BLANCO)
                    pantalla.blit(t_n, (b_dren["rect"].centerx - t_n.get_width() // 2, b_dren["rect"].centery - t_n.get_height() // 2))

            elif id_minijuego == 5:
                txt_i = fuente_hud.render("1. Haz Clic en el Cartucho Usado | 2. Clic en la Ranura", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                if estado_co2 == 0:
                    pygame.draw.rect(pantalla, ROJO_ALERTA, cartucho_saturado, border_radius=6)
                    pantalla.blit(fuente_ficha.render("SATURADO", True, BLANCO), (cartucho_saturado.x - 5, cartucho_saturado.y + 30))

                pygame.draw.rect(pantalla, GRIS_MEDIO, cartucho_ranura, border_radius=6)
                pygame.draw.rect(pantalla, BLANCO, cartucho_ranura, width=2, border_radius=6)

                if estado_co2 == 1:
                    pantalla.blit(fuente_hud.render("¡Ahora haz clic aquí!", True, AMARILLO), (cartucho_ranura.x - 30, cartucho_ranura.y - 30))

        elif modulo_minijuego_activo == 2:
            if id_minijuego == 1:
                txt_i = fuente_hud.render("Haz Clic en un conector de la izq y luego en su mismo color a la der", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                for c_i in cables_izq:
                    pygame.draw.rect(pantalla, c_i["col"], c_i["rect"], border_radius=4)
                for c_d in cables_der:
                    pygame.draw.rect(pantalla, c_d["col"], c_d["rect"], border_radius=4)

                for c_pair in conexiones_hechas:
                    c1 = next(x for x in cables_izq if x["id"] == c_pair[0])
                    c2 = next(x for x in cables_der if x["id"] == c_pair[1])
                    pygame.draw.line(pantalla, c1["col"], c1["rect"].center, c2["rect"].center, 4)

            elif id_minijuego == 2:
                if indice_analisis < len(analisis_muestras):
                    muestra_actual = analisis_muestras[indice_analisis]
                    txt_i = fuente_hud.render("MICROIMAGEN 20×  |  Clasifica por tamaño y morfología", True, BLANCO)
                    pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, 185))
                    txt_paso = fuente_ficha_bold.render(f"MUESTRA {indice_analisis + 1}/{len(analisis_muestras)}   ·   Errores: {errores_analisis}", True, AZUL_UI)
                    pantalla.blit(txt_paso, (ANCHO // 2 - txt_paso.get_width() // 2, 207))

                    marco_pantalla = pygame.Rect(ANCHO // 2 - 150, 228, 300, 175)
                    pygame.draw.rect(pantalla, (20, 34, 48), marco_pantalla, border_radius=8)
                    pygame.draw.rect(pantalla, (70, 160, 180), marco_pantalla, width=2, border_radius=8)
                    rect_micro = pygame.Rect(marco_pantalla.x + 15, marco_pantalla.y + 12, 270, 150)
                    dibujar_microimagen(rect_micro, muestra_actual["clase"], muestra_actual["semilla"])

                    for boton_clase in botones_clasificacion:
                        col_boton = (40, 105, 125) if boton_clase["clase"] == "CRISTAL" else AZUL_UI
                        pygame.draw.rect(pantalla, col_boton, boton_clase["rect"], border_radius=7)
                        pygame.draw.rect(pantalla, (120, 210, 220), boton_clase["rect"], width=2, border_radius=7)
                        etiqueta_clase = fuente_ficha_bold.render(boton_clase["lbl"], True, BLANCO)
                        pantalla.blit(etiqueta_clase, (boton_clase["rect"].centerx - etiqueta_clase.get_width() // 2, boton_clase["rect"].centery - etiqueta_clase.get_height() // 2))
                    if temporizador_feedback_analisis > 0:
                        color_feedback = VERDE_BRILLANTE if "correcta" in feedback_analisis.lower() or "buen" in feedback_analisis.lower() or "identificada" in feedback_analisis.lower() else AMARILLO
                        mensaje_analisis = fuente_hud.render(feedback_analisis, True, color_feedback)
                        pantalla.blit(mensaje_analisis, (ANCHO // 2 - mensaje_analisis.get_width() // 2, 466))
                else:
                    fin_analisis = fuente_titulo.render("¡Muestras clasificadas!", True, VERDE_BRILLANTE)
                    pantalla.blit(fin_analisis, (ANCHO // 2 - fin_analisis.get_width() // 2, ALTO // 2))

            elif id_minijuego == 3:
                txt_i = fuente_hud.render("Arrastra cada muestra de roca a su caja contenedora", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 100))

                for c_r in cajas_rocas:
                    pygame.draw.rect(pantalla, c_r["col"], c_r["rect"], width=3, border_radius=8)
                    t_lbl = fuente_ficha_bold.render(c_r["lbl"], True, c_r["col"])
                    pantalla.blit(t_lbl, (c_r["rect"].centerx - t_lbl.get_width() // 2, c_r["rect"].centery - t_lbl.get_height() // 2))

                for r in rocas:
                    pygame.draw.rect(pantalla, r["col"], r["rect"], border_radius=6)

            elif id_minijuego == 4:
                txt_i = fuente_hud.render("Memoriza y repite la secuencia de colores:", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                str_bio = " - ".join(map(str, secuencia_bio_objetivo))
                txt_seq = fuente_titulo.render(f"SECUENCIA: [ {str_bio} ]", True, AMARILLO)
                pantalla.blit(txt_seq, (ANCHO // 2 - txt_seq.get_width() // 2, ALTO // 2 - 50))

                for b_bio in botones_bio:
                    pygame.draw.rect(pantalla, b_bio["col"], b_bio["rect"], border_radius=8)
                    pygame.draw.rect(pantalla, BLANCO, b_bio["rect"], width=2, border_radius=8)
                    t_val = fuente_menu.render(str(b_bio["val"]), True, BLANCO)
                    pantalla.blit(t_val, (b_bio["rect"].centerx - t_val.get_width() // 2, b_bio["rect"].centery - t_val.get_height() // 2))

            elif id_minijuego == 5:
                txt_i = fuente_hud.render("Ajusta las gotas purificadoras hasta equilibrar el pH en 6.5", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                txt_ph = fuente_titulo.render(f"pH Cultivo: {ph_actual:.1f}", True, VERDE_OK if ph_actual == 6.5 else ROJO_ALERTA)
                pantalla.blit(txt_ph, (ANCHO // 2 - txt_ph.get_width() // 2, ALTO // 2 - 30))

                pygame.draw.rect(pantalla, VERDE_OK, btn_ph_mas, border_radius=6)
                pygame.draw.rect(pantalla, ROJO_ALERTA, btn_ph_menos, border_radius=6)
                pantalla.blit(fuente_hud.render("+ Gotas", True, BLANCO), (btn_ph_mas.x + 15, btn_ph_mas.y + 10))
                pantalla.blit(fuente_hud.render("- Gotas", True, BLANCO), (btn_ph_menos.x + 15, btn_ph_menos.y + 10))

            elif id_minijuego == 6:
                txt_i = fuente_hud.render("Introduce los 3 testigos de suelo en la cámara sellada", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, 185))
                txt_progreso = fuente_ficha_bold.render(f"MUESTRAS PROCESADAS: {progreso_ingesta}/3", True, AZUL_UI)
                pantalla.blit(txt_progreso, (ANCHO // 2 - txt_progreso.get_width() // 2, 208))

                pulso = int(20 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 130.0)))
                color_camara = (70 + pulso, 190 + pulso // 2, 205 + pulso // 3) if ingesta_procesando else (75, 155, 180)
                pygame.draw.rect(pantalla, (15, 30, 44), camara_ingesta_rect, border_radius=10)
                pygame.draw.rect(pantalla, color_camara, camara_ingesta_rect, width=4, border_radius=10)
                pygame.draw.rect(pantalla, (44, 68, 82), (camara_ingesta_rect.x + 14, camara_ingesta_rect.y + 18, camara_ingesta_rect.width - 28, camara_ingesta_rect.height - 36), border_radius=6)
                pygame.draw.rect(pantalla, (145, 200, 210), (camara_ingesta_rect.x + 14, camara_ingesta_rect.y + 18, camara_ingesta_rect.width - 28, camara_ingesta_rect.height - 36), width=2, border_radius=6)
                lbl_camara = fuente_ficha_bold.render("CÁMARA SELLADA", True, BLANCO)
                pantalla.blit(lbl_camara, (camara_ingesta_rect.centerx - lbl_camara.get_width() // 2, camara_ingesta_rect.y + 4))

                # Brazo robótico y pinza articulada.
                pygame.draw.line(pantalla, (180, 196, 204), (camara_ingesta_rect.x - 42, camara_ingesta_rect.y - 5), (camara_ingesta_rect.x + 14, camara_ingesta_rect.y + 30), 10)
                pygame.draw.circle(pantalla, (225, 190, 95), (camara_ingesta_rect.x + 15, camara_ingesta_rect.y + 30), 8)
                pygame.draw.line(pantalla, (205, 215, 220), (camara_ingesta_rect.x + 15, camara_ingesta_rect.y + 30), (camara_ingesta_rect.x + 35, camara_ingesta_rect.y + 42), 5)

                for muestra in ingesta_muestras:
                    if muestra["procesando"]:
                        continue
                    rect_muestra = muestra["rect"]
                    pygame.draw.rect(pantalla, muestra["col"], rect_muestra, border_radius=5)
                    pygame.draw.rect(pantalla, (225, 215, 190), rect_muestra, width=2, border_radius=5)
                    rng_muestra = random.Random(muestra["semilla"])
                    for _ in range(5):
                        px = rng_muestra.randint(rect_muestra.x + 4, rect_muestra.right - 4)
                        py = rng_muestra.randint(rect_muestra.y + 4, rect_muestra.bottom - 4)
                        pygame.draw.circle(pantalla, (215, 195, 155), (px, py), 2)
                    lbl_muestra = fuente_ficha.render(muestra["tipo"], True, BLANCO)
                    pantalla.blit(lbl_muestra, (rect_muestra.centerx - lbl_muestra.get_width() // 2, rect_muestra.bottom + 4))

                if ingesta_procesando:
                    pygame.draw.circle(pantalla, VERDE_BRILLANTE, camara_ingesta_rect.center, 12 + int(8 * (temporizador_ingesta / 0.7)), width=2)
                if temporizador_feedback_ingesta > 0:
                    color_feedback = VERDE_BRILLANTE if "procesada" in feedback_ingesta.lower() or "sellada" in feedback_ingesta.lower() else AMARILLO
                    txt_feedback = fuente_hud.render(feedback_ingesta, True, color_feedback)
                    pantalla.blit(txt_feedback, (ANCHO // 2 - txt_feedback.get_width() // 2, 465))

        elif modulo_minijuego_activo == 3:
            if id_minijuego == 1:
                txt_i = fuente_hud.render("Mueve la Garra con los botones hasta encajar en el marco", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                pygame.draw.rect(pantalla, VERDE_OK, puerto_target, width=3, border_radius=6)
                pygame.draw.rect(pantalla, AZUL_UI, (garra_pos[0], garra_pos[1], 50, 50), border_radius=6)

                pygame.draw.rect(pantalla, GRIS_MEDIO, btn_garra_izq, border_radius=4)
                pygame.draw.rect(pantalla, GRIS_MEDIO, btn_garra_der, border_radius=4)
                pygame.draw.rect(pantalla, GRIS_MEDIO, btn_garra_up, border_radius=4)
                pantalla.blit(fuente_hud.render("<", True, BLANCO), (btn_garra_izq.x + 20, btn_garra_izq.y + 10))
                pantalla.blit(fuente_hud.render(">", True, BLANCO), (btn_garra_der.x + 20, btn_garra_der.y + 10))
                pantalla.blit(fuente_hud.render("^", True, BLANCO), (btn_garra_up.x + 20, btn_garra_up.y + 10))

            elif id_minijuego == 2:
                txt_i = fuente_hud.render("Presiona el botón de Carga hasta llegar al 100%", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                pygame.draw.rect(pantalla, (50, 50, 50), (ANCHO // 2 - 140, ALTO // 2 - 30, 280, 25), border_radius=6)
                pygame.draw.rect(pantalla, VERDE_OK, (ANCHO // 2 - 140, ALTO // 2 - 30, int(2.8 * carga_rover), 25), border_radius=6)

                pygame.draw.rect(pantalla, AZUL_UI, btn_cargar_rover, border_radius=8)
                t_v = fuente_menu.render("CARGAR", True, BLANCO)
                pantalla.blit(t_v, (btn_cargar_rover.centerx - t_v.get_width() // 2, btn_cargar_rover.centery - t_v.get_height() // 2))

            elif id_minijuego == 3:
                txt_i = fuente_hud.render("Ajusta la presión de aire a la zona verde (30 a 35 PSI)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                txt_p = fuente_titulo.render(f"Presión: {psi_neumatico:.1f} PSI", True, VERDE_OK if 30.0 <= psi_neumatico <= 35.0 else ROJO_ALERTA)
                pantalla.blit(txt_p, (ANCHO // 2 - txt_p.get_width() // 2, ALTO // 2 - 30))

                pygame.draw.rect(pantalla, VERDE_OK, btn_psi_mas, border_radius=6)
                pygame.draw.rect(pantalla, ROJO_ALERTA, btn_psi_menos, border_radius=6)
                pantalla.blit(fuente_hud.render("+ Inflar", True, BLANCO), (btn_psi_mas.x + 10, btn_psi_mas.y + 10))
                pantalla.blit(fuente_hud.render("- Desinflar", True, BLANCO), (btn_psi_menos.x + 5, btn_psi_menos.y + 10))

            elif id_minijuego == 4:
                txt_i = fuente_hud.render(f"Pasa el escáner sobre las manchas ({len(manchas_uv)} restantes)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                for m_uv in manchas_uv:
                    pygame.draw.ellipse(pantalla, NARANJA_MARTE, m_uv)

            elif id_minijuego == 5:
                txt_i = fuente_hud.render("Arrastra las cajas de minerales al depósito de la base", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 100))

                pygame.draw.rect(pantalla, VERDE_OK, deposito_base, width=3, border_radius=8)
                t_dep = fuente_ficha_bold.render("DEPÓSITO", True, VERDE_OK)
                pantalla.blit(t_dep, (deposito_base.centerx - t_dep.get_width() // 2, deposito_base.centery - t_dep.get_height() // 2))

                for c_rover in cajas_rover:
                    pygame.draw.rect(pantalla, AMARILLO, c_rover["rect"], border_radius=6)

        elif modulo_minijuego_activo == 4:
            if id_minijuego == 1:
                txt_i = fuente_hud.render("Secuencia: [Válvula] -> [Bomba] -> [Puerta]", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                for b_eva in botones_eva:
                    pygame.draw.rect(pantalla, AZUL_UI, b_eva["rect"], border_radius=8)
                    pygame.draw.rect(pantalla, BLANCO, b_eva["rect"], width=2, border_radius=8)
                    t_lbl = fuente_ficha.render(b_eva["lbl"], True, BLANCO)
                    pantalla.blit(t_lbl, (b_eva["rect"].centerx - t_lbl.get_width() // 2, b_eva["rect"].centery - t_lbl.get_height() // 2))

            elif id_minijuego == 2:
                txt_i = fuente_hud.render("Arrastra el Parche Térmico sobre la fisura del traje", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                pygame.draw.ellipse(pantalla, ROJO_ALERTA, fisura_traje)
                pygame.draw.rect(pantalla, VERDE_OK, parche_eva_rect, border_radius=6)
                pantalla.blit(fuente_ficha.render("PARCHE", True, BLANCO), (parche_eva_rect.x + 2, parche_eva_rect.y + 15))

            elif id_minijuego == 3:
                txt_i = fuente_hud.render("Haz Clic en los 3 cierres para dejarlos en VERDE (Bloqueado)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                for idx, r_cierre in enumerate(cierres_rects):
                    col = VERDE_OK if cierres_casco[idx] else ROJO_ALERTA
                    pygame.draw.rect(pantalla, col, r_cierre, border_radius=8)
                    pygame.draw.rect(pantalla, BLANCO, r_cierre, width=2, border_radius=8)
                    t_c = fuente_hud.render("LOCK" if cierres_casco[idx] else "OPEN", True, BLANCO)
                    pantalla.blit(t_c, (r_cierre.centerx - t_c.get_width() // 2, r_cierre.centery - t_c.get_height() // 2))

            elif id_minijuego == 4:
                txt_i = fuente_hud.render("Presiona el botón de Nitrógeno hasta cargar el Jetpack al 100%", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                pygame.draw.rect(pantalla, (50, 50, 50), (ANCHO // 2 - 140, ALTO // 2 - 30, 280, 25), border_radius=6)
                pygame.draw.rect(pantalla, VERDE_OK, (ANCHO // 2 - 140, ALTO // 2 - 30, int(2.8 * carga_jetpack), 25), border_radius=6)

                pygame.draw.rect(pantalla, AZUL_UI, btn_cargar_jetpack, border_radius=8)
                t_v = fuente_menu.render("INYECTAR N2", True, BLANCO)
                pantalla.blit(t_v, (btn_cargar_jetpack.centerx - t_v.get_width() // 2, btn_cargar_jetpack.centery - t_v.get_height() // 2))

            elif id_minijuego == 5:
                txt_i = fuente_hud.render("Arrastra el Mosquetón de acero a la Guía de Seguridad", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 100))

                pygame.draw.rect(pantalla, VERDE_OK, guia_seguridad, width=3, border_radius=8)
                t_g = fuente_ficha_bold.render("GUÍA EVA", True, VERDE_OK)
                pantalla.blit(t_g, (guia_seguridad.centerx - t_g.get_width() // 2, guia_seguridad.centery - t_g.get_height() // 2))

                pygame.draw.rect(pantalla, AMARILLO, mosqueton_rect, border_radius=6)
                pantalla.blit(fuente_ficha.render("HOOK", True, NEGRO_ESPACIAL), (mosqueton_rect.x + 5, mosqueton_rect.y + 15))

        elif modulo_minijuego_activo == 5:
            if id_minijuego == 1:
                txt_i = fuente_hud.render("Ajusta el nivel de blindaje electromagnético a la zona verde (70-80%)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                txt_e = fuente_titulo.render(f"Protección: {nivel_escudo_rad:.1f}%", True, VERDE_OK if 70.0 <= nivel_escudo_rad <= 80.0 else ROJO_ALERTA)
                pantalla.blit(txt_e, (ANCHO // 2 - txt_e.get_width() // 2, ALTO // 2 - 40))

                rect_slider = pygame.Rect(ANCHO // 2 - 120, ALTO // 2 + 30, 240, 20)
                pygame.draw.rect(pantalla, GRIS_MEDIO, rect_slider, border_radius=6)
                pygame.draw.circle(pantalla, VERDE_OK, (rect_slider.x + int((nivel_escudo_rad / 100.0) * rect_slider.width), rect_slider.centery), 12)

            elif id_minijuego == 2:
                txt_i = fuente_hud.render("Sintoniza la frecuencia de la antena exactamente en 95.0 MHz", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                txt_f = fuente_titulo.render(f"Frecuencia: {frecuencia_antena:.1f} MHz", True, VERDE_OK if frecuencia_antena == 95.0 else ROJO_ALERTA)
                pantalla.blit(txt_f, (ANCHO // 2 - txt_f.get_width() // 2, ALTO // 2 - 30))

                pygame.draw.rect(pantalla, VERDE_OK, btn_freq_mas, border_radius=6)
                pygame.draw.rect(pantalla, ROJO_ALERTA, btn_freq_menos, border_radius=6)
                pantalla.blit(fuente_hud.render("+ Freq", True, BLANCO), (btn_freq_mas.x + 15, btn_freq_mas.y + 10))
                pantalla.blit(fuente_hud.render("- Freq", True, BLANCO), (btn_freq_menos.x + 15, btn_freq_menos.y + 10))

            elif id_minijuego == 3:
                txt_i = fuente_hud.render("Presiona repetidamente el freno magnético para estabilizar las paletas", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                pygame.draw.rect(pantalla, (50, 50, 50), (ANCHO // 2 - 140, ALTO // 2 - 30, 280, 25), border_radius=6)
                pygame.draw.rect(pantalla, VERDE_OK, (ANCHO // 2 - 140, ALTO // 2 - 30, int(2.8 * freno_viento), 25), border_radius=6)

                pygame.draw.rect(pantalla, AZUL_UI, btn_freno_viento, border_radius=8)
                t_v = fuente_menu.render("FRENAR", True, BLANCO)
                pantalla.blit(t_v, (btn_freno_viento.centerx - t_v.get_width() // 2, btn_freno_viento.centery - t_v.get_height() // 2))

            elif id_minijuego == 4:
                txt_i = fuente_hud.render(f"Limpia el polvo marciano de los sensores solar ({len(polvo_sensores)} restantes)", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 90))

                for p_sens in polvo_sensores:
                    pygame.draw.ellipse(pantalla, NARANJA_MARTE, p_sens)

            elif id_minijuego == 5:
                txt_i = fuente_hud.render("Sincroniza la medición barométrica: Presiona [1] -> [2] -> [3]", True, BLANCO)
                pantalla.blit(txt_i, (ANCHO // 2 - txt_i.get_width() // 2, ALTO // 2 - 80))

                for b_press in botones_press:
                    pygame.draw.rect(pantalla, AZUL_UI, b_press["rect"], border_radius=8)
                    pygame.draw.rect(pantalla, BLANCO, b_press["rect"], width=2, border_radius=8)
                    t_n = fuente_menu.render(str(b_press["val"]), True, BLANCO)
                    pantalla.blit(t_n, (b_press["rect"].centerx - t_n.get_width() // 2, b_press["rect"].centery - t_n.get_height() // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
