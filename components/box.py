import tkinter as tk


class Box:
    """
    Representasi 1 elemen visual (kotak + teks + label opsional)
    - Reusable untuk queue / stack / priority queue
    - Tidak tahu apa-apa soal struktur data (murni visual)
    """

    def __init__(
        self,
        canvas: tk.Canvas,
        x: int,
        y: int,
        width: int = 60,
        height: int = 60,
        text: str = "",
        fill: str = "#ADD8E6",
        outline: str = "#333333",
        text_color: str = "#000000",
    ):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.w = width
        self.h = height

        # state
        self._visible = True
        self._label_id = None

        # draw rectangle
        self.rect_id = canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=fill,
            outline=outline,
            width=2
        )

        # draw text (centered)
        self.text_id = canvas.create_text(
            x + width / 2,
            y + height / 2,
            text=text,
            fill=text_color,
            font=("Arial", 12, "bold")
        )

    # =========================
    # POSITION
    # =========================
    def move(self, dx: float, dy: float):
        """Geser relatif"""
        self.canvas.move(self.rect_id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)
        if self._label_id:
            self.canvas.move(self._label_id, dx, dy)

        self.x += dx
        self.y += dy

    def move_to(self, x: float, y: float):
        """Pindah ke posisi absolut (tanpa animasi)"""
        dx = x - self.x
        dy = y - self.y
        self.move(dx, dy)

    def coords(self):
        """Ambil koordinat sekarang"""
        return (self.x, self.y, self.x + self.w, self.y + self.h)

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
        self.canvas.itemconfig(self.rect_id, fill=color)

    def set_outline(self, color: str):
        self.canvas.itemconfig(self.rect_id, outline=color)

    def highlight(self, color: str = "#FFD700"):
        """Tandai (misal current / selected)"""
        self.set_outline(color)

    def reset_style(self):
        self.set_outline("#333333")

    # =========================
    # VISIBILITY
    # =========================
    def hide(self):
        if not self._visible:
            return
        self.canvas.itemconfigure(self.rect_id, state="hidden")
        self.canvas.itemconfigure(self.text_id, state="hidden")
        if self._label_id:
            self.canvas.itemconfigure(self._label_id, state="hidden")
        self._visible = False

    def show(self):
        if self._visible:
            return
        self.canvas.itemconfigure(self.rect_id, state="normal")
        self.canvas.itemconfigure(self.text_id, state="normal")
        if self._label_id:
            self.canvas.itemconfigure(self._label_id, state="normal")
        self._visible = True

    def delete(self):
        """Hapus permanen dari canvas"""
        self.canvas.delete(self.rect_id)
        self.canvas.delete(self.text_id)
        if self._label_id:
            self.canvas.delete(self._label_id)

    # =========================
    # LABEL (FRONT / REAR / dll)
    # =========================
    def set_label(self, text: str, position: str = "top"):
        """
        Tambah / update label kecil (misal FRONT/REAR)
        position: 'top' | 'bottom'
        """
        # hitung posisi label
        if position == "top":
            lx = self.x + self.w / 2
            ly = self.y - 10
        else:  # bottom
            lx = self.x + self.w / 2
            ly = self.y + self.h + 10

        if self._label_id is None:
            self._label_id = self.canvas.create_text(
                lx, ly,
                text=text,
                fill="#000000",
                font=("Arial", 9, "bold")
            )
        else:
            self.canvas.coords(self._label_id, lx, ly)
            self.canvas.itemconfig(self._label_id, text=text)

    def clear_label(self):
        if self._label_id:
            self.canvas.delete(self._label_id)
            self._label_id = None