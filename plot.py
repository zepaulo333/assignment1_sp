import matplotlib.pyplot as plt


def plot_results(aes_results, rsa_results, sha_results):
    sizes = [r['size'] for r in aes_results]

    y_aes_enc = [r['enc_mean'] for r in aes_results]
    y_aes_dec = [r['dec_mean'] for r in aes_results]
    y_rsa_enc = [r['enc_mean'] for r in rsa_results]
    y_rsa_dec = [r['dec_mean'] for r in rsa_results]
    y_sha = [r['mean'] for r in sha_results]

    err_aes_enc = [r['enc_ci'] for r in aes_results]
    err_aes_dec = [r['dec_ci'] for r in aes_results]
    err_rsa_enc = [r['enc_ci'] for r in rsa_results]
    err_rsa_dec = [r['dec_ci'] for r in rsa_results]
    err_sha = [r['ci'] for r in sha_results]

    plt.figure(figsize=(12, 7))

    plt.errorbar(sizes, y_aes_enc, yerr=err_aes_enc, label='AES-256 CTR Encrypt', fmt='-^', capsize=4)
    plt.errorbar(sizes, y_aes_dec, yerr=err_aes_dec, label='AES-256 CTR Decrypt', fmt='-v', capsize=4)
    plt.errorbar(sizes, y_sha, yerr=err_sha, label='SHA-256 Digest', fmt='-x', capsize=4)
    plt.errorbar(sizes, y_rsa_enc, yerr=err_rsa_enc, label='RSA-Based Encrypt', fmt='-o', capsize=4)
    plt.errorbar(sizes, y_rsa_dec, yerr=err_rsa_dec, label='RSA-Based Decrypt', fmt='-s', capsize=4)

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('File Size (Bytes)')
    plt.ylabel('Execution Time (us)')
    plt.title('Cryptographic Benchmarks Comparison (Log-Log Scale)')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig("benchmark_plot.png", dpi=200)
    plt.show()
