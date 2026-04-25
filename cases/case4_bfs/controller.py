from cases.case4_bfs.simulation import BFSSimulation
from cases.case4_bfs.ui import BFSUI

from utils.helpers import safe_call


class BFSController:
    """
    Controller BFS:
    - build graph dari input
    - set start node
    - jalankan BFS step-by-step
    """

    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back

        # =========================
        # CORE
        # =========================
        self.sim = BFSSimulation()

        # =========================
        # UI
        # =========================
        self.ui = BFSUI(
            root,
            on_build=self.handle_build,
            on_start=self.handle_start,
            on_step=self.handle_step,
            on_reset=self.handle_reset,
            on_back=self.handle_back
        )

        self.frame = self.ui.frame

    # =========================
    # BUILD GRAPH
    # =========================
    def handle_build(self):
        edges = self.ui.get_edges_input()

        ok, err = safe_call(self.sim.set_graph, edges)
        if not ok:
            self.ui.set_status(err)
            return

        self.ui.render_graph(self.sim.get_graph())
        self.ui.set_status("Graph built")

    # =========================
    # START BFS
    # =========================
    def handle_start(self):
        start = self.ui.get_start_input()

        ok, err = safe_call(self.sim.set_start, start)
        if not ok:
            self.ui.set_status(err)
            return

        self.ui.set_status(f"Start from {start}")

    # =========================
    # STEP BFS
    # =========================
    def handle_step(self):
        if self.sim.is_finished():
            self.ui.set_status("Traversal finished")
            return

        step = self.sim.next_step()

        if step is None:
            return

        # highlight node
        self.ui.highlight_step(step)

        # tampilkan info queue (opsional di status)
        queue_info = ", ".join(step["queue"])
        self.ui.set_status(f"Current: {step['current']} | Queue: [{queue_info}]")

    # =========================
    # RESET / BACK
    # =========================
    def handle_reset(self):
        self.sim.reset()
        self.ui.clear()
        self.ui.set_status("Reset")

    def handle_back(self):
        self.ui.clear()
        self.on_back()