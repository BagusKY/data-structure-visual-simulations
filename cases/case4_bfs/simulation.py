from core.graph import Graph


class BFSSimulation:
    """
    Simulasi BFS:
    - graph berbasis adjacency list
    - traversal dari node awal
    - menghasilkan langkah (steps) untuk animasi
    """

    def __init__(self):
        self.graph = Graph(directed=False)

        self.start_node = None
        self.steps = []
        self._step_index = 0

    # =========================
    # SETUP GRAPH
    # =========================
    def set_graph(self, edges):
        """
        edges: list of tuple
        contoh: [("A","B"), ("A","C"), ("B","D")]
        """
        self.graph.clear()

        for u, v in edges:
            self.graph.add_edge(u, v)

        self.start_node = None
        self.steps.clear()
        self._step_index = 0

    def set_start(self, node):
        if not self.graph.has_node(node):
            raise ValueError("Start node not found")

        self.start_node = node
        self.steps = self.graph.bfs_steps(node)
        self._step_index = 0

    # =========================
    # STEP CONTROL
    # =========================
    def has_next(self):
        return self._step_index < len(self.steps)

    def next_step(self):
        """
        Ambil langkah BFS berikutnya
        """
        if not self.has_next():
            return None

        step = self.steps[self._step_index]
        self._step_index += 1
        return step

    def reset(self):
        self.steps.clear()
        self._step_index = 0
        self.start_node = None

    # =========================
    # STATE
    # =========================
    def get_graph(self):
        return self.graph.get_all()

    def get_nodes(self):
        return self.graph.get_nodes()

    def get_start(self):
        return self.start_node

    def is_finished(self):
        return self._step_index >= len(self.steps)