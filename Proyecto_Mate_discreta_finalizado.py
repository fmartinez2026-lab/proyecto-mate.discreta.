import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
import os

# DATOS DEL PROGRAMA

# Lista de ciudades que formarán los nodos del grafo
CIUDADES = [
    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
    "Bucaramanga", "Cúcuta", "Pereira", "Manizales", "Santa Marta",
    "Villavicencio", "Ibagué", "Pasto", "Montería", "Sincelejo"
]

# Cada tupla tiene:
# (Ciudad origen, Ciudad destino, Distancia en kilómetros)
CONEXIONES = [
    ("Bogotá", "Medellín", 415),
    ("Bogotá", "Ibagué", 200),
    ("Bogotá", "Villavicencio", 120),
    ("Bogotá", "Bucaramanga", 400),
    ("Medellín", "Cali", 420),
    ("Medellín", "Manizales", 200),
    ("Medellín", "Montería", 400),
    ("Cali", "Ibagué", 270),
    ("Cali", "Pasto", 380),
    ("Manizales", "Pereira", 50),
    ("Pereira", "Ibagué", 120),
    ("Bucaramanga", "Cúcuta", 230),
    ("Bucaramanga", "Santa Marta", 540),
    ("Montería", "Sincelejo", 120),
    ("Sincelejo", "Cartagena", 170),
    ("Cartagena", "Barranquilla", 120),
    ("Barranquilla", "Santa Marta", 100),
    ("Bucaramanga", "Medellín", 390),
    ("Sincelejo", "Medellín", 460),
    ("Cúcuta", "Bogotá", 550),
    ("Pereira", "Cali", 210),
    ("Villavicencio", "Bucaramanga", 490)
]


# FUNCIÓN PARA CREAR EL GRAFO----------

def crear_grafo():
    """
    Crea un grafo no dirigido.

    Cada ciudad será un nodo.
    Cada conexión será una arista con un peso
    que representa la distancia en kilómetros.
    """

    G = nx.Graph()

    # Agrega todas las conexiones con sus pesos
    G.add_weighted_edges_from(CONEXIONES)

    return G


# FUNCIÓN PARA DIBUJAR EL GRAFO--------------

def dibujar_grafo(G, ruta=None):
    """
    Dibuja el mapa de ciudades y sus conexiones.

    Si se recibe una ruta, esta se resalta
    con un color diferente.
    """

    # Limpia la figura anterior
    plt.clf()

    # Genera posiciones automáticas para los nodos
    pos = nx.spring_layout(G, seed=42)

    # Dibuja todos los nodos y conexiones normales
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="pink",
        node_size=700,
        font_size=8,
        edge_color="gray"
    )

    # Si existe una ruta óptima, la resaltamos
    if ruta and len(ruta) > 1:

        # Convierte la lista de ciudades en pares de aristas
        # Ejemplo:
        # [Bogotá, Medellín, Cali]
        # se convierte en:
        # [(Bogotá, Medellín), (Medellín, Cali)]
        aristas = list(zip(ruta, ruta[1:]))

        # Colorea los nodos de la ruta
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=ruta,
            node_color="violet",
            node_size=800
        )

        # Colorea las conexiones de la ruta
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=aristas,
            edge_color="red",
            width=3
        )

    # Obtiene las distancias de cada carretera
    etiquetas = nx.get_edge_attributes(G, "weight")

    # Muestra los pesos sobre las aristas
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=etiquetas
    )

    # Título de la gráfica
    plt.title("Ruta óptima entre ciudades de Colombia")

    # Oculta los ejes de coordenadas
    plt.axis("off")

    # Crea la carpeta img si no existe
    os.makedirs("img", exist_ok=True)

    # Guarda la imagen del grafo
    plt.savefig("img/grafo.png")

    # Muestra la ventana con el grafo
    plt.show(block=False)

# FUNCIÓN PARA CALCULAR LA RUTA---------------

def calcular_ruta():
    """
    Obtiene las ciudades seleccionadas,
    calcula la ruta más corta mediante
    el algoritmo de Dijkstra y muestra
    el resultado.
    """

    # Obtiene las ciudades elegidas
    origen = combo_origen.get()
    destino = combo_destino.get()

    # Verifica que las ciudades sean distintas
    if origen == destino:
        messagebox.showwarning(
            "Atención",
            "Seleccione ciudades diferentes."
        )
        return

    try:
        # Calcula la ruta más corta usando Dijkstra
        ruta = nx.shortest_path(
            G,
            origen,
            destino,
            weight="weight"
        )

        # Calcula la distancia total
        distancia = nx.shortest_path_length(
            G,
            origen,
            destino,
            weight="weight"
        )

        # Convierte la lista en un texto
        # Ejemplo:
        # Bogotá → Medellín → Cali
        texto = (
            f"Ruta óptima:\n"
            f"{' → '.join(ruta)}\n\n"
            f"Distancia: {distancia} km"
        )

        # Muestra el resultado en la interfaz
        resultado.config(text=texto)

        # Dibuja la ruta encontrada
        dibujar_grafo(G, ruta)

    # Se ejecuta si no existe una ruta posible
    except nx.NetworkXNoPath:
        resultado.config(
            text="No existe una ruta disponible."
        )



# CREACIÓN DEL GRAFO------


# Construye el grafo una sola vez al iniciar el programa
G = crear_grafo()



# INTERFAZ GRÁFICA----

# Crea la ventana principal
ventana = tk.Tk()

# Título de la ventana
ventana.title("Rutas entre ciudades de Colombia")

# Tamaño de la ventana
ventana.geometry("550x380")

# Impide cambiar el tamaño de la ventana
ventana.resizable(False, False)

# Marco principal donde se colocarán los elementos
frame = ttk.Frame(ventana, padding=20)
frame.pack(fill="both", expand=True)

# Título principal
ttk.Label(
    frame,
    text="Buscador de rutas",
    font=("Arial", 14, "bold")
).grid(row=0, column=0, columnspan=2, pady=20)

# SELECCIÓN DE ORIGEN

ttk.Label(
    frame,
    text="Origen:"
).grid(row=1, column=0)

# Lista desplegable de ciudades
combo_origen = ttk.Combobox(
    frame,
    values=CIUDADES,
    state="readonly",
    width=25
)
combo_origen.grid(row=1, column=1)

# Ciudad seleccionada por defecto
combo_origen.current(0)

# SELECCIÓN DE DESTINO

ttk.Label(
    frame,
    text="Destino:"
).grid(row=2, column=0)

combo_destino = ttk.Combobox(
    frame,
    values=CIUDADES,
    state="readonly",
    width=25
)
combo_destino.grid(row=2, column=1)

# Selecciona Medellín por defecto
combo_destino.current(1)

# BOTÓN DE CÁLCULO

ttk.Button(
    frame,
    text="Calcular ruta",
    command=calcular_ruta
).grid(
    row=3,
    column=0,
    columnspan=2,
    pady=20
)

# ETIQUETA DE RESULTADOS

resultado = ttk.Label(
    frame,
    text="Seleccione dos ciudades.",
    justify="center"
)
resultado.grid(
    row=4,
    column=0,
    columnspan=2
)

# Mantiene la ventana abierta y esperando eventos
ventana.mainloop()