import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import time
import threading
from PIL import Image, ImageTk

# Función para obtener los puertos COM disponibles
def obtener_puertos_com():
    return [port.device for port in serial.tools.list_ports.comports()]

# Variables globales
ser = None
puertos_disponibles = obtener_puertos_com()
puerto_seleccionado = None  # Se definirá más adelante
baudrate_seleccionado = None  # Se definirá más adelante

# Abre la conexión serial
def abrir_conexion_serial():
    global ser
    if puerto_seleccionado.get() and baudrate_seleccionado.get():
        imagen_led.config(image=led_verde)
        ser = serial.Serial(puerto_seleccionado.get(), int(baudrate_seleccionado.get()))
        time.sleep(2)  # Espera a que se establezca la conexión
        ser.write(f"{baudrate_seleccionado.get()}\n".encode())  # Envía el baud rate al Arduino

# Variables globales para los widgets
intensidad_spinbox = None
btn_set_intensidad = None
valor_num = None
btn_set_num = None
etiqueta_resultado = None
etiqueta_pot = None

# Función para leer del puerto serial
def leer_pot():
    while True:
        if ser and ser.in_waiting > 0:  # Si hay datos disponibles para leer
            valor_pot = ser.readline().decode('utf-8').strip()
            print(f"Valor leído del potenciómetro: {valor_pot}")  # Depuración
            if etiqueta_pot is not None:
                etiqueta_pot.config(text=f"Valor Potenciómetro: {valor_pot}")

# Crear y destruir widgets
def crear_num_widgets():
    global valor_num, btn_set_num, etiqueta_resultado
    
    valor_num = ttk.Entry(tab2, width=5)
    valor_num.pack(pady=5)
    btn_set_num = ttk.Button(tab2, text="Calcular", command=calcular_num)
    btn_set_num.pack(pady=5)
    etiqueta_resultado = ttk.Label(tab2)
    etiqueta_resultado.pack(pady=5)

def crear_intensidad_widgets():
    global intensidad_spinbox, btn_set_intensidad

    intensidad_spinbox = ttk.Spinbox(tab2, from_=0, to=255, width=5)
    intensidad_spinbox.pack(pady=5)

    btn_set_intensidad = tk.Button(tab2, text="Establecer Intensidad", command=set_intensidad)
    btn_set_intensidad.pack(pady=5)

def eliminar_widgets():
    global intensidad_spinbox, btn_set_intensidad, valor_num, btn_set_num, etiqueta_resultado, etiqueta_pot
    if intensidad_spinbox is not None:
        intensidad_spinbox.destroy()
    if btn_set_intensidad is not None:
        btn_set_intensidad.destroy()
    if valor_num is not None:
        valor_num.destroy()
    if btn_set_num is not None:
        btn_set_num.destroy()
    if etiqueta_resultado is not None:
        etiqueta_resultado.destroy()
    if etiqueta_pot is not None:
        etiqueta_pot.destroy()

    etiqueta_resultado = None
    btn_set_num = None
    valor_num = None
    intensidad_spinbox = None
    btn_set_intensidad = None
    etiqueta_pot = None

def set_opcion():
    global etiqueta_pot
    ejecutar_op = opcion_spinbox.get()
    eliminar_widgets()

    if ejecutar_op == '1':
        print("Opción 1 seleccionada.")
        crear_num_widgets()
    elif ejecutar_op == '2':
        print("Opción 2 seleccionada.")
        etiqueta_pot = ttk.Label(tab2, text="Valor Potenciómetro: ")
        etiqueta_pot.pack(pady=5)
    elif ejecutar_op == '3':
        print("Opción 3 seleccionada.")
        crear_intensidad_widgets()
    else:
        print("Opción no válida.")

# Comandos para cada opción de la pestaña 2
def calcular_num():
    num = float(valor_num.get())
    num_q = float(num + 1)
    etiqueta_resultado.config(text=f"Resultado: {num_q}")

def encender_led():
    ser.write(b'encender\n')  # Envía el comando para encender el LED
    print("LED encendido.")

def apagar_led():
    ser.write(b'apagar\n')  # Envía el comando para apagar el LED
    print("LED apagado.")

def set_intensidad():
    valor = intensidad_spinbox.get()  # Obtiene el valor del Spinbox
    ser.write(f'set_intensidad,{valor}\n'.encode())  # Envía el valor
    print(f'Intensidad del LED establecida en: {valor}')

