from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Configuración ---
URL_BASE = 'http://127.0.0.1:5500/front/'
URL_LOGIN = URL_BASE + 'index.html'
URL_MENU = URL_BASE + 'menu.html'
URL_BUSQUEDA = URL_BASE + 'busqueda.html'
USUARIO = 'usuario_prueba'
CONTRASENA = 'clave123'
DNI_BUSQUEDA = '11223344'  # Otro DNI de prueba
TIEMPO_ESPERA_PANTALLA = 1  # Segundos a esperar entre cada acción/pantalla

# --- Inicializar el navegador ---
driver = webdriver.Chrome()  # Asegúrate de tener ChromeDriver instalado y en tu PATH

try:
    # --- Paso 1: Login ---
    driver.get(URL_LOGIN)
    print(f"Abriendo página de login... (Esperando {TIEMPO_ESPERA_PANTALLA} segundos)")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    usuario_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'usuario'))
    )
    contrasena_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'contrasena'))
    )
    boton_ingresar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Ingresar")]'))
    )

    usuario_input.send_keys(USUARIO)
    contrasena_input.send_keys(CONTRASENA)
    boton_ingresar.click()
    print(f"Realizando login (simulado por envío de formulario)... (Esperando {TIEMPO_ESPERA_PANTALLA} segundos)")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    # Esperar a ser redirigido a la página del menú
    WebDriverWait(driver, 10).until(
        EC.url_contains('menu.html')
    )
    print(f"Navegando al menú... (Esperando {TIEMPO_ESPERA_PANTALLA} segundos)")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    # --- Paso 2: Navegación y Selección del Formulario de Búsqueda ---
    menu_extras_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//nav//a[contains(text(), "Opciones Extras")]'))
    )
    menu_extras_link.click()
    print(f"Abriendo menú desplegable... (Esperando {TIEMPO_ESPERA_PANTALLA} segundos)")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    # Esperar a que el menú desplegable sea visible
    dropdown_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//nav//ul[@class="dropdown-content"]'))
    )
    print("Menú desplegable visible.")

    # Intentar encontrar y hacer clic en la primera opción
    primera_opcion = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//nav//ul[@class="dropdown-content"]//a[contains(text(), "Primera Opción Desplegable")]'))
    )
    primera_opcion.click()
    print(f"Seleccionando la primera opción del desplegable... (Esperando {TIEMPO_ESPERA_PANTALLA} segundos)")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    # --- Paso 3: Ingresar DNI y Buscar Ofertas ---
    dni_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'dni'))
    )
    boton_buscar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//form[@id="busquedaDNI"]//button[text()="Buscar Ofertas"]'))
    )

    dni_input.send_keys(DNI_BUSQUEDA)
    print(f"Ingresando DNI: {DNI_BUSQUEDA}")
    boton_buscar.click()
    print(f"Haciendo clic en 'Buscar Ofertas'... (Esperando {TIEMPO_ESPERA_PANTALLA} segundos)")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    # Esperar a que la sección de resultados de ofertas sea visible
    resultados_div = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'resultados'))
    )
    print("Sección de resultados visible. Esperando a que aparezca la oferta...")

    # Esperar a que AL MENOS UN botón de actualizar estado sea clickable dentro de los resultados
    boton_actualizar = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@id="resultados"]//button[@class="actualizar-estado"]'))
    )
    print("Botón 'Actualizar Estado' encontrado y clickable.")

    # Hacer clic en el botón para actualizar el estado
    boton_actualizar.click()
    print("Haciendo clic en 'Actualizar Estado'.")
    time.sleep(TIEMPO_ESPERA_PANTALLA)

    # Obtener el elemento del estado y verificar que el texto sea "Finalizado"
    estado_elemento = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="resultados"]//span[contains(@class, "estado")]'))
    )
    print(f"Estado actual: {estado_elemento.text}")
    assert estado_elemento.text == 'Finalizado'
    print("Estado actualizado correctamente a: Finalizado")

except Exception as e:
    import traceback
    print(f"Ocurrió un error: {e}")
    traceback.print_exc()

finally:
    driver.quit()
    print("Navegador cerrado.")