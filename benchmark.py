import os
import timeit
import numpy as np

from files_generation import FILE_SIZES, OUTPUT_DIR
from crypto import aes_ctr_encrypt, aes_ctr_decrypt, rsa_based_encrypt, rsa_based_decrypt, sha256_hash

N_RUNS = 200
VARIABILITY_RANDOM_FILES = 20


def _stats(times):
    mean = np.mean(times)
    std = np.std(times, ddof=1) if len(times) > 1 else 0.0
    ci95 = 1.96 * std / np.sqrt(len(times)) if len(times) > 1 else 0.0
    return mean, std, ci95


def run_aes_benchmark():
    results = []
    print(f"{'Tamanho':>10} | {'Enc Mean (µs)':>15} | {'Enc CI 95%':>12} | {'Dec Mean (µs)':>15} | {'Dec CI 95%':>12}")
    print("-" * 75)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            data = f.read()

        enc_times, dec_times = [], []

        # Warm-up (not measured)
        key_w, nonce_w = os.urandom(32), os.urandom(16)
        c_warm = aes_ctr_encrypt(key_w, nonce_w, data)
        aes_ctr_decrypt(key_w, nonce_w, c_warm)

        for _ in range(N_RUNS):
            key, nonce = os.urandom(32), os.urandom(16)

            t1 = timeit.default_timer()
            ciphertext = aes_ctr_encrypt(key, nonce, data)
            t2 = timeit.default_timer()
            enc_times.append((t2 - t1) * 1e6)

            t3 = timeit.default_timer()
            aes_ctr_decrypt(key, nonce, ciphertext)
            t4 = timeit.default_timer()
            dec_times.append((t4 - t3) * 1e6)

        m_enc, _, ci_enc = _stats(enc_times)
        m_dec, _, ci_dec = _stats(dec_times)

        results.append({'size': size, 'enc_mean': m_enc, 'dec_mean': m_dec, 'enc_ci': ci_enc, 'dec_ci': ci_dec})
        print(f"{size:>10d} | {m_enc:>15.2f} | {ci_enc:>12.2f} | {m_dec:>15.2f} | {ci_dec:>12.2f}")

    return results


def run_aes_variability_benchmark():
    """
    Required by assignment point B:
    1) fixed algorithm over the same file multiple times
    2) fixed algorithm over multiple randomly generated files of fixed size
    """
    results = []
    print("\n[AES Variability] Same file repeated vs random files (fixed size)")
    print(f"{'Size (B)':>10} | {'Same Mean (µs)':>15} | {'Same CI':>10} | {'Rand Mean (µs)':>15} | {'Rand CI':>10}")
    print("-" * 75)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            fixed_data = f.read()

        key, nonce = os.urandom(32), os.urandom(16)

        # Same file multiple times
        same_times = []
        for _ in range(N_RUNS):
            t1 = timeit.default_timer()
            aes_ctr_encrypt(key, nonce, fixed_data)
            t2 = timeit.default_timer()
            same_times.append((t2 - t1) * 1e6)

        # Multiple random files of fixed size
        rand_times = []
        for _ in range(VARIABILITY_RANDOM_FILES):
            data = os.urandom(size)
            t1 = timeit.default_timer()
            aes_ctr_encrypt(key, nonce, data)
            t2 = timeit.default_timer()
            rand_times.append((t2 - t1) * 1e6)

        same_mean, _, same_ci = _stats(same_times)
        rand_mean, _, rand_ci = _stats(rand_times)

        results.append({
            'size': size,
            'same_mean': same_mean,
            'same_ci': same_ci,
            'random_mean': rand_mean,
            'random_ci': rand_ci
        })
        print(f"{size:10d} | {same_mean:15.2f} | {same_ci:10.2f} | {rand_mean:15.2f} | {rand_ci:10.2f}")

    return results


def run_rsa_benchmark(e, d, n):
    results = []
    print(f"{'Size (B)':>10} | {'Enc Mean (µs)':>15} | {'Dec Mean (µs)':>15} | {'Ratio (D/E)':>10}")
    print("-" * 58)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            data = f.read()

        enc_times, dec_times = [], []

        for _ in range(N_RUNS):
            t1 = timeit.default_timer()
            c0, c_data, o_len = rsa_based_encrypt(data, e, n)
            t2 = timeit.default_timer()
            enc_times.append((t2 - t1) * 1e6)

            t3 = timeit.default_timer()
            rsa_based_decrypt(c0, c_data, o_len, d, n)
            t4 = timeit.default_timer()
            dec_times.append((t4 - t3) * 1e6)

        m_enc, _, ci_enc = _stats(enc_times)
        m_dec, _, ci_dec = _stats(dec_times)
        results.append({
            'size': size, 'enc_mean': m_enc, 'dec_mean': m_dec,
            'enc_ci': ci_enc, 'dec_ci': ci_dec,
        })
        print(f"{size:10d} | {m_enc:15.2f} | {m_dec:15.2f} | {m_dec / m_enc:10.2f}x")

    return results


def run_sha_benchmark():
    results = []
    print(f"{'Size (B)':>10} | {'SHA-256 Mean (µs)':>18} | {'CI 95%':>10}")
    print("-" * 45)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            data = f.read()

        sha_times = []

        for _ in range(N_RUNS):
            t1 = timeit.default_timer()
            sha256_hash(data)
            t2 = timeit.default_timer()
            sha_times.append((t2 - t1) * 1e6)

        m_sha, _, ci_sha = _stats(sha_times)

        results.append({'size': size, 'mean': m_sha, 'ci': ci_sha})
        print(f"{size:10d} | {m_sha:18.2f} | {ci_sha:10.2f}")

    return results