def cerrar_serial():
    if ser:
        ser.close()
    ventana.destroy()  # Cierra la ventana de la GUI

# Crear la ventana principal y poner tema
ventana = tk.Tk()
ventana.tk.call('source', 'forest-dark.tcl')
ttk.Style().theme_use('forest-dark')


# Crear pestañas
tab_control = ttk.Notebook(ventana)
ventana.geometry("600x600")
ventana.title("PRACTICA 1")



# Opción para seleccionar puerto COM
puerto_seleccionado = tk.StringVar(value=puertos_disponibles[0] if puertos_disponibles else '')
baudrate_seleccionado = tk.StringVar(value='115200')  # Baudrate por defecto

# Pestaña 1: Control de Encendido y Apagado
tab1 = tk.Frame(tab_control)
tab_control.add(tab1, text='Setup')

# Opción para seleccionar puerto COM
ttk.Label(tab1, text="Selecciona el puerto COM:").pack(pady=5)
puerto_menu = ttk.OptionMenu(tab1, puerto_seleccionado, puerto_seleccionado.get(), *puertos_disponibles)
puerto_menu.pack(pady=5)

# Opción para seleccionar baudrate
ttk.Label(tab1, text="Selecciona el Baudrate:").pack(pady=5)
baudrate_menu = ttk.Combobox(tab1, textvariable=baudrate_seleccionado, values=["9600", "115200", "57600", "38400", "19200", "14400"], state='readonly')
baudrate_menu.pack(pady=5)



btn_conectar = tk.Button(tab1, text="Conectar", command=abrir_conexion_serial)
btn_conectar.pack(pady=10)
# Crear un marco para contener los elementos
frame = tk.Frame(ventana, width=1, height=1)
frame.pack_propagate(False)  # Evita que el marco ajuste su tamaño automáticamente
frame.pack(padx=1, pady=1)

# Cargar y redimensionar las imágenes
led_verde = Image.open("led_verde.png").resize((100, 100), Image.LANCZOS)
led_rojo = Image.open("led_rojo.png").resize((100, 100), Image.LANCZOS)

led_verde = ImageTk.PhotoImage(led_verde)
led_rojo = ImageTk.PhotoImage(led_rojo)

imagen_led = tk.Label(tab1)
imagen_led = tk.Label(tab1, image=led_rojo)
imagen_led.pack(pady=20)

btn_encender = tk.Button(tab1, text="Encender LED", command=encender_led)
btn_encender.pack(pady=10)

btn_apagar = tk.Button(tab1, text="Apagar LED", command=apagar_led)
btn_apagar.pack(pady=10)

# Pestaña 2: Control
tab2 = tk.Frame(tab_control)
tab_control.add(tab2, text='Menú')

opciones=ttk.Label(tab2, text="1) NUMERO +1\n\n2) LEER POT\n\n3) INTENSIDAD DEL LED")
opciones.place(x=20, y= 180)
etiqueta_opcion = ttk.Label(tab2, text="Selecciona una opción")
etiqueta_opcion.place(x=115, y=120)
opcion_spinbox = ttk.Spinbox(tab2, from_=1, to=3, state='readonly', width=2)
opcion_spinbox.place(x=250, y=180)
btn_opcion = ttk.Button(tab2, text="SELECCIONAR", command=set_opcion)
btn_opcion.place(x=230, y=230)

# Inicia la lectura en un hilo separado
threading.Thread(target=leer_pot, daemon=True).start()

#Tab Nombres

tab3 = tk.Frame(tab_control)
tab_control.add(tab3, text='EQUIPO')
#Etiquetas de nombres
etiqueta_nombres= ttk.Label(tab3, text="\n\nMikel Dante Rodriguez Rivera 202156246\n\nRaúl Garcia Castillo 202145777\n\nAndrea Catalina Garcia Osorio 202145963\n\nErick Moroni Camacho Torres 202133253", font='Arial,18')
etiqueta_nombres.pack(pady=10)

# Inicia la aplicación
tab_control.pack(expand=1, fill="both")
btn_salir = tk.Button(ventana, text="Salir", command=cerrar_serial)
btn_salir.pack(pady=10)

# Inicia la aplicación
ventana.mainloop()