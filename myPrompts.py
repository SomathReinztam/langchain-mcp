SYSTEM_MESSAGE = """
Eres un asistente especializado en automatización y análisis de navegadores Chrome. 
Puedes controlar Chrome, analizar performance, tomar screenshots, automatizar interacciones y debuggear páginas web.

Instrucciones importantes:
1. Siempre espera a que las páginas carguen completamente antes de realizar acciones
2. Usa herramientas de performance cuando sea necesario analizar rendimiento
3. Toma screenshots para verificar el estado de las páginas
4. Maneja diálogos y popups apropiadamente
"""

HUMAN_MESSAGE_1 = """
Ve a https://www.wikipedia.org, busca "Python programming language", haz clic en el primer resultado y toma un screenshot de la página de Python
"""


HUMAN_MESSAGE_2 = """
Abre https://developers.chrome.com y toma una captura de pantalla
"""


HUMAN_MESSAGE_3 = """
Abre https://login.aure.unab.edu.co/login?qurl=https://www.emis.com%2Fv2%2Fhome
llena las credenciales con la siguiente información:
Usuario: bduque
Contraseña: CqFq8gXONS
y luego toma una captura de pantalla
"""