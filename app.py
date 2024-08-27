#!/usr/bin/env python3

import cv2
import numpy as np
import pyautogui as pg
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def capturarPunto(event=None):
    # Coordenadas del cursor
    position = pg.position()

    # Captura del área
    screenshot = pg.screenshot(region=(position[0]-1, position[1]-1, 1, 1))
    
    # Convierte la imagen a RGB
    im = screenshot.convert('RGB')

    # Obtiene el color del píxel en la posición (0, 0) de la región capturada
    color = im.getpixel((0, 0))

    # Mostrar los valores RGB en el Label
    rgb_values.set(f'R: {color[0]} \nG: {color[1]} \nB: {color[2]}')

    # Colocar los valores RGB en el Entry para copiarlos
    entry_rgb.delete(0, tk.END)
    entry_rgb.insert(0, f'{color[0]} {color[1]} {color[2]}')

    print(f'R:{color[0]} G:{color[1]} B:{color[2]}')

    # Convertir en array, el área capturada con numpy
    screenshot = np.array(screenshot)
    print(screenshot[0][0])

    # Cambia el fondo de la ventana al color capturado
    hex_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
    frameTop.config(background=hex_color)
    print(hex_color)

    return color

def copiar_al_portapapeles():
    rgb_value = entry_rgb.get()  
    root.clipboard_clear()
    root.clipboard_append(rgb_value)
    root.update()

    print(f'Valor RGB copiado al portapapeles: {rgb_value}')

# Función para actualizar la imagen en el Label de Tkinter
def update_image():
    # Tamaño del área que se mostrará
    size = 15
    position = pg.position()
    screenshot = pg.screenshot(region=(int(position[0]-size/2), int(position[1]-size/2), size, size))

    # Convierte el array de la captura a BGR
    im = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Amplía el área del cursor
    im = cv2.resize(im, (size*10, size*10), interpolation=cv2.INTER_AREA)

    # Rectángulo en el centro de la imagen
    startingC = int((size*10)/2 - 5)
    endingC = int((size*10)/2 + 5)
    im = cv2.rectangle(im, (startingC, startingC), (endingC, endingC), (0,0,0), 3)

    # Convertir la imagen a un formato que Tkinter pueda usar
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(im)
    imgtk = ImageTk.PhotoImage(image=im_pil)

    # Actualiza la imagen en el Label
    label.config(image=imgtk)
    label.image = imgtk

    # Se llama a sí misma cada 10 ms
    root.after(10, update_image)


# Ventana principal
root = tk.Tk()
root.geometry("300x350")
root.title("Cuentagotas")
root.iconbitmap("favicon.ico")

# Frame superior
frameTop = tk.Frame(root)
frameTop.pack(side="top", fill="both", expand=True)

# Label de la imagen
label = ttk.Label(frameTop)
label.pack(pady=15)

# Instrucciones
label_font = ("Helvetica", 10, "bold")
label_instruction = ttk.Label(frameTop, text='Presiona ESPACIO para capturar', foreground="white", background="black", anchor="center", font=label_font)
label_instruction.pack(ipadx=5, ipady=5)

# Frame inferior
frameBottom = ttk.Frame(root)
frameBottom.pack(side="top", fill="both", expand=True)

# Variable de valores RGB
rgb_values = tk.StringVar()
label_rgb = ttk.Label(frameBottom, textvariable=rgb_values)
label_rgb.pack(pady=10)

# Entry de los valores RGB. Permite copiarlos
entry_rgb = ttk.Entry(frameBottom, justify='center')
entry_rgb.pack()
# entry_rgb.grid(row=0, column=1, columnspan=2)

# Botones para copiar
btn_copiar = ttk.Button(frameBottom, text="Copiar", command=copiar_al_portapapeles)
btn_copiar.pack(pady=10)

# Espacio para capturar el punto
root.bind('<space>', capturarPunto)

# Inicia la actualización de la imagen
update_image()

root.mainloop()
print("Programa finalizado")