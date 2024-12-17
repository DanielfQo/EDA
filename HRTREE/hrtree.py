import networkx as nx
import matplotlib.pyplot as plt

import copy

class HRTreeNode:
    def __init__(self, is_leaf=False, timestamp=None):
        self.is_leaf = is_leaf  # Indica si el nodo es hoja
        self.entries = []       # Contiene pares (MBR, puntero o ID)
        self.timestamp = timestamp  # Marca de tiempo del nodo

class HRTree:
    def __init__(self):
        self.history = []   # Array que apunta a las raíces de las versiones del árbol
        self.current_time = -1  # Tiempo actual del árbol (empezamos en -1, así la primera versión es 0)
    
    def create_new_version(self):
        self.current_time += 1
        if self.history:
            # Crear una copia profunda de la última versión
            new_root = copy.deepcopy(self.history[-1])
            new_root.timestamp = self.current_time
            self.history.append(new_root)
        else:
            # Primera versión: crear raíz
            root = HRTreeNode(is_leaf=True, timestamp=self.current_time)
            self.history.append(root)

    def insert(self, mbr):
        """Inserta un nuevo MBR en el árbol en la versión actual."""
        if not self.history:
            # Si el árbol está vacío, crear la primera versión y raíz
            self.create_new_version()

        root = self.history[-1]
        updated_root, new_sibling = self._insert_recursive(root, mbr)

        # Si hubo división en la raíz
        if new_sibling is not None:
            # Crear un nuevo nodo raíz que apunte a los dos nodos resultantes
            new_root = HRTreeNode(is_leaf=False, timestamp=self.current_time)
            new_root.entries = [
                (self._calculate_mbr(updated_root.entries), updated_root),
                (self._calculate_mbr(new_sibling.entries), new_sibling)
            ]
            self.history[-1] = new_root
        else:
            self.history[-1] = updated_root

    def _insert_recursive(self, node, mbr):
        """Inserta un MBR de forma recursiva en el nodo dado.
           Devuelve: (nodo_actualizado, nuevo_hermano_o_None)"""
        # Crear copia si el timestamp no coincide con la versión actual
        if node.timestamp < self.current_time:
            new_node = HRTreeNode(is_leaf=node.is_leaf, timestamp=self.current_time)
            new_node.entries = list(node.entries)
        else:
            new_node = node

        if new_node.is_leaf:
            # Insertar el MBR directamente en la hoja
            if len(new_node.entries) < self._max_entries():
                new_node.entries.append((mbr, None))
                return new_node, None
            else:
                # Dividir el nodo hoja
                return self._split_node(new_node, (mbr, None))
        else:
            # Elegir el hijo adecuado
            best_child = self._choose_subtree(new_node, mbr)
            updated_child, new_sibling = self._insert_recursive(best_child, mbr)
            
            # Actualizar la entrada correspondiente al hijo modificado
            self._update_entry(new_node, best_child, updated_child)

            # Si hubo división en el hijo
            if new_sibling is not None:
                # Añadir el nuevo hermano al nodo actual
                new_node.entries.append((self._calculate_mbr(new_sibling.entries), new_sibling))
                # Comprobar si es necesario dividir el nodo actual
                if len(new_node.entries) > self._max_entries():
                    return self._split_node(new_node)
            
            return new_node, None

    def query(self, query_mbr, time_point=None):
        """Consulta los MBRs que se superponen con query_mbr en una versión específica."""
        if time_point is None:
            time_point = self.current_time
        # Asegurarse de que time_point exista
        if time_point < 0 or time_point >= len(self.history):
            return []
        
        root = self.history[time_point]
        results = []
        self._query_recursive(root, query_mbr, results)
        return results

    def _query_recursive(self, node, query_mbr, results):
        """Realiza la consulta de forma recursiva."""
        for mbr, pointer in node.entries:
            if self._mbr_overlap(mbr, query_mbr):
                if node.is_leaf:
                    results.append(mbr)
                else:
                    self._query_recursive(pointer, query_mbr, results)

    # Métodos auxiliares
    def _max_entries(self):
        return 4  # Máximo de entradas por nodo (por simplicidad)

    def _split_node(self, node, new_entry=None):
        """Divide un nodo lleno. Retorna (nuevo_nodo_izq, nuevo_nodo_der). 
           Si new_entry no es None, se agrega antes de dividir."""
        if new_entry is not None:
            all_entries = node.entries + [new_entry]
        else:
            all_entries = node.entries

        # Ordenar por x mínimo (simple heurística)
        all_entries.sort(key=lambda x: x[0][0][0])
        mid = len(all_entries) // 2

        left_node = HRTreeNode(is_leaf=node.is_leaf, timestamp=self.current_time)
        right_node = HRTreeNode(is_leaf=node.is_leaf, timestamp=self.current_time)

        left_node.entries = all_entries[:mid]
        right_node.entries = all_entries[mid:]

        return left_node, right_node

    def _choose_subtree(self, node, mbr):
        """Elige la mejor rama para insertar el MBR."""
        best_choice = None
        min_increase = float('inf')

        for entry_mbr, child in node.entries:
            current_area = self._calculate_area(entry_mbr)
            enlarged_mbr = self._enlarge_mbr(entry_mbr, mbr)
            enlarged_area = self._calculate_area(enlarged_mbr)
            increase = enlarged_area - current_area

            if increase < min_increase:
                min_increase = increase
                best_choice = child

        return best_choice

    def _update_entry(self, parent, old_child, new_child):
        """Actualiza la entrada de un nodo padre con un nuevo hijo."""
        for i, (mbr, child) in enumerate(parent.entries):
            if child == old_child:
                parent.entries[i] = (self._calculate_mbr(new_child.entries), new_child)
                break

    def _mbr_overlap(self, mbr1, mbr2):
        """Comprueba si dos MBRs se superponen."""
        return not (
            mbr1[1][0] < mbr2[0][0] or  # Derecha de mbr1 a izquierda de mbr2
            mbr1[0][0] > mbr2[1][0] or  # Izquierda de mbr1 a derecha de mbr2
            mbr1[1][1] < mbr2[0][1] or  # Arriba de mbr1 debajo de mbr2
            mbr1[0][1] > mbr2[1][1]    # Abajo de mbr1 encima de mbr2
        )

    def _calculate_area(self, mbr):
        """Calcula el área de un MBR."""
        return (mbr[1][0] - mbr[0][0]) * (mbr[1][1] - mbr[0][1])

    def _enlarge_mbr(self, mbr1, mbr2):
        """Calcula un MBR ampliado que contiene a ambos MBRs."""
        return (
            (min(mbr1[0][0], mbr2[0][0]), min(mbr1[0][1], mbr2[0][1])),
            (max(mbr1[1][0], mbr2[1][0]), max(mbr1[1][1], mbr2[1][1]))
        )

    def _calculate_mbr(self, entries):
        """Calcula el MBR que cubre todas las entradas."""
        min_x = min(entry[0][0][0] for entry in entries)
        min_y = min(entry[0][0][1] for entry in entries)
        max_x = max(entry[0][1][0] for entry in entries)
        max_y = max(entry[0][1][1] for entry in entries)
        return ((min_x, min_y), (max_x, max_y))

