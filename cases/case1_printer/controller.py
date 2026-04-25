from cases.case1_printer.simulation import PrinterSimulation
from cases.case1_printer.ui import PrinterUI

from animations.movement import Movement
from animations.timing import Timing

from utils.helpers import safe_call


class PrinterController:
    """
    Controller:
    - penghubung UI ↔ Simulation
    - handle animasi
    - handle event tombol
    """

    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back

        # =========================
        # CORE
        # =========================
        self.sim = PrinterSimulation(capacity=5)

        # =========================
        # ANIMATION
        # =========================
        self.movement = Movement(root)

        # =========================
        # UI
        # =========================
        self.ui = PrinterUI(
            root,
            on_add=self.handle_add,
            on_start=self.handle_start,
            on_step=self.handle_step,
            on_reset=self.handle_reset,
            on_back=self.handle_back
        )

        self.frame = self.ui.frame

        # initial render
        self.refresh_ui()

    # =========================
    # UI REFRESH
    # =========================
    def refresh_ui(self):
        self.ui.render_queue(self.sim.get_queue())
        self.ui.show_current_job(self.sim.get_current_job())

        if self.sim.is_idle():
            self.ui.set_status("Idle")
        elif self.sim.is_busy():
            self.ui.set_status("Printing...")

    # =========================
    # HANDLERS
    # =========================
    def handle_add(self):
        ok, result = safe_call(self.sim.add_job)

        if not ok:
            self.ui.set_status(result)
            return

        self.refresh_ui()

    def handle_start(self):
        job = self.sim.start_next_job()

        if job is None:
            self.ui.set_status("No job to start")
            return

        self.refresh_ui()

    def handle_step(self):
        """
        Jalankan 1 langkah waktu + animasi
        """
        finished = self.sim.step()

        if finished:
            # animasi selesai cetak
            self.animate_finish_job()
        else:
            self.refresh_ui()

    def handle_reset(self):
        self.sim.reset()
        self.ui.clear()
        self.refresh_ui()

    def handle_back(self):
        self.ui.clear()
        self.on_back()

    # =========================
    # ANIMATION LOGIC
    # =========================
    def animate_finish_job(self):
        """
        Animasi saat job selesai:
        - box current keluar
        - queue geser kiri
        """

        current_box = self.ui.current_box

        if current_box is None:
            self.refresh_ui()
            return

        # STEP 1: box keluar ke kanan
        def after_move_out():
            current_box.delete()
            self.ui.current_box = None

            # STEP 2: geser semua box ke kiri
            self.shift_queue_left()

        self.movement.move_by(
            current_box,
            dx=200,
            dy=0,
            duration=Timing.duration(Timing.MOVE),
            easing="ease_out",
            on_done=after_move_out
        )

    def shift_queue_left(self):
        """
        Geser semua box ke kiri setelah dequeue
        """
        boxes = self.ui.boxes

        if not boxes:
            self.refresh_ui()
            return

        gap = 80

        def after_shift():
            self.refresh_ui()

        # animasi semua box
        remaining = len(boxes)

        def one_done():
            nonlocal remaining
            remaining -= 1
            if remaining == 0:
                after_shift()

        for box in boxes:
            self.movement.move_by(
                box,
                dx=-gap,
                dy=0,
                duration=Timing.duration(Timing.FAST),
                easing="ease_in_out",
                on_done=one_done
            )