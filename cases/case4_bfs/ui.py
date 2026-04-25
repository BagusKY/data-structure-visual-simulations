import tkinter as tk
from components.node import Node


class BFSUI:
    """
    UI untuk BFS Graph:
    - render node & edge
    - highlight traversal (current / visited)
    """

    def __init__(self, root, on_build, on_start, on_step, on_reset, on_back):
        self.root = root

        # callbacks
        self.on_build = on_build
        self.on_start = on_start
        self.on_step = on_step
        self.on_reset = on_reset
        self.on_back = on_back

        # frame
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # =========================
        # TITLE
        # =========================
        title = tk.Label(
            self.frame,
            text="Case 4: BFS Graph",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # =========================
        # INPUT
        # =========================
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Edges (A-B, A-C):").grid(row=0, column=0, padx=5)
        self.edges_entry = tk.Entry(input_frame, width=40)
        self.edges_entry.insert(0, "A-B, A-C, B-D, C-E")
        self.edges_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Start Node:").grid(row=1, column=0, padx=5)
        self.start_entry = tk.Entry(input_frame, width=10)
        self.start_entry.insert(0, "A")
        self.start_entry.grid(row=1, column=1, sticky="w", padx=5)

        # =========================
        # CANVAS
        # =========================
        self.canvas = tk.Canvas(self.frame, width=800, height=400, bg="white")
        self.canvas.pack(pady=10)

        # =========================
        # BUTTONS
        # =========================
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Build Graph", width=14, command=self.on_build).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Start BFS", width=14, command=self.on_start).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Next Step", width=14, command=self.on_step).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Reset", width=14, command=self.on_reset).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Back", width=14, command=self.on_back).grid(row=0, column=4, padx=5)

        # =========================
        # STATUS
        # =========================
        self.status_label = tk.Label(self.frame, text="Status: Ready", font=("Arial", 11))
        self.status_label.pack(pady=5)

        # =========================
        # STATE
        # =========================
        self.nodes = {}  # name -> Node

    # =========================
    # INPUT PARSER
    # =========================
    def get_edges_input(self):
        raw = self.edges_entry.get()
        edges = []

        for part in raw.split(","):
            part = part.strip()
            if "-" in part:
                u, v = part.split("-")
                edges.append((u.strip(), v.strip()))

        return edges

    def get_start_input(self):
        return self.start_entry.get().strip()

    # =========================
    # RENDER GRAPH
    # =========================
    def render_graph(self, adjacency):
        """
        adjacency: {node: [neighbors]}
        """
        # clear lama
        self.clear()

        # posisi sederhana (grid / manual layout)
        positions = self._generate_positions(list(adjacency.keys()))

        # buat node dulu
        for name, (x, y) in positions.items():
            self.nodes[name] = Node(self.canvas, x, y, text=name)

        # buat edge
        for u, neighbors in adjacency.items():
            for v in neighbors:
                if u < v:  # hindari double line
                    self.nodes[u].connect_to(self.nodes[v])

    def _generate_positions(self, nodes):
        """
        Layout sederhana (grid)
        """
        positions = {}
        cols = 4
        gap_x = 150
        gap_y = 120

        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols

            x = 100 + col * gap_x
            y = 100 + row * gap_y

            positions[node] = (x, y)

        return positions

    # =========================
    # HIGHLIGHT
    # =========================
    def highlight_step(self, step):
        """
        step = {
            current,
            queue,
            visited
        }
        """
        # reset semua
        for node in self.nodes.values():
            node.highlight("default")

        # visited
        for v in step["visited"]:
            if v in self.nodes:
                self.nodes[v].highlight("visited")

        # current
        cur = step["current"]
        if cur in self.nodes:
            self.nodes[cur].highlight("current")

    # =========================
    # STATUS
    # =========================
    def set_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    # =========================
    # CLEANUP
    # =========================
    def clear(self):
        for node in self.nodes.values():
            node.delete()
        self.nodes.clear()