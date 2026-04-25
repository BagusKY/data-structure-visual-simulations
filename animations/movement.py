import math


class Movement:
    """
    Engine animasi berbasis tkinter.after
    - move_to: geser ke posisi target (smooth)
    - move_by: geser relatif (smooth)
    - sequence: jalankan beberapa animasi berurutan
    """

    def __init__(self, root, fps=60):
        self.root = root
        self.fps = fps
        self._frame_delay = int(1000 / fps)

    # =========================
    # CORE ANIMATION
    # =========================
    def move_to(self, obj, target_x, target_y, duration=400, easing="linear", on_done=None):
        """
        Animasi ke posisi absolut
        obj harus punya:
            - move(dx, dy)
            - x, y
        """
        start_x, start_y = obj.x, obj.y
        dx = target_x - start_x
        dy = target_y - start_y

        self._animate(
            obj=obj,
            dx=dx,
            dy=dy,
            duration=duration,
            easing=easing,
            on_done=on_done
        )

    def move_by(self, obj, dx, dy, duration=400, easing="linear", on_done=None):
        """
        Animasi relatif
        """
        self._animate(
            obj=obj,
            dx=dx,
            dy=dy,
            duration=duration,
            easing=easing,
            on_done=on_done
        )

    # =========================
    # INTERNAL ENGINE
    # =========================
    def _animate(self, obj, dx, dy, duration, easing, on_done):
        frames = max(1, int(self.fps * (duration / 1000)))

        # incremental per frame
        step_dx = dx / frames
        step_dy = dy / frames

        current_frame = 0

        def step():
            nonlocal current_frame

            t = current_frame / frames
            factor = self._ease(t, easing)

            # delta berbasis easing
            obj.move(step_dx * factor, step_dy * factor)

            current_frame += 1

            if current_frame <= frames:
                self.root.after(self._frame_delay, step)
            else:
                # pastikan tepat di posisi akhir
                obj.move(dx - step_dx * frames, dy - step_dy * frames)

                if on_done:
                    on_done()

        step()

    # =========================
    # EASING FUNCTIONS
    # =========================
    def _ease(self, t, mode):
        if mode == "ease_in":
            return t * t
        elif mode == "ease_out":
            return 1 - (1 - t) * (1 - t)
        elif mode == "ease_in_out":
            return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
        else:
            return 1  # linear

    # =========================
    # SEQUENCE (CHAIN ANIMATION)
    # =========================
    def sequence(self, actions):
        """
        Jalankan animasi berurutan

        actions = [
            lambda done: self.move_to(obj, x, y, on_done=done),
            lambda done: self.move_by(obj, dx, dy, on_done=done),
        ]
        """

        def run(index):
            if index >= len(actions):
                return

            def next_step():
                run(index + 1)

            actions[index](next_step)

        run(0)