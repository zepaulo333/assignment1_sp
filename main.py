from files_generation import generate_files
from crypto import generate_rsa_keypair
from benchmark import run_aes_benchmark, run_aes_variability_benchmark, run_rsa_benchmark, run_sha_benchmark
from plot import plot_results


def main():
    generate_files()

    aes_results = run_aes_benchmark()
    aes_variability_results = run_aes_variability_benchmark()

    e, d, n = generate_rsa_keypair(2048)
    rsa_results = run_rsa_benchmark(e, d, n)

    sha_results = run_sha_benchmark()

    plot_results(aes_results, rsa_results, sha_results)

    print("\n=== Assignment B extra analysis (same file vs random files, fixed size) ===")
    for r in aes_variability_results:
        print(
            f"Size {r['size']} B -> same-file mean: {r['same_mean']:.2f} µs (±{r['same_ci']:.2f}), "
            f"random-files mean: {r['random_mean']:.2f} µs (±{r['random_ci']:.2f})"
        )


if __name__ == "__main__":
    main()