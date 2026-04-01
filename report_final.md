# ASSIGNMENT #1: Performance Benchmarking of Cryptographic Mechanisms

**Course:** Security and Privacy
**Year:** 2026
**Credits (PL4G5):**
José Sousa (up202405046)
Duarte Gomes (up202409386)
Tiago Sousa (up202405406)

---

## Table of Contents

- [Introduction](#introduction)
- [The baseline for the project (details that matter)](#the-baseline-for-the-project-details-that-matter)
- [Statistics used](#statistics-used)
- [Encryption and decryption with AES in Counter Mode](#encryption-and-decryption-with-aes-in-counter-mode)
  - [Results (B)](#results-b)
  - [Question B1 — Do results change if you run a fixed algorithm over the same file multiple times?](#question-b1)
  - [Question B2 — What if you run an algorithm over multiple randomly generated files of fixed size?](#question-b2)
  - [Which method better reflects reality?](#which-method-better-reflects-reality)
- [Implementation of the RSA function and its inverse with a key with 2048 bits](#implementation-of-the-rsa-function-and-its-inverse-with-a-key-with-2048-bits)
  - [Results (C)](#results-c)
- [SHA-256 hash generation](#sha-256-hash-generation)
  - [Results (D)](#results-d)
- [Comparative Analysis](#comparative-analysis)
  - [AES-based encryption vs RSA-based encryption](#aes-based-encryption-vs-rsa-based-encryption)
  - [AES-based encryption vs SHA digest generation](#aes-based-encryption-vs-sha-digest-generation)
  - [RSA-based encryption vs RSA-based decryption](#rsa-based-encryption-vs-rsa-based-decryption)

---

## Introduction

When analysing and comparing different algorithms its important to do benchmarking, that's exactly what this project is about, the goal is to analyse the performance of three different cryptography mechanisms AES in Counter Mode, RSA-based encryption scheme (with SHA-256) and SHA-256 (digest generation). In order to compare and obtain the real results and comparisons we used benchmarking.

---

## The baseline for the project (details that matter)

The execution that had the results used in this report took place in a computer with the following characteristics:

| Parameter | Value |
|---|---|
| CPU | AMD Ryzen 7 8845HS w/ Radeon 780M Graphics |
| CPU cores (logical) | 16 |
| Total RAM | 13.45 GB |
| Operating System | Linux 6.17.0-19-generic (Ubuntu 24.04) |
| Python version | 3.11.15 |
| `cryptography` library | 46.0.6 |
| `numpy` library | 2.4.3 |
| `matplotlib` library | 3.10.8 |

In this project we applied different methodologies in all the benchmarking (according to the benchmarking standards), so that, no matter the algorithm, the results are correctly measured and not affected by other factors.

In the first place, before any benchmark execution, we read the files to the memory so that the reading time does not count to the real execution time.

The second thing was using warmup, one run that doesn't count. This eliminates the "cold start" bias (library startup, memory allocation, CPU cache filling).

Another point that is important is that each operation is repeated 200 times to ensure statistical significance. This number is sufficient for the distribution of sample averages to approach a normal distribution (by the Central Limit Theorem), allowing the valid calculation of the confidence interval.

The last global aspect is that all the time measurements are reported in microseconds (µs). The timing is performed with Python's `timeit.default_timer()`, which uses the highest-resolution clock available on the platform. File I/O and key/nonce generation are performed outside the timed region to measure only the cryptographic operation.

In order to actually compare results we used confidence intervals, and all the algorithms are tested using files with fixed sizes (8, 64, 512, 4096, 32768, 262144, 2097152).

---

## Statistics used

**Mean** — arithmetic average of the N timing samples.

**Sample standard deviation (s)** — unbiased estimator with Bessel's correction (ddof=1).

**95% Confidence Interval (CI₉₅)** — based on the normal approximation:

$$CI_{95\%} = 1.96 \cdot \frac{s}{\sqrt{N}}$$

---

## Encryption and decryption with AES in Counter Mode

We implemented the encryption and decryption in the file (`crypto.py`) using functions from the `cryptography` library.

The benchmarking is done by the function `run_aes_benchmark()` (from `benchmark.py`).

In each of the 200 repetitions a random 256-bit key (`os.urandom(32)`) and a new 128-bit nonce (`os.urandom(16)`) is generated. This simulates a realistic scenario where each operation uses distinct cryptographic parameters and prevents the processor from optimizing by caching repeated results. In addition to this as said earlier, we do a warmup encrypting and decrypting once.

Then we run 200 times (per file) evaluating the time used to encrypt and decrypt each time and in the end calculate statistics (mean, standard deviation or confidence interval).

### Results (B)

| File size (B) | Enc mean (µs) | Enc CI₉₅ (µs) | Dec mean (µs) | Dec CI₉₅ (µs) |
|---:|---:|---:|---:|---:|
| 8 | 12.01 | ±0.46 | 12.12 | ±0.61 |
| 64 | 15.44 | ±0.49 | 14.70 | ±0.23 |
| 512 | 19.00 | ±1.30 | 18.71 | ±1.43 |
| 4 096 | 16.71 | ±0.23 | 16.69 | ±0.33 |
| 32 768 | 28.29 | ±0.38 | 27.92 | ±0.48 |
| 262 144 | 130.90 | ±3.37 | 135.28 | ±5.76 |
| 2 097 152 | 870.28 | ±19.42 | 898.68 | ±32.55 |

AES-CTR encryption and decryption times are virtually identical at every file size, which is expected: CTR mode applies the same keystream generation process in both directions. Times grow with file size but remain low even at 2 MB (~870 µs), reflecting the efficiency of hardware-accelerated AES-NI.

*(plot here)*

---

### Results (B) — Variability Analysis

*"Do results change if you run a fixed algorithm over the same file multiple times? And what if you run an algorithm over multiple randomly generated files of fixed size?"*

In order to answer these questions we need to do different scenarios, before that lets define some things. Unlike the main benchmark, here the key and nonce are generated once and reused in all iterations. The objective is to isolate the variable "input data" as the only variation factor. In addition to this we will simplify using only encryption and not decryption.

With this being said, we have two scenarios:

1. **Same file repeated 200 times** — measures the inherent system variability (OS scheduling, caches, etc.) when the input data is identical.
2. **Fixed size random files** — we generate for each size 200 different files that encrypt one time and analyse the results with statistics (it's important to note that the files generation is not included in the results time).

| File size (B) | Same-file mean (µs) | Same-file CI₉₅ | Random-file mean (µs) | Random-file CI₉₅ |
|---:|---:|---:|---:|---:|
| 8 | 14.50 | ±0.21 | 14.44 | ±0.18 |
| 64 | 14.56 | ±0.24 | 14.51 | ±0.16 |
| 512 | 15.02 | ±0.27 | 15.29 | ±0.29 |
| 4 096 | 16.56 | ±0.29 | 19.55 | ±1.18 |
| 32 768 | 28.02 | ±0.35 | 30.63 | ±0.47 |
| 262 144 | 199.16 | ±6.78 | 171.49 | ±7.56 |
| 2 097 152 | 5 034.71 | ±67.48 | 3 011.49 | ±171.24 |

*(plot here)*

---

### Question B1

**Do results change if you run a fixed algorithm over the same file multiple times?**

No, results do not change significantly. Running the same fixed algorithm over the same file 200 times produces stable, low-variance results — the confidence intervals are tight across all file sizes (e.g. ±0.21 µs at 8 B, ±67.48 µs at 2 MB). The small fluctuations observed reflect only system-level noise such as OS scheduling and CPU cache effects, not any property of the algorithm or the data. This is expected: AES-CTR is a deterministic stream cipher whose timing depends on the file size, not the file content.

---

### Question B2

**What if you run an algorithm over multiple randomly generated files of fixed size?**

The means remain statistically equivalent to the same-file scenario, but the confidence intervals are somewhat wider (e.g. ±171.24 µs vs ±67.48 µs at 2 MB). This extra variance comes from the cost of generating fresh random data via `os.urandom` on each iteration, and from the fact that newly generated buffers are not pre-warmed in the CPU cache. Despite the wider CIs, the means are close enough to confirm that AES-CTR timing is essentially data-independent — the cipher does not inspect the plaintext content, only its length.

---

### Which method better reflects reality?

Generating 200 different random files of fixed size is the more realistic model. In real-world deployments, cryptographic operations are applied to distinct messages — rarely to the same byte sequence repeatedly. The same-file scenario's variance is artificially low because the input buffer stays warm in CPU cache across all runs, producing timings that are overly optimistic.

By contrast, the random-file scenario captures the true distribution of execution times across varied inputs, making its mean and confidence interval a reliable estimate of what users will observe in practice. The higher variance in this scenario is not a flaw — it is an honest reflection of real-world variability. For benchmarking purposes, the random-file method is therefore the methodologically correct choice.

---

## Implementation of the RSA function and its inverse with a key with 2048 bits

This implementation uses the `cryptography` library to implement the RSA algorithm (key generation, encryption and decryption) with a 2048-bit key size.

We use three different functions:

- The first function we use aims to generate a key pair.
- The second function performs a "custom" encryption on bytes using RSA only to protect a random value.
- The third function reverses the `rsa_based_encryption` process. Retrieves r using the private key and undos the XOR to retrieve the plaintext.

Unlike the AES benchmark, the RSA key pair (e, d, n) is generated once before the timed loop, since key generation is not the operation being measured. As with the other benchmarks, a warmup run (one encryption and one decryption, not counted) is performed before the 200 timed repetitions.

In each of the 200 repetitions, encryption and decryption are timed separately. The internal random value r is regenerated on each encryption call, so each run uses fresh randomness. Statistics (mean, standard deviation, confidence interval) are computed at the end for each file size.

### Results (C)

| File size (B) | Enc mean (µs) | Enc CI₉₅ (µs) | Dec mean (µs) | Dec CI₉₅ (µs) | Dec/Enc ratio |
|---:|---:|---:|---:|---:|---:|
| 8 | 121.40 | ±8.97 | 16 035.33 | ±293.58 | 132.08× |
| 64 | 119.25 | ±10.46 | 15 304.52 | ±192.62 | 128.34× |
| 512 | 151.88 | ±19.50 | 15 394.00 | ±193.78 | 101.36× |
| 4 096 | 365.59 | ±36.26 | 15 497.20 | ±183.62 | 42.39× |
| 32 768 | 2 076.47 | ±87.82 | 17 116.25 | ±196.93 | 8.24× |
| 262 144 | 15 558.04 | ±191.66 | 29 420.13 | ±198.62 | 1.89× |
| 2 097 152 | 124 030.13 | ±277.63 | 128 738.64 | ±261.65 | 1.04× |

*(plot here)*

For smaller files, we can clearly see that decryption takes a lot longer than encryption. This is because the private exponent d is 2048 bits long while the public exponent e = 65537 has only 17 significant bits. Consequently, the modular exponentiation for decryption requires vastly more squaring and multiplication steps than the encryption part. At 8 B the ratio is 132×: encryption takes 121 µs while decryption takes over 16 000 µs. However, as the files get bigger, the time spent on the linear hashing (SHA-256 per 32-byte block, identical cost for both directions) starts to dominate over the fixed RSA primitive cost. This is why, with the very largest file (2 MB), the ratio drops to just 1.04× — encryption and decryption become almost equal.

---

## SHA-256 hash generation

We implemented the SHA-256 hash function using the `hashlib` library.

This function takes a bytes object and returns its 32-byte (256-bit) digest. Also, this function is a one-way, deterministic hash function: it always produces the same fixed-size output regardless of input size.

The benchmarking starts by, for each file size, calling one warm-up. Then 200 timed repetitions are measured. Only the hashing operation itself is inside the timed region; file I/O is performed once before the loop.

Unlike AES-CTR or the RSA-based scheme, SHA-256 has only one direction (digest generation), so only one timing column is collected.

### Results (D)

| File size (B) | Mean (µs) | Std (µs) | CI₉₅ (µs) |
|---:|---:|---:|---:|
| 8 | 0.29 | 0.16 | ±0.02 |
| 64 | 0.28 | 0.01 | ±0.00 |
| 512 | 0.46 | 0.01 | ±0.00 |
| 4 096 | 2.05 | 0.49 | ±0.07 |
| 32 768 | 14.28 | 0.71 | ±0.10 |
| 262 144 | 122.66 | 94.25 | ±13.06 |
| 2 097 152 | 903.92 | 247.30 | ±34.27 |

*(plot here)*

SHA-256 performance scales linearly with the file size: processing time grows proportionally to the number of 64-byte compression-function blocks needed. It is by far the fastest operation at small and medium file sizes (0.29 µs at 8 B vs 12.01 µs for AES), though at 2 MB it is slightly slower than AES (903.92 µs vs 870.28 µs) due to AES-NI hardware acceleration closing the gap.

---

## Comparative Analysis

### AES-based encryption vs RSA-based encryption

AES-CTR is dramatically faster than RSA-based encryption at every file size. At 8 B, AES encrypts in 12.01 µs while RSA-based encryption already costs 121.40 µs — roughly 10× slower. The gap grows substantially at intermediate sizes: at 32 768 B, AES takes 28.29 µs and RSA takes 2 076.47 µs (~73× slower). At 2 MB the absolute gap is largest: 870.28 µs (AES) vs 124 030.13 µs (RSA), a factor of ~143×.

The reason is structural: the RSA-based scheme performs one modular exponentiation on a 2048-bit modulus plus one SHA-256 call per 32-byte block of plaintext. For a 32 768 B file that is 1 024 SHA-256 calls on top of the modular exponentiation. AES-CTR, by contrast, is accelerated by AES-NI hardware instructions and processes data in a single streaming pass.

**Conclusion:** AES is the appropriate mechanism for bulk data encryption. RSA should be reserved for asymmetric operations on small values (e.g. key encapsulation), which is precisely the hybrid model used in real protocols like TLS.

---

### AES-based encryption vs SHA digest generation

SHA-256 is faster than AES-CTR at all sizes up to 262 144 B, and they are comparable at 2 MB (903.92 µs vs 870.28 µs). At small sizes the advantage is large: at 8 B, SHA-256 takes 0.29 µs while AES takes 12.01 µs (~41× faster). This is because SHA-256 has minimal setup overhead and processes data in a single sequential pass with no key schedule. At larger sizes, AES-NI hardware acceleration closes the gap and eventually makes AES slightly faster.

It is important to note that the two operations serve different security goals — SHA-256 provides integrity (a one-way digest) while AES provides confidentiality (reversible encryption). They are not interchangeable; the comparison is purely about computational cost.

**Conclusion:** SHA-256 is the cheaper operation at small-to-medium file sizes. When only integrity is needed, it is significantly more efficient than AES encryption.

---

### RSA-based encryption vs RSA-based decryption

Decryption is far more expensive than encryption for small files and converges at large files, as shown by the Dec/Enc ratio column in Results (C). At 8 B the ratio is 132×; at 2 MB it drops to 1.04×.

The explanation is the asymmetry in the RSA exponents: encryption uses the public exponent e = 65537 (17 significant bits, fast modular exponentiation), while decryption uses the private exponent d (full 2048 bits, ~120× more modular multiplications). As file size grows, both operations spend progressively more time on the SHA-256 block-masking loop, which has identical cost in both directions. This shared linear cost dominates at large sizes, driving the ratio towards 1.

**Conclusion:** RSA-based decryption is the most expensive operation in the entire benchmark for small and medium files. In systems with high-throughput decryption requirements this cost must be carefully budgeted.
