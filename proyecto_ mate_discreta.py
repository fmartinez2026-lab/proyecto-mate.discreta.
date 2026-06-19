import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
import heapq
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

#FUNCIONES LÓGICAS Y MATEMÁTICAS
def crear_grafo():
    """ Crea y retorna un objeto Grafo de NetworkX (G = (V, E)) """
    G = nx.Graph()
    G.add_nodes_from(CIUDADES)
    for origen, destino, peso in CONEXIONES:
        G.add_edge(origen, destino, weight=peso)
    return G

def dijkstra(grafo, origen, destino):
    """ Implementación del Algoritmo de Dijkstra usando una cola de prioridad """
    distancias = {nodo: float('inf') for nodo in grafo.nodes}
    distancias[origen] = 0
    
    predecesores = {nodo: None for nodo in grafo.nodes}
    cola_prioridad = [(0, origen)]
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        if nodo_actual == destino:
            break
            
        for vecino in grafo.neighbors(nodo_actual):
            peso = grafo[nodo_actual][vecino]['weight']
            nueva_distancia = distancia_actual + peso
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                predecesores[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
                
    # Reconstrucción del camino óptimo
    ruta = []
    nodo_aux = destino
    while nodo_aux is not None:
        ruta.insert(0, nodo_aux)
        nodo_aux = predecesores[nodo_aux]
        
    if distancias[destino] == float('inf'):
        return None, []
        
    return distancias[destino], ruta

#VISUALIZACIÓN Y ELEMENTOS GRÁFICOS
def dibujar_grafo(grafo, ruta_optima=None):
    """ Genera la visualización del grafo con Matplotlib """
    plt.clf() 
    pos = nx.spring_layout(grafo, seed=42) 
    
    nx.draw_networkx_nodes(grafo, pos, node_color='pink', node_size=700)
    nx.draw_networkx_labels(grafo, pos, font_size=9, font_weight='bold')
    
    aristas_ruta = []
    if ruta_optima and len(ruta_optima) > 1:
        for i in range(len(ruta_optima) - 1):
            aristas_ruta.append((ruta_optima[i], ruta_optima[i+1]))
            
    aristas_normales = [e for e in grafo.edges if e not in aristas_ruta and (e[1], e[0]) not in aristas_ruta]
    nx.draw_networkx_edges(grafo, pos, edgelist=aristas_normales, edge_color='gray', width=1.5, alpha=0.6)
    
    if aristas_ruta:
        nx.draw_networkx_edges(grafo, pos, edgelist=aristas_ruta, edge_color='crimson', width=3.5)
        nx.draw_networkx_nodes(grafo, pos, nodelist=ruta_optima, node_color='violet', node_size=800)

    etiquetas_aristas = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=etiquetas_aristas, font_size=8)
    
    plt.title("Mapa de Conexiones Viales y Ruta Óptima", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.margins(0.15)
    
    if not os.path.exists('img'):
        os.makedirs('img')
    plt.savefig('img/grafo.png', bbox_inches='tight')
    plt.show(block=False)

def mostrar_ruta(grafo, combo_origen, combo_destino, label_resultado):
    """ Evento que calcula la ruta al presionar el botón """
    origen = combo_origen.get()
    destino = combo_destino.get()
    
    if origen == destino:
        messagebox.showwarning("Atención", "El origen y el destino deben ser diferentes.")
        return
        
    distancia_total, ruta = dijkstra(grafo, origen, destino)
    
    if not ruta:
        label_resultado.config(text="No se encontró una ruta disponible.")
        return
        
    secuencia_ruta = " ---> ".join(ruta)
    texto_resultado = f"Ruta Óptima:\n{secuencia_ruta}\n\nDistancia Total: {distancia_total} km"
    label_resultado.config(text=texto_resultado)
    
    dibujar_grafo(grafo, ruta)

def iniciar_interfaz():
    """ Construye y despliega la interfaz de usuario con Tkinter """
    G = crear_grafo()
    
    ventana = tk.Tk()
    ventana.title("Optimizador de Rutas en Colombia.lol")
    ventana.geometry("550x400")
    ventana.resizable(False, False)
    
    style = ttk.Style()
    style.theme_use('clam')
    
    frame = ttk.Frame(ventana, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    titulo = ttk.Label(frame, text="Buscador de ruta mas rapida", font=("Arial", 14, "bold"))
    titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    ttk.Label(frame, text="Ciudad de Origen:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
    combo_origen = ttk.Combobox(frame, values=CIUDADES, state="readonly", width=25)
    combo_origen.grid(row=1, column=1, pady=5, padx=10)
    combo_origen.current(0)
    
    ttk.Label(frame, text="Ciudad de Destino:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
    combo_destino = ttk.Combobox(frame, values=CIUDADES, state="readonly", width=25)
    combo_destino.grid(row=2, column=1, pady=5, padx=10)
    combo_destino.current(1)
    
    frame_resultado = ttk.LabelFrame(frame, text=" Resultado del Análisis(aprox) ", padding="10")
    frame_resultado.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=20)
    
    label_resultado = ttk.Label(frame_resultado, text="Seleccione las ciudades y calcule la ruta.", 
                                font=("Arial", 10, "italic"), justify=tk.CENTER, anchor=tk.CENTER)
    label_resultado.pack(fill=tk.BOTH, expand=True)
    
    btn_calcular = ttk.Button(frame, text="Calcular Ruta", 
                              command=lambda: mostrar_ruta(G, combo_origen, combo_destino, label_resultado))
    btn_calcular.grid(row=3, column=0, columnspan=2, pady=15)
    
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
