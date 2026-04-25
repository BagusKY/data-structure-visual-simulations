from core.queue import Queue


class HotPotatoSimulation:
    """
    Simulasi permainan Hot Potato:
    - pemain berdiri dalam queue
    - "kentang panas" diputar sejumlah langkah
    - pemain terakhir yang kena → keluar (eliminasi)
    - ulang sampai tersisa 1 pemenang
    """

    def __init__(self):
        self.queue = Queue()
        self.players = []
        self.eliminated = []
        self.current = None

    # =========================
    # SETUP
    # =========================
    def set_players(self, names):
        """
        names: list of string
        """
        if not names:
            raise ValueError("Player list cannot be empty")

        self.queue.clear()
        self.players = list(names)
        self.eliminated.clear()
        self.current = None

        for name in self.players:
            self.queue.enqueue(name)

    # =========================
    # GAME STEP
    # =========================
    def play_round(self, steps):
        """
        Jalankan 1 ronde:
        - putar queue sebanyak 'steps'
        - pemain terakhir keluar
        Return:
            {
                "rotations": [...],
                "eliminated": name,
                "remaining": [...]
            }
        """
        if self.queue.size() <= 1:
            return None  # game selesai

        if steps <= 0:
            raise ValueError("Steps must be > 0")

        rotations = []

        # rotasi (pass potato)
        for _ in range(steps):
            player = self.queue.dequeue()
            self.queue.enqueue(player)
            rotations.append(player)

        # eliminasi
        eliminated_player = self.queue.dequeue()
        self.eliminated.append(eliminated_player)

        return {
            "rotations": rotations,
            "eliminated": eliminated_player,
            "remaining": self.queue.get_all()
        }

    # =========================
    # STATE
    # =========================
    def get_players(self):
        return self.queue.get_all()

    def get_eliminated(self):
        return list(self.eliminated)

    def get_winner(self):
        if self.queue.size() == 1:
            return self.queue.peek()
        return None

    def is_finished(self):
        return self.queue.size() <= 1

    def reset(self):
        self.queue.clear()
        self.players.clear()
        self.eliminated.clear()
        self.current = None