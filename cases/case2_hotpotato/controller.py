from cases.case2_hotpotato.simulation import HotPotatoSimulation
from cases.case2_hotpotato.ui import HotPotatoUI

from animations.movement import Movement
from animations.timing import Timing

from utils.helpers import safe_call


class HotPotatoController:
    """
    Controller Hot Potato:
    - handle setup pemain
    - jalankan 1 ronde (rotasi + eliminasi)
    - animasi highlight rotasi
    """

    def __init__(self, root, on_back):
        self.root = root
        self.on_back = on_back

        # =========================
        # CORE
        # =========================
        self.sim = HotPotatoSimulation()

        # =========================
        # ANIMATION
        # =========================
        self.movement = Movement(root)

        # =========================
        # UI
        # =========================
        self.ui = HotPotatoUI(
            root,
            on_setup=self.handle_setup,
            on_play=self.handle_play,
            on_reset=self.handle_reset,
            on_back=self.handle_back
        )

        self.frame = self.ui.frame

        # state bantu animasi
        self._rotation_steps = []
        self._step_index = 0

    # =========================
    # SETUP
    # =========================
    def handle_setup(self):
        names = self.ui.get_players_input()

        ok, err = safe_call(self.sim.set_players, names)
        if not ok:
            self.ui.set_status(err)
            return

        self.ui.render_players(self.sim.get_players())
        self.ui.render_eliminated(self.sim.get_eliminated())
        self.ui.set_status("Players ready")

    # =========================
    # PLAY ROUND
    # =========================
    def handle_play(self):
        if self.sim.is_finished():
            winner = self.sim.get_winner()
            if winner:
                self.ui.set_status(f"Winner: {winner}")
            return

        steps = self.ui.get_steps_input()
        if steps <= 0:
            self.ui.set_status("Steps must be > 0")
            return

        result = self.sim.play_round(steps)
        if result is None:
            return

        self._rotation_steps = result["rotations"]
        self._step_index = 0

        # mulai animasi rotasi
        self.animate_rotation(result)

    # =========================
    # ROTATION ANIMATION
    # =========================
    def animate_rotation(self, result):
        """
        Highlight pemain satu per satu (simulasi passing)
        """

        boxes = self.ui.boxes

        if not boxes:
            self.finish_round(result)
            return

        def step():
            if self._step_index >= len(self._rotation_steps):
                self.finish_round(result)
                return

            # reset semua highlight
            self.ui.reset_highlight()

            # index pemain sekarang (selalu index 0 karena queue berputar secara logika)
            idx = self._step_index % len(boxes)

            self.ui.highlight_player(idx, mode="current")

            self._step_index += 1

            self.root.after(
                Timing.duration(Timing.SHORT_DELAY),
                step
            )

        step()

    # =========================
    # FINISH ROUND
    # =========================
    def finish_round(self, result):
        """
        Setelah rotasi selesai → eliminasi
        """

        eliminated = result["eliminated"]

        self.ui.set_status(f"Eliminated: {eliminated}")

        # update UI (tanpa animasi kompleks, tetap konsisten)
        self.ui.render_players(result["remaining"])
        self.ui.render_eliminated(self.sim.get_eliminated())

        # cek winner
        if self.sim.is_finished():
            winner = self.sim.get_winner()
            if winner:
                self.ui.set_status(f"Winner: {winner}")

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