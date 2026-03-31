import os

FILE_SIZES = [8, 64, 512, 4096, 32768, 262144, 2097152]

OUTPUT_DIR = "test_files"


def generate_files():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "wb") as f:
            f.write(os.urandom(size))
        print(f"  Gerado: {filepath} ({size} bytes)")
