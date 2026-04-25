from core.queue import Queue
from utils.helpers import generate_label


class PrinterSimulation:
    """
    Simulasi antrian printer:
    - dokumen masuk (enqueue)
    - dokumen diproses satu per satu (dequeue)
    - tiap dokumen punya waktu cetak (duration)
    """

    def __init__(self, capacity=5):
        self.queue = Queue(capacity=capacity)

        self._counter = 0          # untuk label (A, B, C, ...)
        self.current_job = None    # job yang sedang diproses
        self.time_remaining = 0    # sisa waktu job aktif

    # =========================
    # JOB MANAGEMENT
    # =========================
    def add_job(self, pages=None):
        """
        Tambah job ke queue
        pages: jumlah halaman (opsional)
        """
        label = generate_label(self._counter)
        self._counter += 1

        job = {
            "id": label,
            "pages": pages if pages is not None else 1,
            "duration": self._calc_duration(pages if pages else 1)
        }

        self.queue.enqueue(job)
        return job

    def _calc_duration(self, pages):
        """
        Hitung waktu cetak berdasarkan jumlah halaman
        (simulasi sederhana)
        """
        base_time = 1.0   # detik per halaman (logika, bukan delay UI)
        return pages * base_time

    # =========================
    # PROCESSING
    # =========================
    def start_next_job(self):
        """
        Ambil job berikutnya dari queue
        """
        if self.current_job is not None:
            return None  # masih ada job berjalan

        if self.queue.is_empty():
            return None

        self.current_job = self.queue.dequeue()
        self.time_remaining = self.current_job["duration"]

        return self.current_job

    def step(self, delta=1.0):
        """
        Simulasi waktu berjalan
        delta = waktu yang berlalu (detik)
        """
        if self.current_job is None:
            return None

        self.time_remaining -= delta

        if self.time_remaining <= 0:
            finished = self.current_job
            self.current_job = None
            self.time_remaining = 0
            return finished  # job selesai

        return None  # belum selesai

    # =========================
    # STATE ACCESS
    # =========================
    def get_queue(self):
        """
        Return list job dalam queue (tanpa yang sedang diproses)
        """
        return self.queue.get_all()

    def get_current_job(self):
        return self.current_job

    def is_busy(self):
        return self.current_job is not None

    def is_idle(self):
        return self.current_job is None and self.queue.is_empty()

    def reset(self):
        self.queue.clear()
        self.current_job = None
        self.time_remaining = 0
        self._counter = 0