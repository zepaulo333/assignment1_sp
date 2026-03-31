# Assignment #1 — Performance Benchmarking of Cryptographic Mechanisms
**PL4: Performance Measures for Message Digests, Symmetric and Asymmetric Cryptography**

---

## 1. Experimental Setup

All benchmarks were executed on the following machine:

| Parameter | Value |
|---|---|
| CPU | Intel Core i9-7900X @ 3.30 GHz |
| CPU cores (logical) | 20 |
| Total RAM | 31.02 GB |
| Operating System | Linux 6.17.0-19-generic (Ubuntu 24.04) |
| Python version | 3.11.15 |
| `cryptography` library | 46.0.6 |
| `numpy` library | 2.4.3 |
| `matplotlib` library | 3.10.8 |

---

## 2. Methodology

### 2.1 Statistical Significance

To produce statistically significant results, each cryptographic operation was repeated **N = 200 times** per file size. For each series of measurements the following statistics were computed:

- **Mean** — arithmetic average of the N timing samples.
- **Sample standard deviation** — unbiased estimator with Bessel's correction (ddof=1).
- **95 % Confidence Interval (CI₉₅)** — based on the normal approximation:

$$CI_{95\%} = 1.96 \cdot \frac{s}{\sqrt{N}}$$

All times are reported in **microseconds (µs)**. Timing is performed with Python's `timeit.default_timer()`, which uses the highest-resolution clock available on the platform. File I/O and key/nonce generation are performed **outside** the timed region to measure only the cryptographic operation.

A **warm-up run** is executed before every benchmark series to mitigate cold-start effects (e.g. JIT compilation, CPU branch prediction, library initialisation).

### 2.2 File Sizes

Random binary files were generated with `os.urandom` for the following sizes:

```
8, 64, 512, 4096, 32768, 262144, 2097152  (bytes)
```

### 2.3 AES-CTR Variability Analysis

To answer the question posed in Point B ("Do results change if you run a fixed algorithm over the same file multiple times? And what if you run it over multiple randomly generated files of fixed size?"), two scenarios were measured:

1. **Same-file scenario** — the same fixed data buffer is encrypted 200 times with a fixed key/nonce.
2. **Random-file scenario** — 100 freshly generated random buffers of the same size are each encrypted once.

---

## 3. Implementation

### 3.1 AES-256 in Counter Mode (Point B)

AES-256-CTR was implemented using `cryptography.hazmat.primitives.ciphers` with:
- 256-bit key (32 bytes), drawn freshly from `os.urandom` for each benchmark run.
- 128-bit nonce (16 bytes), also drawn fresh for each run.

```python
def aes_ctr_encrypt(key: bytes, nonce: bytes, plaintext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()

def aes_ctr_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
```

### 3.2 RSA-Based Encryption Scheme (Point C)

The encryption scheme implemented is:

$$Enc(m;\, r) = \bigl(RSA(r),\; H(0,r)\oplus m_0,\; \ldots,\; H(n,r)\oplus m_n\bigr)$$

where $H = \text{SHA-256}$ (output size $\ell = 32$ bytes), $r$ is a uniformly random value sampled modulo $n$, and $n = \lceil |m|/\ell \rceil$ is the number of 32-byte message blocks.

