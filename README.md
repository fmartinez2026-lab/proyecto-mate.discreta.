# proyecto-mate.discreta.
calculador de rutas optimas

Este es un proyecto que consiste en un calculador de rutas óptimas con una interfaz gráfica amigable e intuitiva. El programa modela el mapa vial de 15 ciudades principales de Colombia mediante la teoría de grafos, devolviendo el camino más corto posible en distancia y tiempo de ejecución.

¿Como usarlo?

1. Inicia el programa: Ejecuta el archivo de Python para desplegar la ventana principal.
2. Selecciona los destinos: En los menús desplegables de la interfaz gráfica, elige una ciudad de Origen y una de Destino.
3. Calcula la ruta: Haz clic en el botón "Calcular ruta".
4. Visualiza el resultado: * En la misma ventana verás el desglose del texto con las paradas exactas (ej. Bogotá → Ibagué → Cali) junto con los kilómetros totales.
5. Se abrirá automáticamente un gráfico dinámico en color donde se iluminará en rojo el camino óptimo y en violeta las ciudades visitadas.

ciudades incluidas (15)

Bogotá (Capital),
Medellín,
Cali,
Barranquilla,
Cartagena,
Bucaramanga,
Cúcuta,
Pereira,
Manizales,
Santa Marta,
Villavicencio,
Ibagué,
Pasto,
Montería,
Sincelejo.


Requerimientos
Para ejecutar este proyecto, es necesario contar con las siguientes librerías:
tkinter
networkx
matplotlib.pyplot
heapq
os
