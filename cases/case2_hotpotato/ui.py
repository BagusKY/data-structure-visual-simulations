import tkinter as tk
from components.box import Box


class HotPotatoUI:
    """
    UI layer untuk Hot Potato:
    - render pemain (queue)
    - highlight rotasi & eliminasi (dipanggil controller)
    - input steps
    """

    def __init__(self, root, on_setup, on_play, on_reset, on_back):
        self.root = root

        # callbacks dari controller
        self.on_setup = on_setup
        self.on_play = on_play
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
            text="Case 2: Hot Potato (Queue)",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)

        # =========================
        # INPUT AREA
        # =========================
        input_frame = tk.Frame(self.frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Players (comma):").grid(row=0, column=0, padx=5)
        self.players_entry = tk.Entry(input_frame, width=40)
        self.players_entry.insert(0, "A,B,C,D,E")
        self.players_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Steps:").grid(row=1, column=0, padx=5)
        self.steps_entry = tk.Entry(input_frame, width=10)
        self.steps_entry.insert(0, "3")
        self.steps_entry.grid(row=1, column=1, sticky="w", padx=5)

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

        tk.Button(btn_frame, text="Setup", width=12, command=self.on_setup).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Play Round", width=12, command=self.on_play).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Reset", width=12, command=self.on_reset).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Back", width=12, command=self.on_back).grid(row=0, column=3, padx=5)

        # =========================
        # STATUS
        # =========================
        self.status_label = tk.Label(self.frame, text="Status: Ready", font=("Arial", 11))
        self.status_label.pack(pady=5)

        # =========================
        # STATE UI
        # =========================
        self.boxes = []            # pemain (queue)
        self.eliminated_boxes = []  # yang sudah keluar

    # =========================
    # INPUT
    # =========================
    def get_players_input(self):
        raw = self.players_entry.get()
        names = [x.strip() for x in raw.split(",") if x.strip()]
        return names

    def get_steps_input(self):
        try:
            return int(self.steps_entry.get())
        except:
            return 0

    # =========================
    # RENDER
    # =========================
    def render_players(self, players):
        # clear lama
        for b in self.boxes:
            b.delete()
        self.boxes.clear()

        start_x = 50
        y = 120
        gap = 80

        for i, name in enumerate(players):
            x = start_x + i * gap
            box = Box(self.canvas, x, y, text=name)
            self.boxes.append(box)

        if self.boxes:
            self.boxes[0].set_label("FRONT", "top")

    def render_eliminated(self, eliminated_list):
        # clear lama
        for b in self.eliminated_boxes:
            b.delete()
        self.eliminated_boxes.clear()

        start_x = 50
        y = 220
        gap = 60

        for i, name in enumerate(eliminated_list):
            x = start_x + i * gap
            box = Box(self.canvas, x, y, text=name, fill="#FF7F7F")
            self.eliminated_boxes.append(box)

    # =========================
    # VISUAL EFFECT
    # =========================
    def highlight_player(self, index, mode="current"):
        """
        mode:
        - current (kuning)
        - visited (biru)
        """
        if 0 <= index < len(self.boxes):
            self.boxes[index].highlight("#FFD700" if mode == "current" else "#87CEFA")

    def reset_highlight(self):
        for b in self.boxes:
            b.reset_style()

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

        for b in self.eliminated_boxes:
            b.delete()
        self.eliminated_boxes.clear()