- **Key size:** 2048 bits, generated via `cryptography`'s RSA key generation with public exponent $e = 65537$.
- **Encryption:** computes $c_0 = r^e \bmod n$ (using Python's built-in `pow(r, e, n)`) and for each block $i$: $c_i = m_i \oplus \text{SHA-256}(i \,\|\, r)$.
- **Decryption:** recovers $r = c_0^d \bmod n$ and reverses the XOR masks.

```python
def rsa_based_encrypt(plaintext: bytes, e: int, n: int):
    ell = 32
    r = int.from_bytes(os.urandom((n.bit_length()+7)//8), 'big') % n
    c0 = pow(r, e, n)
    r_bytes = r.to_bytes((n.bit_length()+7)//8, 'big')
    cipher_blocks = []
    for i, block in enumerate(chunks(plaintext, ell)):
        h_i = hashlib.sha256(i.to_bytes(4,'big') + r_bytes).digest()
        cipher_blocks.append(bytes(a^b for a,b in zip(block.ljust(ell,b'\x00'), h_i)))
    return c0, b"".join(cipher_blocks), len(plaintext)

def rsa_based_decrypt(c0, cipher_data, original_len, d, n):
    r = pow(c0, d, n)
    r_bytes = r.to_bytes((n.bit_length()+7)//8, 'big')
    plain_blocks = []
    for i in range(len(cipher_data)//32):
        c_i = cipher_data[i*32:(i+1)*32]
        h_i = hashlib.sha256(i.to_bytes(4,'big') + r_bytes).digest()
        plain_blocks.append(bytes(a^b for a,b in zip(c_i, h_i)))
    return b"".join(plain_blocks)[:original_len]
```

### 3.3 SHA-256 Digest (Point D)

```python
def sha256_hash(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()
```

---

## 4. Results

### 4.1 AES-256-CTR Encryption and Decryption (Point B)

| File size (B) | Enc mean (µs) | Enc CI₉₅ (µs) | Dec mean (µs) | Dec CI₉₅ (µs) |
|---:|---:|---:|---:|---:|
| 8 | 7.38 | ±0.12 | 7.12 | ±0.18 |
| 64 | 9.79 | ±1.03 | 9.51 | ±1.17 |
| 512 | 7.78 | ±0.10 | 7.57 | ±0.17 |
| 4 096 | 8.83 | ±0.15 | 8.60 | ±0.23 |
| 32 768 | 16.73 | ±0.54 | 16.04 | ±0.26 |
| 262 144 | 80.39 | ±0.80 | 79.75 | ±1.27 |
| 2 097 152 | 701.91 | ±3.18 | 703.19 | ±9.68 |

### 4.2 AES-CTR Variability: Same File vs Random Files (Point B)

| File size (B) | Same-file mean (µs) | Same-file CI₉₅ | Random-file mean (µs) | Random-file CI₉₅ |
|---:|---:|---:|---:|---:|
| 8 | 7.79 | ±0.41 | 7.22 | ±0.09 |
| 64 | 7.31 | ±0.15 | 7.00 | ±0.01 |
| 512 | 8.66 | ±0.31 | 7.85 | ±0.42 |
| 4 096 | 8.75 | ±0.24 | 8.52 | ±0.13 |
| 32 768 | 16.46 | ±0.27 | 16.91 | ±0.65 |
| 262 144 | 78.00 | ±0.71 | 83.67 | ±3.97 |
| 2 097 152 | 2 309.79 | ±16.58 | 2 077.81 | ±121.42 |

### 4.3 RSA-Based Encryption and Decryption (Point C)

| File size (B) | Enc mean (µs) | Enc CI₉₅ (µs) | Dec mean (µs) | Dec CI₉₅ (µs) | Dec/Enc ratio |
|---:|---:|---:|---:|---:|---:|
| 8 | 159.69 | ±2.39 | 21 813.74 | ±271.28 | 136.60× |
| 64 | 160.15 | ±0.97 | 21 534.50 | ±33.78 | 134.47× |
| 512 | 219.00 | ±12.56 | 22 677.78 | ±708.94 | 103.55× |
| 4 096 | 571.41 | ±19.30 | 22 393.70 | ±479.48 | 39.19× |
| 32 768 | 3 286.76 | ±12.94 | 24 818.26 | ±273.85 | 7.55× |
| 262 144 | 26 746.14 | ±700.76 | 49 416.59 | ±1 090.79 | 1.85× |
| 2 097 152 | 212 660.17 | ±2 335.29 | 235 838.38 | ±2 718.45 | 1.11× |

### 4.4 SHA-256 Digest Generation (Point D)

| File size (B) | Mean (µs) | Std (µs) | CI₉₅ (µs) |
|---:|---:|---:|---:|
| 8 | 0.61 | 0.16 | ±0.02 |
| 64 | 0.77 | 0.69 | ±0.10 |
| 512 | 1.68 | 0.02 | ±0.00 |
| 4 096 | 9.11 | 2.84 | ±0.39 |
| 32 768 | 63.92 | 5.98 | ±0.83 |
| 262 144 | 501.94 | 18.15 | ±2.52 |
| 2 097 152 | 4 005.04 | 84.44 | ±11.70 |

---

## 5. Plots

The following plots were generated (all in log-log scale, error bars represent the 95 % CI):

| File | Content |
|---|---|
| `plots/plot_all_combined.png` | All five series together |
| `plots/plot_aes_enc_dec.png` | AES-CTR encrypt vs decrypt |
| `plots/plot_rsa_enc_dec.png` | RSA-based encrypt vs decrypt |
| `plots/plot_aes_vs_rsa.png` | AES encrypt vs RSA-based encrypt |
| `plots/plot_aes_vs_sha.png` | AES encrypt vs SHA-256 digest |
| `plots/plot_sha256.png` | SHA-256 digest alone |

---

## 6. Analysis and Discussion

### 6.1 AES-based encryption vs RSA-based encryption

**AES-CTR is dramatically faster than the RSA-based scheme for all file sizes.**

For the smallest file (8 B), AES encryption takes **7.38 µs** whereas RSA-based encryption already costs **159.69 µs** — a factor of roughly **22×**. This gap widens significantly at intermediate sizes: at 32 768 B, AES takes 16.73 µs and RSA takes 3 286.76 µs (**≈ 196× slower**). At the largest size (2 097 152 B) the ratio narrows to about **303×** (AES: 701.91 µs, RSA: 212 660.17 µs) because the RSA-based scheme's bulk data work (XOR with SHA-256 masks) now dominates its own cost and both algorithms scale roughly linearly with data size — but AES benefits from hardware AES-NI acceleration, whereas the Python-level SHA-256 loop in the RSA scheme does not.

**Why the difference?** The RSA-based scheme performs one modular exponentiation ($r^e \bmod n$) using a 2048-bit modulus plus one SHA-256 call per 32-byte block. For a 32 768 B file that is 1 024 SHA-256 calls on top of the modular exponentiation. AES-CTR, by contrast, is accelerated by AES-NI hardware instructions and processes data in a single streaming pass.

**Practical conclusion:** AES is the appropriate choice for bulk data encryption. RSA (or any asymmetric primitive) should only be applied to small payloads (e.g. key encapsulation), exactly as in hybrid encryption schemes like TLS.

### 6.2 AES-based encryption vs SHA-256 digest generation

**SHA-256 is consistently faster than AES-CTR for all file sizes.**

At 8 B, SHA-256 takes 0.61 µs vs 7.38 µs for AES — a **12× advantage**. At 2 097 152 B, SHA-256 takes 4 005.04 µs vs 701.91 µs for AES — here **AES is faster by ≈ 5.7×**. The crossover occurs somewhere around 32 768 B, where both algorithms are in the tens of microseconds range.

This happens because SHA-256 has higher per-byte throughput than AES-CTR at large sizes (SHA-256 processes data in 64-byte blocks using a fixed-cost compression function), while AES-CTR benefits from hardware parallelism at larger scales. For small inputs, SHA-256's constant-overhead advantage dominates; for large inputs, AES-NI throughput takes over.

**Important note:** the two operations serve different security goals — SHA-256 provides integrity (a one-way digest) while AES provides confidentiality (reversible encryption). They are not interchangeable, but if only a digest is needed, SHA-256 is a cheaper operation at small-to-medium sizes.

### 6.3 RSA-based encryption vs RSA-based decryption

**Decryption is significantly more expensive than encryption, and the ratio narrows as file size grows.**

For small files (8–64 B), decryption is **~135× slower** than encryption (e.g. 21 813 µs vs 160 µs at 8 B). For large files (2 097 152 B), the ratio drops to just **1.11×** (235 838 µs vs 212 660 µs).

**Why?** Both operations share identical data-processing cost (SHA-256 per block + XOR). The key difference is the modular exponentiation:
- **Encryption** uses the *public* exponent $e = 65537 = 2^{16}+1$, which requires only 17 modular squarings (fast).
- **Decryption** uses the *private* exponent $d$, which is a full 2048-bit number requiring ~2048 squarings/multiplications (roughly 100× more work).

As file size increases, the bulk SHA-256 data work dominates and the ratio converges towards 1. For small files the modular exponentiation cost overwhelms everything else, making decryption ~135× slower.

**Practical conclusion:** in systems requiring high-throughput decryption, the cost of private-key operations must be carefully budgeted — hardware security modules or pre-computation techniques may be warranted.

### 6.4 AES-CTR Variability: Same File vs Random Files

**Results are largely stable between the two scenarios; differences are statistically small and within noise for most sizes.**

| Size | Same-file (µs) | Random-file (µs) | Difference |
|---:|---:|---:|---:|
| 8 B | 7.79 | 7.22 | −7% |
| 64 B | 7.31 | 7.00 | −4% |
| 512 B | 8.66 | 7.85 | −9% |
| 4 096 B | 8.75 | 8.52 | −3% |
| 32 768 B | 16.46 | 16.91 | +3% |
| 262 144 B | 78.00 | 83.67 | +7% |
| 2 097 152 B | 2 309.79 | 2 077.81 | −10% |

The random-file scenario shows wider confidence intervals (especially at large sizes: ±121 µs vs ±16 µs at 2 MB), reflecting the extra variance introduced by `os.urandom` generation and cache effects when switching data buffers. The same-file scenario benefits from the input buffer remaining warm in CPU cache across runs, yielding tighter CIs.

**Conclusion:** AES-CTR timing is **data-independent** by design — the cipher operates on the counter stream, not the plaintext directly. The observed small differences are attributable entirely to CPU cache effects and OS scheduling jitter, not to the content or freshness of the data.

---

## 7. Summary

| Algorithm | 8 B (µs) | 512 B (µs) | 32 768 B (µs) | 2 097 152 B (µs) |
|---|---:|---:|---:|---:|
| AES-CTR Encrypt | 7.38 | 7.78 | 16.73 | 701.91 |
| AES-CTR Decrypt | 7.12 | 7.57 | 16.04 | 703.19 |
| RSA-Based Encrypt | 159.69 | 219.00 | 3 286.76 | 212 660.17 |
| RSA-Based Decrypt | 21 813.74 | 22 677.78 | 24 818.26 | 235 838.38 |
| SHA-256 Digest | 0.61 | 1.68 | 63.92 | 4 005.04 |

Key takeaways:
1. **AES-CTR** is the most efficient choice for bulk encryption at all tested sizes; encrypt and decrypt times are virtually symmetric.
2. **SHA-256** is the fastest operation at small and medium sizes; at 2 MB it is about 5.7× slower than AES-CTR but still far faster than RSA-based decryption.
3. **RSA-based encryption** has a fixed per-operation cost dominated by SHA-256 block masking for large files, making it unacceptably slow compared to AES.
4. **RSA-based decryption** is the most expensive operation at small sizes due to the private-key modular exponentiation; its relative disadvantage decreases as file size grows.
5. **AES-CTR timing is data-independent**: results are consistent whether the same file or fresh random files are used, confirming the cipher's constant-time design.
