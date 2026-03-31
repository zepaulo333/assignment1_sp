import os
import timeit
import numpy as np

from files_generation import FILE_SIZES, OUTPUT_DIR
from crypto import (
    aes_ctr_encrypt, aes_ctr_decrypt,
    rsa_based_encrypt, rsa_based_decrypt,
    sha256_hash,
)

N_RUNS = 200
N_RANDOM_FILES = 100


def _stats(times):
    mean = np.mean(times)
    std = np.std(times, ddof=1) if len(times) > 1 else 0.0
    ci95 = 1.96 * std / np.sqrt(len(times)) if len(times) > 1 else 0.0
    return mean, std, ci95



def run_aes_benchmark():
    results = []
    print("\n[AES-CTR Benchmark]")
    print(f"{'Size (B)':>10} | {'Enc Mean (us)':>14} | {'Enc Std':>10} | {'Enc CI95':>10} | "
          f"{'Dec Mean (us)':>14} | {'Dec Std':>10} | {'Dec CI95':>10}")
    print("-" * 100)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            data = f.read()

        enc_times, dec_times = [], []

        key_w, nonce_w = os.urandom(32), os.urandom(16)
        ct_warm = aes_ctr_encrypt(key_w, nonce_w, data)
        aes_ctr_decrypt(key_w, nonce_w, ct_warm)

        for _ in range(N_RUNS):
            key = os.urandom(32)  
            nonce = os.urandom(16)  

            t1 = timeit.default_timer()
            ciphertext = aes_ctr_encrypt(key, nonce, data)
            t2 = timeit.default_timer()
            enc_times.append((t2 - t1) * 1e6)

            t3 = timeit.default_timer()
            aes_ctr_decrypt(key, nonce, ciphertext)
            t4 = timeit.default_timer()
            dec_times.append((t4 - t3) * 1e6)

        m_enc, s_enc, ci_enc = _stats(enc_times)
        m_dec, s_dec, ci_dec = _stats(dec_times)

        results.append({
            'size': size,
            'enc_mean': m_enc, 'enc_std': s_enc, 'enc_ci': ci_enc,
            'dec_mean': m_dec, 'dec_std': s_dec, 'dec_ci': ci_dec,
        })
        print(f"{size:10d} | {m_enc:14.2f} | {s_enc:10.2f} | {ci_enc:10.2f} | "
              f"{m_dec:14.2f} | {s_dec:10.2f} | {ci_dec:10.2f}")

    return results

def run_aes_variability_benchmark():
    results = []
    print("\n[AES Variability — Same file vs Random files]")
    print(f"{'Size (B)':>10} | {'Same Mean (us)':>15} | {'Same CI95':>10} | "
          f"{'Rand Mean (us)':>15} | {'Rand CI95':>10}")
    print("-" * 75)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            fixed_data = f.read()

        key = os.urandom(32)
        nonce = os.urandom(16)

        aes_ctr_encrypt(key, nonce, fixed_data)

        same_times = []
        for _ in range(N_RUNS):
            t1 = timeit.default_timer()
            aes_ctr_encrypt(key, nonce, fixed_data)
            t2 = timeit.default_timer()
            same_times.append((t2 - t1) * 1e6)

        rand_times = []
        for _ in range(N_RANDOM_FILES):
            random_data = os.urandom(size)
            t1 = timeit.default_timer()
            aes_ctr_encrypt(key, nonce, random_data)
            t2 = timeit.default_timer()
            rand_times.append((t2 - t1) * 1e6)

        same_mean, _, same_ci = _stats(same_times)
        rand_mean, _, rand_ci = _stats(rand_times)

        results.append({
            'size': size,
            'same_mean': same_mean, 'same_ci': same_ci,
            'random_mean': rand_mean, 'random_ci': rand_ci,
        })
        print(f"{size:10d} | {same_mean:15.2f} | {same_ci:10.2f} | "
              f"{rand_mean:15.2f} | {rand_ci:10.2f}")

    return results

def run_rsa_benchmark(e, d, n):
    results = []
    print("\n[RSA-Based Benchmark]")
    print(f"{'Size (B)':>10} | {'Enc Mean (us)':>14} | {'Enc CI95':>10} | "
          f"{'Dec Mean (us)':>14} | {'Dec CI95':>10} | {'Ratio D/E':>10}")
    print("-" * 80)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            data = f.read()

        enc_times, dec_times = [], []

        c0_w, cd_w, ol_w = rsa_based_encrypt(data, e, n)
        rsa_based_decrypt(c0_w, cd_w, ol_w, d, n)

        for _ in range(N_RUNS):
            t1 = timeit.default_timer()
            c0, c_data, o_len = rsa_based_encrypt(data, e, n)
            t2 = timeit.default_timer()
            enc_times.append((t2 - t1) * 1e6)

            t3 = timeit.default_timer()
            rsa_based_decrypt(c0, c_data, o_len, d, n)
            t4 = timeit.default_timer()
            dec_times.append((t4 - t3) * 1e6)

        m_enc, s_enc, ci_enc = _stats(enc_times)
        m_dec, s_dec, ci_dec = _stats(dec_times)

        ratio = m_dec / m_enc if m_enc > 0 else 0

        results.append({
            'size': size,
            'enc_mean': m_enc, 'enc_std': s_enc, 'enc_ci': ci_enc,
            'dec_mean': m_dec, 'dec_std': s_dec, 'dec_ci': ci_dec,
        })
        print(f"{size:10d} | {m_enc:14.2f} | {ci_enc:10.2f} | "
              f"{m_dec:14.2f} | {ci_dec:10.2f} | {ratio:10.2f}x")

    return results

def run_sha_benchmark():
    results = []
    print("\n[SHA-256 Benchmark]")
    print(f"{'Size (B)':>10} | {'Mean (us)':>14} | {'Std (us)':>10} | {'CI95 (us)':>10}")
    print("-" * 55)

    for size in FILE_SIZES:
        filepath = os.path.join(OUTPUT_DIR, f"file_{size}.bin")
        with open(filepath, "rb") as f:
            data = f.read()

        sha_times = []

        # Warm-up
        sha256_hash(data)

        for _ in range(N_RUNS):
            t1 = timeit.default_timer()
            sha256_hash(data)
            t2 = timeit.default_timer()
            sha_times.append((t2 - t1) * 1e6)

        m_sha, s_sha, ci_sha = _stats(sha_times)

        results.append({
            'size': size,
            'mean': m_sha, 'std': s_sha, 'ci': ci_sha,
        })
        print(f"{size:10d} | {m_sha:14.2f} | {s_sha:10.2f} | {ci_sha:10.2f}")

    return results
