import tkinter as tk

from cases.case1_printer.controller import PrinterController
from cases.case2_hotpotato.controller import HotPotatoController
from cases.case3_hospital.controller import HospitalController
from cases.case4_bfs.controller import BFSController
from cases.case5_airport.controller import AirportController


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualisasi Struktur Data")
        self.root.geometry("900x500")

        self.current_frame = None

        self.show_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_menu(self):
        self.clear_frame()

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        title = tk.Label(
            frame,
            text="Visualisasi Struktur Data",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        btn1 = tk.Button(frame, text="1. Printer Queue", width=30,
                         command=self.open_case1)
        btn1.pack(pady=5)

        btn2 = tk.Button(frame, text="2. Hot Potato (Queue)", width=30,
                         command=self.open_case2)
        btn2.pack(pady=5)

        btn3 = tk.Button(frame, text="3. Hospital (Priority Queue)", width=30,
                         command=self.open_case3)
        btn3.pack(pady=5)

        btn4 = tk.Button(frame, text="4. BFS Graph", width=30,
                         command=self.open_case4)
        btn4.pack(pady=5)

        btn5 = tk.Button(frame, text="5. Airport Queue", width=30,
                         command=self.open_case5)
        btn5.pack(pady=5)

    def open_case1(self):
        self.load_case(PrinterController)

    def open_case2(self):
        self.load_case(HotPotatoController)

    def open_case3(self):
        self.load_case(HospitalController)

    def open_case4(self):
        self.load_case(BFSController)

    def open_case5(self):
        self.load_case(AirportController)

    def load_case(self, controller_class):
        self.clear_frame()
        controller = controller_class(self.root, self.show_menu)
        self.current_frame = controller.frame


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()