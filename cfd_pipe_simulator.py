# Importación de librerías
import numpy
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import IntVar
from collections import deque

## ····· Variables ····· ····· ····· ##
nx = 41 # Número de nodos en la dirección X
ny = 41 # Número de nodos en la dirección Y
nit = 20 # Número de iteraciones para el método de Poisson (para calcular la presión)
dx = 2/(nx-1) # Tamaño del incremento en X
dy = 2/(ny-1) # Tamaño del incremento en Y
dt = .0005 # Incremento de tiempo ⚠️ Change this value until it works in your device, better start with lower dt if it doesn't works
x = numpy.linspace(0, 2, nx) # Coordenadas X desde 0 hasta 2
y = numpy.linspace(0, 2, ny) # Coordenadas Y desde 0 hasta 2
X, Y = numpy.meshgrid(x, y) # Matrices que dfinen la malla X e Y

# · · · Propiedades del fluido
rho = 1 # Densidad del fluido
nu = 1 # Viscosidad del fluido
u = numpy.zeros((nx, ny)) # Campo de velocidad en la dirección X (inicialmente 0)
v = numpy.zeros((nx, ny)) # Campo de velocidad en la dirección Y (inicialmente 0)
p = numpy.zeros((nx, ny)) # Campo de presión (inicialmente 0)
b = numpy.zeros((nx, ny)) # Variable auxiliar utilizada en el método de Poisson para la presión

# · · ·
xr, xm = 0, 0 # Posición X real y en la matriz del raton
yr, ym = 0, 0 # Posición Y real y en la matriz del raton
Fx = numpy.zeros((nx, ny)) # Fuerza X
Fy = numpy.zeros((nx, ny)) # Fuerza Y / Cond. Iniciales --> 0
Fx[:, :] = 1 # Condiciones iniciales Fuerza X --> 1
posiciones_anteriores = deque(maxlen=2) # Crear pila de posiciónes para la dirección

## ····· Funciones ····· ····· ····· ##
def build_up_b(b, rho, dt, u, v, dx, dy): # Calcula el término b de la ecuación de Poisson (auxiliar)
    b[1:-1, 1:-1] = (rho * (1 / dt * #
    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx) + #
    (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy)) - #
    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 - #
    2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) * #
    (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) - #
    ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2)) #
    return b

def pressure_poisson(p, dx, dy, b): # Resuelve la ecuación de Poisson para la presión
    pn = numpy.empty_like(p) # Crear matriz para usarla en los cálculos (t-1)
    pn = p.copy() #
    for q in range(nit): # Iteración predefinida
        pn = p.copy() # Copia de la matriz para usarla en los cálculos (t-1)
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 +
        (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
        (2 * (dx**2 + dy**2)) -
        dx**2 * dy**2 / (2 * (dx**2 + dy**2)) * b[1:-1,1:-1])

        p[:, -1] = 0 # Condiciones de contorno
        p[0, :] = p[1, :] # Simetria en las paredes
        p[-1, :] = p[-2, :] # " "
        p[:, 0] = 0 #
        p[xm-5:xm+5, ym+5] = p[xm-5:xm+5, ym+6] # Asignar valores
        p[xm-5:xm+5, ym-5] = p[xm-5:xm+5, ym-6] # en la posición del
        p[xm-5, ym-5:ym+5] = p[xm-6, ym-5:ym+5] # raton para el
        p[xm+5, ym-5:ym+5] = p[xm+6, ym-5:ym+5] # objeto
    return p