class HRTreeFullVisualizer:
    def __init__(self, hr_tree):
        self.hr_tree = hr_tree

    def draw_tree(self, version=None):
        if version is None:
            version = self.hr_tree.current_time
        
        if version >= len(self.hr_tree.history) or version < 0:
            raise ValueError(f"La version {version} no existe.")

        G = nx.DiGraph()
        root = self.hr_tree.history[version]
        self._add_nodes_edges(G, root, f"Root_V{version}")

        # Dibujar el grafo
        plt.figure(figsize=(10, 6))
        try:
            pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
        except ImportError:
            pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightgray", 
                font_size=10, font_weight="bold")
        plt.title(f"HR-Tree - Version V{version}")
        plt.show()
    
    def draw_full_history(self):
        G = nx.DiGraph()
        root_global_label = "global_root"
        G.add_node(root_global_label, color="lightgray")

        # Iterar sobre cada versión y añadir sus raíces
        for version, root in enumerate(self.hr_tree.history):
            root_label = f"Root_V{version}"
            G.add_node(root_label, color="lightgray")
            G.add_edge(root_global_label, root_label, label=f"T{version}")
            self._add_nodes_edges(G, root, root_label)

        # Dibujar el grafo
        plt.figure(figsize=(12, 8))
        try:
            pos = nx.drawing.nx_pydot.graphviz_layout(G, prog="dot")
        except ImportError:
            pos = nx.spring_layout(G)

        node_colors = [G.nodes[node].get('color', 'lightgray') for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000,
                font_size=8, font_weight="bold", edge_color="gray", arrows=True)
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title("Full HR-Tree History")
        plt.show()

    def _add_nodes_edges(self, G, node, parent_label):
        node_label = f"Node_{id(node)}_T{node.timestamp}"
        G.add_node(node_label)
        G.add_edge(parent_label, node_label)

        if node.is_leaf:
            for i, (mbr, _) in enumerate(node.entries):
                leaf_label = f"Leaf_{mbr[0]}-{mbr[1]}"
                G.add_node(leaf_label, color="lightgray")
                G.add_edge(node_label, leaf_label)
        else:
            for mbr, child in node.entries:
                self._add_nodes_edges(G, child, node_label)
    





tree = HRTree()
tree.create_new_version()
tree.insert(((0,0),(1,1)))
tree.insert(((2,2),(3,3)))
tree.insert(((4,4),(5,5)))
tree.insert(((6,6),(7,7)))
tree.insert(((8,8),(9,9)))  # Debería provocar división

# Consultar en la versión actual (tiempo actual):
print("Consulta:", tree.query(((0,0),(9,9))))  # Debería encontrar el MBR ((0,0),(1,1)) o cercanos
# Visualizar cada R tree por version
visualizer = HRTreeFullVisualizer(tree)
visualizer.draw_tree(version=0)
visualizer.draw_tree(version=1)
visualizer.draw_tree(version=2)

# Visualizar el historial completo del árbol
full_visualizer = HRTreeFullVisualizer(tree)
full_visualizer.draw_full_history()

