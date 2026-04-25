from core.priority_queue import PriorityQueue
from utils.helpers import generate_label


class AirportSimulation:
    """
    Simulasi bandara (runway scheduling):
    - pesawat landing / takeoff
    - emergency punya prioritas lebih tinggi
    - runway hanya 1 (diproses satu per satu)
    """

    def __init__(self):
        self.queue = PriorityQueue()

        self._counter = 0
        self.current_plane = None

    # =========================
    # ADD PLANE
    # =========================
    def add_plane(self, plane_type="landing", emergency=False):
        """
        plane_type: "landing" / "takeoff"
        emergency: True / False
        """

        label = generate_label(self._counter)
        self._counter += 1

        # priority rules:
        # emergency landing = 1 (highest)
        # landing = 2
        # takeoff = 3
        if emergency:
            priority = 1
        elif plane_type == "landing":
            priority = 2
        else:
            priority = 3

        plane = {
            "id": label,
            "type": plane_type,
            "emergency": emergency,
            "priority": priority
        }

        self.queue.enqueue(plane, priority)
        return plane

    # =========================
    # PROCESS
    # =========================
    def process_next(self):
        """
        Ambil pesawat berikutnya
        """
        if self.current_plane is not None:
            return None

        if self.queue.is_empty():
            return None

        self.current_plane = self.queue.dequeue()
        return self.current_plane

    def finish_current(self):
        """
        Selesaikan pesawat di runway
        """
        if self.current_plane is None:
            return None

        finished = self.current_plane
        self.current_plane = None
        return finished

    # =========================
    # STATE
    # =========================
    def get_queue(self):
        return self.queue.get_with_priority()

    def get_current(self):
        return self.current_plane

    def is_busy(self):
        return self.current_plane is not None

    def is_idle(self):
        return self.current_plane is None and self.queue.is_empty()

    def reset(self):
        self.queue.clear()
        self.current_plane = None
        self._counter = 0