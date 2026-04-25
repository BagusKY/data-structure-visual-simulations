from core.priority_queue import PriorityQueue
from utils.helpers import generate_label


class HospitalSimulation:
    """
    Simulasi antrian rumah sakit (priority queue):
    - pasien datang dengan tingkat prioritas
    - prioritas kecil = lebih darurat
    - diproses satu per satu
    """

    def __init__(self):
        self.queue = PriorityQueue()

        self._counter = 0
        self.current_patient = None

    # =========================
    # PATIENT MANAGEMENT
    # =========================
    def add_patient(self, priority=None):
        """
        Tambah pasien
        priority:
            1 = darurat
            2 = sedang
            3 = ringan
        """
        if priority is None:
            priority = 3  # default ringan

        if priority <= 0:
            raise ValueError("Priority must be >= 1")

        label = generate_label(self._counter)
        self._counter += 1

        patient = {
            "id": label,
            "priority": priority
        }

        self.queue.enqueue(patient, priority)
        return patient

    # =========================
    # PROCESSING
    # =========================
    def process_next(self):
        """
        Ambil pasien berikutnya (berdasarkan prioritas)
        """
        if self.current_patient is not None:
            return None  # masih ada pasien diproses

        if self.queue.is_empty():
            return None

        self.current_patient = self.queue.dequeue()
        return self.current_patient

    def finish_current(self):
        """
        Selesaikan pasien saat ini
        """
        if self.current_patient is None:
            return None

        finished = self.current_patient
        self.current_patient = None
        return finished

    # =========================
    # STATE
    # =========================
    def get_queue(self):
        return self.queue.get_with_priority()

    def get_current(self):
        return self.current_patient

    def is_busy(self):
        return self.current_patient is not None

    def is_idle(self):
        return self.current_patient is None and self.queue.is_empty()

    def reset(self):
        self.queue.clear()
        self.current_patient = None
        self._counter = 0