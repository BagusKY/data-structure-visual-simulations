import tkinter as tk
from components.box import Box


class AirportUI:
    """
    UI Airport:
    - render queue pesawat
    - tampilkan runway (current plane)
    - warna berdasarkan tipe & emergency
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
            text="Case 5: Airport Runway Scheduling",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # =========================
        # INPUT
        # =========================
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Type:").grid(row=0, column=0, padx=5)

        self.type_var = tk.StringVar(value="landing")
        tk.OptionMenu(input_frame, self.type_var, "landing", "takeoff").grid(row=0, column=1, padx=5)

        self.emergency_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Emergency", variable=self.emergency_var).grid(row=0, column=2, padx=5)

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

        tk.Button(btn_frame, text="Add Plane", width=14, command=self.on_add).grid(row=0, column=0, padx=5)
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
    def get_input(self):
        return self.type_var.get(), self.emergency_var.get()

    # =========================
    # COLOR LOGIC
    # =========================
    def get_color(self, plane):
        if plane["emergency"]:
            return "#FF4D4D"  # merah (emergency)
        elif plane["type"] == "landing":
            return "#FFD93D"  # kuning
        else:
            return "#6BCB77"  # hijau

    # =========================
    # RENDER QUEUE
    # =========================
    def render_queue(self, planes):
        """
        planes: [(plane_dict, priority)]
        """
        # clear lama
        for b in self.boxes:
            b.delete()
        self.boxes.clear()

        start_x = 50
        y = 140
        gap = 80

        for i, (plane, priority) in enumerate(planes):
            x = start_x + i * gap
            color = self.get_color(plane)

            label = f"{plane['id']}"

            box = Box(self.canvas, x, y, text=label, fill=color)
            self.boxes.append(box)

        if self.boxes:
            self.boxes[0].set_label("NEXT", "top")

    # =========================
    # RUNWAY (CURRENT)
    # =========================
    def show_current(self, plane):
        if self.current_box:
            self.current_box.delete()
            self.current_box = None

        if plane is None:
            return

        color = self.get_color(plane)

        self.current_box = Box(
            self.canvas,
            600,
            60,
            text=plane["id"],
            fill=color
        )

        self.current_box.set_label("RUNWAY", "bottom")

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