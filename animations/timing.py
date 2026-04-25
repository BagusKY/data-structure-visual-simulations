class Timing:
    """
    Pengatur waktu global untuk animasi
    Semua delay & durasi lewat sini → biar konsisten
    """

    # =========================
    # BASE CONFIG
    # =========================
    SPEED = 1.0  # 1.0 = normal, >1 lebih cepat, <1 lebih lambat

    # =========================
    # DURATIONS (ms)
    # =========================
    MOVE = 400
    FAST = 200
    SLOW = 700

    # =========================
    # DELAYS (ms)
    # =========================
    SHORT_DELAY = 200
    NORMAL_DELAY = 500
    LONG_DELAY = 800

    # =========================
    # CONTROL METHODS
    # =========================
    @classmethod
    def set_speed(cls, speed: float):
        """
        Ubah kecepatan global animasi
        contoh:
            2.0 = 2x lebih cepat
            0.5 = lebih lambat
        """
        if speed <= 0:
            raise ValueError("Speed must be > 0")
        cls.SPEED = speed

    @classmethod
    def duration(cls, value: int):
        """
        Ambil durasi yang sudah disesuaikan speed
        """
        return int(value / cls.SPEED)

    @classmethod
    def delay(cls, root, value: int, callback=None):
        """
        Delay dengan speed control
        """
        adjusted = cls.duration(value)
        if callback:
            root.after(adjusted, callback)
        else:
            root.after(adjusted)