import tkinter as tk

from components.box import Box


class PrinterUI:
    """
    UI layer untuk Printer Simulation
    - handle canvas & layout
    - render box queue
    - tidak tahu logic queue
    """

    def __init__(self, root, on_add, on_start, on_step, on_reset, on_back):
        self.root = root

        # CALLBACK (dari controller)
        self.on_add = on_add
        self.on_start = on_start
        self.on_step = on_step
        self.on_reset = on_reset
        self.on_back = on_back

        # FRAME UTAMA
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # =========================
        # TITLE
        # =========================
        title = tk.Label(
            self.frame,
            text="Case 1: Printer Queue",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # =========================
        # CANVAS
        # =========================
        self.canvas = tk.Canvas(self.frame, width=800, height=300, bg="white")
        self.canvas.pack(pady=10)

        # =========================
        # BUTTONS
        # =========================
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add Job", width=12, command=self.on_add).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Start", width=12, command=self.on_start).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Step", width=12, command=self.on_step).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Reset", width=12, command=self.on_reset).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Back", width=12, command=self.on_back).grid(row=0, column=4, padx=5)

        # =========================
        # STATUS
        # =========================
        self.status_label = tk.Label(self.frame, text="Status: Idle", font=("Arial", 11))
        self.status_label.pack(pady=5)

        # =========================
        # STATE UI
        # =========================
        self.boxes = []  # list Box (queue visual)
        self.current_box = None  # box yang sedang diproses

    # =========================
    # RENDER QUEUE
    # =========================
    def render_queue(self, jobs):
        """
        jobs: list of job dict dari simulation
        """
        # hapus box lama
        for box in self.boxes:
            box.delete()
        self.boxes.clear()

        start_x = 50
        y = 120
        gap = 80

        for i, job in enumerate(jobs):
            x = start_x + i * gap

            box = Box(self.canvas, x, y, text=job["id"])
            self.boxes.append(box)

        # label FRONT & REAR
        if self.boxes:
            self.boxes[0].set_label("FRONT", position="top")
            self.boxes[-1].set_label("REAR", position="bottom")

    # =========================
    # CURRENT JOB
    # =========================
    def show_current_job(self, job):
        """
        Tampilkan job yang sedang diproses
        """
        if self.current_box:
            self.current_box.delete()
            self.current_box = None

        if job is None:
            return

        self.current_box = Box(
            self.canvas,
            600,
            50,
            text=job["id"],
            fill="#FFD700"
        )

        self.current_box.set_label("PRINTING", position="bottom")

    # =========================
    # STATUS
    # =========================
    def set_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    # =========================
    # CLEANUP
    # =========================
    def clear(self):
        for box in self.boxes:
            box.delete()
        self.boxes.clear()

        if self.current_box:
            self.current_box.delete()
            self.current_box = None