def cavity_flow(nt, u, v, dt, dx, dy, p, rho, nu): # Resuelve la ecuación de momento
    un = numpy.empty_like(u) # Crear la matriz para usarla en los cálculos (t-1)
    vn = numpy.empty_like(v) # Crear la matriz para usarla en los cálculos (t-1)
    b = numpy.zeros((ny, nx)) # Llamamos a la variable
    for n in range(nt): # Iteración en el tiempo
        un = u.copy() # Copia de la matriz para usarla en los cálculos (t-1)
        vn = v.copy() # Copia de la matriz para usarla en los cálculos (t-1)
        b = build_up_b(b, rho, dt, u, v, dx, dy) # Iteració de la pressió
        p = pressure_poisson(p, dx, dy, b) #
        u[1:-1, 1:-1] = (un[1:-1, 1:-1] - #
        un[1:-1, 1:-1] * dt / dx * #
        (un[1:-1, 1:-1] - un[1:-1, 0:-2]) - #
        vn[1:-1, 1:-1] * dt / dy * #
        (un[1:-1, 1:-1] - un[0:-2, 1:-1]) - #
        dt / (2 * rho * dx) * #
        (p[1:-1, 2:] - p[1:-1, 0:-2]) + #
        nu * (dt / dx**2 * #
        (un[1:-1, 2:] - 2 * un[1:-1, 1:-1] + un[1:-1, 0:-2]) + #
        dt / dy**2 * #
        (un[2:, 1:-1] - 2 * un[1:-1, 1:-1] + un[0:-2, 1:-1])) + #
        Fx[1:-1, 1:-1] * dt) #

        v[1:-1, 1:-1] = (vn[1:-1, 1:-1] - #
        un[1:-1, 1:-1] * dt / dx * #
        (vn[1:-1, 1:-1] - vn[1:-1, 0:-2]) - #
        vn[1:-1, 1:-1] * dt / dy * #
        (vn[1:-1, 1:-1] - vn[0:-2, 1:-1]) - #
        dt / (2 * rho * dy) * #
        (p[2:, 1:-1] - p[0:-2, 1:-1]) + #
        nu * (dt / dx**2 * #
        (vn[1:-1, 2:] - 2 * vn[1:-1, 1:-1] + vn[1:-1, 0:-2]) + #
        dt / dy**2 * #
        (vn[2:, 1:-1] - 2 * vn[1:-1, 1:-1] + vn[0:-2, 1:-1])) + #
        Fy[1:-1, 1:-1] * dt) #

        u[1:-1, -1] = (un[1:-1, -1] - un[1:-1, -1] * dt / dx *
        (un[1:-1, -1] - un[1:-1, -2]) -
        vn[1:-1, -1] * dt / dy *
        (un[1:-1, -1] - un[0:-2, -1]) -
        dt / (2 * rho * dx) *
        (p[1:-1, 0] - p[1:-1, -2]) +
        nu * (dt / dx**2 *
        (un[1:-1, 0] - 2 * un[1:-1,-1] + un[1:-1, -2]) +
        dt / dy**2 *
        (un[2:, -1] - 2 * un[1:-1, -1] + un[0:-2, -1])) + Fx[1:-1,-1] * dt)

        u[1:-1, 0] = (un[1:-1, 0] - un[1:-1, 0] * dt / dx *
        (un[1:-1, 0] - un[1:-1, -1]) -
        vn[1:-1, 0] * dt / dy *
        (un[1:-1, 0] - un[0:-2, 0]) -
        dt / (2 * rho * dx) *
        (p[1:-1, 1] - p[1:-1, -1]) +
        nu * (dt / dx**2 *
        (un[1:-1, 1] - 2 * un[1:-1, 0] + un[1:-1, -1]) +
        dt / dy**2 *
        (un[2:, 0] - 2 * un[1:-1, 0] + un[0:-2, 0])) + Fx[1:-1, 0] * dt)

        v[1:-1, -1] = (vn[1:-1, -1] - un[1:-1, -1] * dt / dx *
        (vn[1:-1, -1] - vn[1:-1, -2]) -
        vn[1:-1, -1] * dt / dy *
        (vn[1:-1, -1] - vn[0:-2, -1]) -
        dt / (2 * rho * dy) *
        (p[2:, -1] - p[0:-2, -1]) +
        nu * (dt / dx**2 *
        (vn[1:-1, 0] - 2 * vn[1:-1, -1] + vn[1:-1, -2]) +
        dt / dy**2 *
        (vn[2:, -1] - 2 * vn[1:-1, -1] + vn[0:-2, -1])) + Fy[1:-1,-1] * dt )

        v[1:-1, 0] = (vn[1:-1, 0] - un[1:-1, 0] * dt / dx *
        (vn[1:-1, 0] - vn[1:-1, -1]) -
        vn[1:-1, 0] * dt / dy *
        (vn[1:-1, 0] - vn[0:-2, 0]) -
        dt / (2 * rho * dy) *
        (p[2:, 0] - p[0:-2, 0]) +
        nu * (dt / dx**2 *
        (vn[1:-1, 1] - 2 * vn[1:-1, 0] + vn[1:-1, -1]) +
        dt / dy**2 *
        (vn[2:, 0] - 2 * vn[1:-1, 0] + vn[0:-2, 0])) + Fy[1:-1, 0] * dt )

        u[0, :] = 0 # Condiciones de contorno
        u[-1, :] = 0 #
        v[0, :] = 0 #
        v[-1, :] = 0 #
        if square.get() == 1: # Asignar valores en la posición del raton para el objeto según si és un circulo o un cuadrado
            u[xm-5: xm+5, ym-5: ym+5] = 0 # 
            v[xm-5: xm+5, ym-5: ym+5] = 0 # 
        elif circle.get() == 1: #
            u[xm-2: xm+2, ym+2] = 0 # 
            u[xm-3: xm+3, ym+1] = 0 # 
            u[xm-3: xm+3, ym] = 0 # 
            u[xm-3: xm+3, ym-1] = 0 # 
            u[xm-2: xm+2, ym-2] = 0 # 
            v[xm-2: xm+2, ym+2] = 0 # 
            v[xm-3: xm+3, ym+1] = 0 # 
            v[xm-3: xm+3, ym] = 0 # 
            v[xm-3: xm+3, ym-1] = 0 # 
            v[xm-2: xm+2, ym-2] = 0 # 
        Fx[xm-7: xm+7, ym-7: ym+7], Fy[xm-7: xm+7, ym-7: ym+7] = calcular_fuerza() # Aplicar Fuerzas
        Fx.fill(1)
    return u, v, p

