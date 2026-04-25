import string
import random


# =========================
# GENERATORS
# =========================
def generate_label(index: int) -> str:
    """
    0 -> A, 1 -> B, ... 25 -> Z, 26 -> A1, 27 -> B1, ...
    Cocok untuk label elemen (A, B, C, ...)
    """
    if index < 0:
        raise ValueError("Index must be >= 0")

    base = string.ascii_uppercase
    letter = base[index % 26]
    suffix = index // 26

    return f"{letter}{suffix}" if suffix > 0 else letter


def generate_random_id(length: int = 6) -> str:
    """
    Generate ID acak (huruf + angka)
    """
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


# =========================
# SAFE OPERATIONS
# =========================
def safe_call(fn, *args, **kwargs):
    """
    Jalankan fungsi dengan try-except
    Return:
        (True, result) atau (False, error_message)
    """
    try:
        return True, fn(*args, **kwargs)
    except Exception as e:
        return False, str(e)


# =========================
# LIST UTILITIES
# =========================
def chunk_list(data, size):
    """
    Bagi list jadi beberapa bagian kecil
    """
    if size <= 0:
        raise ValueError("Size must be > 0")

    return [data[i:i + size] for i in range(0, len(data), size)]


def flatten(list_of_lists):
    """
    Flatten list 2D → 1D
    """
    return [item for sublist in list_of_lists for item in sublist]


# =========================
# DEBUG / FORMAT
# =========================
def format_queue(data):
    """
    Format list jadi string queue
    """
    return " → ".join(str(x) for x in data)


def print_debug(title: str, data):
    """
    Debug helper (opsional)
    """
    print(f"[DEBUG] {title}: {data}")