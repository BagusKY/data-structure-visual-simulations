import tkinter as tk
from components.box import Box


class HospitalUI:
    """
    UI untuk Hospital Priority Queue
    - render pasien (dengan warna prioritas)
    - tampilkan pasien yang sedang diproses
    """

    def __init__(self, root, on_add, on_process, on_finish, on_reset, on_back):
        self.root = root

        # callbacks
        self.on_add = on_add
        self.on_process = on_process
        self.on_finish = on_finish
        self.on_reset = on_reset
        self.on_back = on_back

        # frame utama
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        # =========================
        # TITLE
        # =========================
        title = tk.Label(
            self.frame,
            text="Case 3: Hospital (Priority Queue)",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # =========================
        # INPUT PRIORITY
        # =========================
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Priority (1=High, 3=Low):").grid(row=0, column=0, padx=5)
        self.priority_entry = tk.Entry(input_frame, width=10)
        self.priority_entry.insert(0, "3")
        self.priority_entry.grid(row=0, column=1, padx=5)

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

        tk.Button(btn_frame, text="Add Patient", width=14, command=self.on_add).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Process", width=14, command=self.on_process).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Finish", width=14, command=self.on_finish).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Reset", width=14, command=self.on_reset).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Back", width=14, command=self.on_back).grid(row=0, column=4, padx=5)

        # =========================
        # STATUS
        # =========================
        self.status_label = tk.Label(self.frame, text="Status: Ready", font=("Arial", 11))
        self.status_label.pack(pady=5)

        # =========================
        # STATE UI
        # =========================
        self.boxes = []
        self.current_box = None

    # =========================
    # INPUT
    # =========================
    def get_priority_input(self):
        try:
            value = int(self.priority_entry.get())
            return value
        except:
            return 3

    # =========================
    # COLOR MAPPING
    # =========================
    def get_color_by_priority(self, priority):
        if priority == 1:
            return "#FF6B6B"  # merah (darurat)
        elif priority == 2:
            return "#FFD93D"  # kuning (sedang)
        else:
            return "#6BCB77"  # hijau (ringan)

    # =========================
    # RENDER QUEUE
    # =========================
    def render_queue(self, patients):
        """
        patients: [(patient_dict, priority), ...]
        """
        # clear lama
        for b in self.boxes:
            b.delete()
        self.boxes.clear()

        start_x = 50
        y = 120
        gap = 80

        for i, (patient, priority) in enumerate(patients):
            x = start_x + i * gap
            color = self.get_color_by_priority(priority)

            box = Box(self.canvas, x, y, text=patient["id"], fill=color)
            self.boxes.append(box)

        if self.boxes:
            self.boxes[0].set_label("NEXT", "top")

    # =========================
    # CURRENT PATIENT
    # =========================
    def show_current(self, patient):
        if self.current_box:
            self.current_box.delete()
            self.current_box = None

        if patient is None:
            return

        color = self.get_color_by_priority(patient["priority"])

        self.current_box = Box(
            self.canvas,
            600,
            50,
            text=patient["id"],
            fill=color
        )

        self.current_box.set_label("TREATING", "bottom")

    # =========================
    # STATUS
    # =========================
    def set_status(self, text):
        self.status_label.config(text=f"Status: {text}")

    # =========================
    # CLEANUP
    # =========================
    def clear(self):
        for b in self.boxes:
            b.delete()
        self.boxes.clear()

        if self.current_box:
            self.current_box.delete()
            self.current_box = None