## ····· Funciones de Visualización ····· ##
def update_plot(): # Actualiza el gráfico en la interfaz de usuario
    global u, v, p # Llamar variables
    ax.clear() # Limpiar la gráfica
    u, v, p = cavity_flow(1, u, v, dt, dx, dy, p, rho, nu) # Calcular velocidades y presión
    if show_pressure.get() == 1: # Mostrar lineas, vectores o mapa de presión según el boton
        pyplot.contourf(X, Y, p, alpha=0.5, cmap=pyplot.cm.viridis) #
    if show_quiver.get() == 1: #
        pyplot.quiver(X[::3, ::3], Y[::3, ::3], u[::3, ::3], v[::3, ::3]) # 
    if show_streamlines.get() == 1: #
        pyplot.streamplot(X, Y, u, v, start_points=start_points) # 
    ax.set_xlabel('X') #
    ax.set_ylabel('Y') #
    if square.get() == 1: #
        ax.scatter(xr, yr, s=2500, color='red', marker='s') # cursor --> cuadraado
    elif circle.get() == 1: #
        ax.scatter(xr, yr, s=1500, color='red', marker='o') # cursor --> circlo
    canvas.draw()
    root.after(1, update_plot)

## ····· Funciones de Interacción ····· ##
def get_mouse_position(event): # Obtener posición del raton para la interacción
    global xm, ym, xr, yr
    if event.xdata is not None and event.ydata is not None:
        # Que no se salga de los valores permitidos dentro de la matriz de valores
        if 6 <= int(event.xdata*int(nx/2)) < nx-6 and 6 <= int(event.ydata*int(ny/2)) < ny-6:
            ym = int(event.xdata * int(nx/2)) # Asignar posición del raton en la matriz
            xm = int(event.ydata * int(ny/2)) #
            xr, yr = event.xdata, event.ydata # Asignar posición real en la ventana
            posiciones_anteriores.append((xr, yr)) # Añadir posición del raton para obtener dirección

