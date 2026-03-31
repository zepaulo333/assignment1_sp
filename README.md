# Assignment 1 — Cryptographic Performance Benchmark

This project was developed for the **Security and Privacy** course to benchmark and compare the performance of:

- **AES-256 in CTR mode** (encryption and decryption)
- **RSA-based encryption scheme** with `H = SHA-256` (encryption and decryption)
- **SHA-256** digest generation

The benchmarks are executed for files with the following sizes (in bytes):

`8, 64, 512, 4096, 32768, 262144, 2097152`

---

## Project Structure

```
assignment1_sp/
├── main.py                      # runs the full benchmark pipeline
├── crypto.py                    # cryptographic implementations (AES, RSA-based, SHA-256)
├── benchmark.py                 # benchmark routines and statistics (mean + 95% CI)
├── files_generation.py          # generates random test files
├── plot.py                      # generates all benchmark plots
├── environment.yml              # Conda environment configuration
├── report.md                    # benchmark report
├── test_files/                  # generated test files (created at runtime)
└── plots/                       # generated plot images (created at runtime)
```

---

## Requirements

- Python 3.11 (recommended)
- `cryptography`
- `numpy`
- `matplotlib`

---

## Environment Setup

### Option 1 — Conda (recommended)

```bash
conda env create -f environment.yml
conda activate assignment1_sp
```

### Option 2 — pip

```bash
pip install cryptography numpy matplotlib
```

---

## How to Run

```bash
python3 main.py
```

---

## What the Program Does

When executed, the program:

1. Prints the experimental setup (OS, CPU, RAM, Python and library versions)
2. Generates random test files in the required sizes
3. Runs AES-256 CTR benchmark (encrypt/decrypt)
4. Runs AES variability analysis (same file repeatedly vs random files of fixed size)
5. Generates a 2048-bit RSA key pair and runs RSA-based benchmark
6. Runs SHA-256 benchmark
7. Generates the plot `benchmark_plot.png`
8. Prints a summary of the extra variability analysis

---

## Output

Expected outputs include:

- Console tables with:
  - AES encryption/decryption mean times and 95% CI
  - RSA-based encryption/decryption mean times and 95% CI
  - SHA-256 mean times and 95% CI
  - AES variability comparison (same file vs random files)
- Plot files (saved in the `plots/` directory):
  - `plot_all_combined.png`
  - `plot_aes_enc_dec.png`
  - `plot_rsa_enc_dec.png`
  - `plot_aes_vs_rsa.png`
  - `plot_aes_vs_sha.png`
  - `plot_sha256.png`

---

## Notes

- RSA-based benchmark can be significantly slower for large files.
- Test files are generated in the `test_files/` directory.
- The plot uses **log-log scale** (file size vs execution time in microseconds).
