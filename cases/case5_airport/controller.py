from cases.case5_airport.simulation import AirportSimulation
from cases.case5_airport.ui import AirportUI

from animations.movement import Movement
from animations.timing import Timing

from utils.helpers import safe_call


class AirportController:
    """
    Controller Airport:
    - tambah pesawat (landing/takeoff/emergency)
    - proses runway (priority)
    - animasi masuk & keluar
    """

    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back

        # =========================
        # CORE
        # =========================
        self.sim = AirportSimulation()

        # =========================
        # ANIMATION
        # =========================
        self.movement = Movement(root)

        # =========================
        # UI
        # =========================
        self.ui = AirportUI(
            root,
            on_add=self.handle_add,
            on_process=self.handle_process,
            on_finish=self.handle_finish,
            on_reset=self.handle_reset,
            on_back=self.handle_back
        )

        self.frame = self.ui.frame

        self.refresh_ui()

    # =========================
    # UI REFRESH
    # =========================
    def refresh_ui(self):
        self.ui.render_queue(self.sim.get_queue())
        self.ui.show_current(self.sim.get_current())

        if self.sim.is_idle():
            self.ui.set_status("Idle")
        elif self.sim.is_busy():
            self.ui.set_status("Runway busy")

    # =========================
    # HANDLERS
    # =========================
    def handle_add(self):
        plane_type, emergency = self.ui.get_input()

        ok, result = safe_call(self.sim.add_plane, plane_type, emergency)
        if not ok:
            self.ui.set_status(result)
            return

        self.refresh_ui()

        # animasi masuk dari kanan
        if self.ui.boxes:
            new_box = self.ui.boxes[-1]
            new_box.move(200, 0)

            self.movement.move_by(
                new_box,
                dx=-200,
                dy=0,
                duration=Timing.duration(Timing.FAST),
                easing="ease_out"
            )

    def handle_process(self):
        plane = self.sim.process_next()

        if plane is None:
            self.ui.set_status("No plane to process")
            return

        self.refresh_ui()

    def handle_finish(self):
        """
        Selesaikan pesawat di runway + animasi keluar
        """
        current_box = self.ui.current_box

        if current_box is None:
            self.ui.set_status("No active plane")
            return

        def after_out():
            current_box.delete()
            self.ui.current_box = None

            self.sim.finish_current()

            self.shift_queue_left()

        # animasi keluar ke kanan
        self.movement.move_by(
            current_box,
            dx=250,
            dy=0,
            duration=Timing.duration(Timing.MOVE),
            easing="ease_out",
            on_done=after_out
        )

    def shift_queue_left(self):
        boxes = self.ui.boxes

        if not boxes:
            self.refresh_ui()
            return

        gap = 80
        remaining = len(boxes)

        def one_done():
            nonlocal remaining
            remaining -= 1
            if remaining == 0:
                self.refresh_ui()

        for box in boxes:
            self.movement.move_by(
                box,
                dx=-gap,
                dy=0,
                duration=Timing.duration(Timing.FAST),
                easing="ease_in_out",
                on_done=one_done
            )

    def handle_reset(self):
        self.sim.reset()
        self.ui.clear()
        self.refresh_ui()

    def handle_back(self):
        self.ui.clear()
        self.on_back()