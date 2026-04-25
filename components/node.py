import tkinter as tk


class Node:
    """
    Representasi node graph:
    - lingkaran + teks
    - bisa di-highlight (visited/current)
    - aware terhadap edge (garis ikut bergerak saat node pindah)
    """

    def __init__(
        self,
        canvas: tk.Canvas,
        x: int,
        y: int,
        radius: int = 25,
        text: str = "",
        fill: str = "#90EE90",
        outline: str = "#333333",
        text_color: str = "#000000",
    ):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = radius

        self._visible = True
        self._edges = []  # list of edge ids (line) yang terhubung

        # circle
        self.oval_id = canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=fill,
            outline=outline,
            width=2
        )

        # text (center)
        self.text_id = canvas.create_text(
            x, y,
            text=text,
            fill=text_color,
            font=("Arial", 11, "bold")
        )

    # =========================
    # POSITION
    # =========================
    def move(self, dx: float, dy: float):
        """Geser relatif + update semua edge"""
        self.canvas.move(self.oval_id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)

        self.x += dx
        self.y += dy

        # update semua edge yang terhubung
        for edge in self._edges:
            self._update_edge_coords(edge)

    def move_to(self, x: float, y: float):
        dx = x - self.x
        dy = y - self.y
        self.move(dx, dy)

    def coords(self):
        return (self.x, self.y)

    # =========================
    # TEXT
    # =========================
    def set_text(self, text: str):
        self.canvas.itemconfig(self.text_id, text=text)

    def get_text(self):
        return self.canvas.itemcget(self.text_id, "text")

    # =========================
    # STYLE / STATE
    # =========================
    def set_fill(self, color: str):
        self.canvas.itemconfig(self.oval_id, fill=color)

    def set_outline(self, color: str):
        self.canvas.itemconfig(self.oval_id, outline=color)

    def highlight(self, mode: str):
        """
        mode:
        - 'default'
        - 'visited'
        - 'current'
        """
        if mode == "visited":
            self.set_fill("#87CEFA")   # biru
        elif mode == "current":
            self.set_fill("#FFD700")   # kuning
        else:
            self.set_fill("#90EE90")   # hijau default

    # =========================
    # VISIBILITY
    # =========================
    def hide(self):
        if not self._visible:
            return
        self.canvas.itemconfigure(self.oval_id, state="hidden")
        self.canvas.itemconfigure(self.text_id, state="hidden")
        for edge in self._edges:
            self.canvas.itemconfigure(edge, state="hidden")
        self._visible = False

    def show(self):
        if self._visible:
            return
        self.canvas.itemconfigure(self.oval_id, state="normal")
        self.canvas.itemconfigure(self.text_id, state="normal")
        for edge in self._edges:
            self.canvas.itemconfigure(edge, state="normal")
        self._visible = True

    def delete(self):
        self.canvas.delete(self.oval_id)
        self.canvas.delete(self.text_id)
        for edge in self._edges:
            self.canvas.delete(edge)

    # =========================
    # EDGE MANAGEMENT
    # =========================
    def connect_to(self, other_node, color="#000000", width=2):
        """
        Buat edge (garis) antara node ini dan node lain
        """
        line = self.canvas.create_line(
            self.x, self.y,
            other_node.x, other_node.y,
            fill=color,
            width=width
        )

        # simpan di kedua node
        self._edges.append((line, other_node))
        other_node._edges.append((line, self))

        return line

    def _update_edge_coords(self, edge_tuple):
        """
        Update posisi garis saat node bergerak
        """
        line_id, other = edge_tuple
        self.canvas.coords(
            line_id,
            self.x, self.y,
            other.x, other.y
        )