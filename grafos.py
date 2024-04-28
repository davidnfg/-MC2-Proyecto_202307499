import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GraphApp:
    def __init__(self, master):
        # Inicialización de la aplicación gráfica
        self.master = master
        self.master.title("Grafos")

        # Creación de los lienzos para mostrar los grafos
        self.canvas_left = FigureCanvasTkAgg(plt.figure(figsize=(5, 5)), master=self.master)
        self.canvas_left.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_right = FigureCanvasTkAgg(plt.figure(figsize=(5, 5)), master=self.master)
        self.canvas_right.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Creación del frame para los elementos de la interfaz
        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH)

        # Creación de etiquetas y campos de entrada para vértices y aristas
        self.vertices_label = tk.Label(self.frame, text="Vértices:")
        self.vertices_label.grid(row=0, column=0)

        self.vertices_entry = tk.Entry(self.frame)
        self.vertices_entry.grid(row=0, column=1)

        self.edge_label = tk.Label(self.frame, text="Arista (A--B):")
        self.edge_label.grid(row=1, column=0)

        self.edge_entry = tk.Entry(self.frame)
        self.edge_entry.grid(row=1, column=1)

        # Botón para agregar aristas al grafo
        self.add_button = tk.Button(self.frame, text="Agregar", command=self.add_edge)
        self.add_button.grid(row=1, column=2)

        # Resumen de las aristas ingresadas
        self.summary_label = tk.Label(self.frame, text="Resumen:")
        self.summary_label.grid(row=2, column=0)

        self.summary_text = tk.Text(self.frame, height=10, width=30)
        self.summary_text.grid(row=2, column=1, columnspan=2)

        # Botón para generar el grafo original
        self.generate_button = tk.Button(self.frame, text="Generar Grafo", command=self.generate_graph)
        self.generate_button.grid(row=3, column=1, columnspan=2)

        # Botón para agregar el árbol de búsqueda
        self.add_tree_button = tk.Button(self.frame, text="Agregar Árbol", command=self.add_tree)
        self.add_tree_button.grid(row=4, column=1, columnspan=2)

        # Selección del algoritmo de búsqueda (Anchura o Profundidad)
        self.search_label = tk.Label(self.frame, text="Algoritmo:")
        self.search_label.grid(row=5, column=0)

        self.search_var = tk.StringVar()
        self.search_var.set("Anchura")  # Valor predeterminado
        self.search_dropdown = tk.OptionMenu(self.frame, self.search_var, "Anchura", "Profundidad")
        self.search_dropdown.grid(row=5, column=1, columnspan=2)

        # Creación del grafo
        self.graph = nx.Graph()

    def add_edge(self):
        # Función para agregar una arista al grafo
        edge = self.edge_entry.get()
        try:
            a, b = edge.split("--")
            self.graph.add_edge(a.strip(), b.strip())
            self.summary_text.insert(tk.END, f"Arista: {a.strip()}--{b.strip()}\n")
        except ValueError:
            messagebox.showerror("Error", "Formato de arista incorrecto (A--B)")

    def generate_graph(self):
        # Función para generar el grafo original
        self.draw_graph(self.graph, self.canvas_left)

    def add_tree(self):
        # Función para agregar el árbol de búsqueda
        search_algorithm = self.search_var.get()
        source_nodes = [node.strip() for node in self.vertices_entry.get().split(",")]
        if all(node in self.graph for node in source_nodes):
            if search_algorithm == "Anchura":
                tree = nx.bfs_tree(self.graph, source=source_nodes[0])
            else:
                tree = nx.dfs_tree(self.graph, source=source_nodes[0])
            self.draw_graph(tree, self.canvas_right)
        else:
            messagebox.showerror("Error", "Uno o más nodos no están presentes en el grafo.")

    def draw_graph(self, graph, canvas):
        # Función para dibujar un grafo en un lienzo
        canvas.figure.clear()  # Limpiar la figura antes de dibujar

        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, ax=canvas.figure.add_subplot(111))

        canvas.draw()

def main():
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
