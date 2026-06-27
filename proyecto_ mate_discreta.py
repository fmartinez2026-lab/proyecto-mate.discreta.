import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
import os

CIUDADES = [
    "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
    "Bucaramanga", "Cúcuta", "Pereira", "Manizales", "Santa Marta",
    "Villavicencio", "Ibagué", "Pasto", "Montería", "Sincelejo"
]

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

def crear_grafo():

    G = nx.Graph()

    G.add_weighted_edges_from(CONEXIONES)

    return G

def dibujar_grafo(G, ruta=None):

    plt.clf()

    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="pink",
        node_size=700,
        font_size=8,
        edge_color="gray"
    )

    if ruta and len(ruta) > 1:

        aristas = list(zip(ruta, ruta[1:]))

        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=ruta,
            node_color="violet",
            node_size=800
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=aristas,
            edge_color="red",
            width=3
        )

    etiquetas = nx.get_edge_attributes(G, "weight")

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=etiquetas
    )

    plt.title("Ruta óptima entre ciudades de Colombia")
    plt.axis("off")
    os.makedirs("img", exist_ok=True)
    plt.savefig("img/grafo.png")
    plt.show(block=False)

def calcular_ruta():

    origen = combo_origen.get()
    destino = combo_destino.get()

    if origen == destino:
        messagebox.showwarning(
            "Atención",
            "Seleccione ciudades diferentes."
        )
        return

    try:
  
        ruta = nx.shortest_path(
            G,
            origen,
            destino,
            weight="weight"
        )

        distancia = nx.shortest_path_length(
            G,
            origen,
            destino,
            weight="weight"
        )

        texto = (
            f"Ruta óptima:\n"
            f"{' → '.join(ruta)}\n\n"
            f"Distancia: {distancia} km"
        )

        resultado.config(text=texto)

        dibujar_grafo(G, ruta)

    except nx.NetworkXNoPath:
        resultado.config(
            text="No existe una ruta disponible."
        )

G = crear_grafo()

ventana = tk.Tk()

ventana.title("Rutas entre ciudades de Colombia")

ventana.geometry("550x380")

ventana.resizable(False, False)

frame = ttk.Frame(ventana, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(
    frame,
    text="Buscador de rutas",
    font=("Arial", 14, "bold")
).grid(row=0, column=0, columnspan=2, pady=20)

ttk.Label(
    frame,
    text="Origen:"
).grid(row=1, column=0)

combo_origen = ttk.Combobox(
    frame,
    values=CIUDADES,
    state="readonly",
    width=25
)
combo_origen.grid(row=1, column=1)

combo_origen.current(0)

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

combo_destino.current(1)

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

ventana.mainloop()