def calcular_fuerza():
    if len(posiciones_anteriores) < 2:
        return 0, 0
    pos_actual = posiciones_anteriores[1] # Pasar posiciones de la pila
    pos_anterior = posiciones_anteriores[0] # a variables
    diferencia_x = pos_anterior[0] - pos_actual[0] # Calcular dirección con la diferencia de pos.
    diferencia_y = pos_actual[1] - pos_anterior[1] # 
    fuerza_x = -2 * diferencia_x # Coeficiente -2 para controlar la fuerza (F=ma-->m)
    fuerza_y = -2 * diferencia_y # Coeficiente -2 para controlar la fuerza
    return fuerza_x, fuerza_y

## Configuración de la Interfaz ····· ····· ##
root = tk.Tk() # Crear la ventana principal
root.title("Gráfico Matplotlib en Tkinter") # Establecer el título
frame = tk.Frame(root) # Crear un marco en la ventana
frame.pack(side="left") # Posicionar el marco en el lado izquierdo

# Crear una figura de Matplotlib
fig = pyplot.figure(figsize=(9, 5), dpi=100)
ax = fig.gca() # Crear ejes en la figura
start_points = numpy.array([[0, 0.0], # Define las coordenadas iniciales del origen de las lineas de corriente (hecho con excel)
[0, 0.10526315789473684], 
[0, 0.21052631578947367], 
[0, 0.3157894736842105], 
[0, 0.42105263157894735], 
[0, 0.5263157894736842], 
[0, 0.631578947368421], 
[0, 0.7368421052631579], 
[0, 0.8421052631578947], 
[0, 0.9473684210526315], 
[0, 1.0526315789473684], 
[0, 1.1578947368421053], 
[0, 1.263157894736842], 
[0, 1.368421052631579], 
[0, 1.4736842105263157], 
[0, 1.5789473684210527], 
[0, 1.6842105263157894], 
[0, 1.7894736842105263], 
[0, 1.894736842105263], 
[0, 2.0]]) 

# Crear una imagen con mapa de colores
im = ax.imshow(p, cmap='viridis', vmin=0, vmax=200)
# Agregar una barra de color (colorbar) a la figura
cbar = fig.colorbar(im)
# Crear un lienzo para mostrar la figura de Matplotlib en Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Variables de control para botones de verificación
show_pressure = IntVar()
show_pressure.set(1) # Presión activada por defecto
show_quiver = IntVar()
show_quiver.set(1) # Quiver activado por defecto
show_streamlines = IntVar()
show_streamlines.set(0)

# Botones de verificación (checkbuttons) para activar/desactivar gráficos
pressure_checkbox = tk.Checkbutton(root, text="Presión", variable=show_pressure)
pressure_checkbox.pack()
quiver_checkbox = tk.Checkbutton(root, text="Velocidades", variable=show_quiver)
quiver_checkbox.pack()
streamlines_checkbox = tk.Checkbutton(root, text=" Lineas de Corriente", variable=show_streamlines)
streamlines_checkbox.pack()

# Botones circulo-cuadrado
circle = IntVar()
circle.set(0)
square = IntVar()
square.set(1)
circle_checkbox = tk.Checkbutton(root, text="Circulo", variable=circle)
circle_checkbox.pack()
square_checkbox = tk.Checkbutton(root, text="Cuadrado", variable=square)
square_checkbox.pack()

# Conectar la función get_mouse_position a un evento (al mover el raton)
canvas.mpl_connect('motion_notify_event', get_mouse_position)
# Iniciar la actualización del gráfico
root.after(1, update_plot)
# Iniciar el loop de la aplicación Tkinter
root.mainloop()
