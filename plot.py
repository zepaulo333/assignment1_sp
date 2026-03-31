import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np


def plot_results(aes_results, rsa_results, sha_results, output_dir="."):
    sizes = [r['size'] for r in aes_results]

    # Extrair dados
    y_aes_enc = [r['enc_mean'] for r in aes_results]
    y_aes_dec = [r['dec_mean'] for r in aes_results]
    y_rsa_enc = [r['enc_mean'] for r in rsa_results]
    y_rsa_dec = [r['dec_mean'] for r in rsa_results]
    y_sha     = [r['mean'] for r in sha_results]

    err_aes_enc = [r['enc_ci'] for r in aes_results]
    err_aes_dec = [r['dec_ci'] for r in aes_results]
    err_rsa_enc = [r['enc_ci'] for r in rsa_results]
    err_rsa_dec = [r['dec_ci'] for r in rsa_results]
    err_sha     = [r['ci'] for r in sha_results]

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.errorbar(sizes, y_aes_enc, yerr=err_aes_enc, label='AES-CTR Encrypt',
                fmt='-^', capsize=4, linewidth=2, markersize=7)
    ax.errorbar(sizes, y_aes_dec, yerr=err_aes_dec, label='AES-CTR Decrypt',
                fmt='-v', capsize=4, linewidth=2, markersize=7)
    ax.errorbar(sizes, y_sha, yerr=err_sha, label='SHA-256 Digest',
                fmt='-x', capsize=4, linewidth=2, markersize=7)
    ax.errorbar(sizes, y_rsa_enc, yerr=err_rsa_enc, label='RSA-Based Encrypt',
                fmt='-o', capsize=4, linewidth=2, markersize=7)
    ax.errorbar(sizes, y_rsa_dec, yerr=err_rsa_dec, label='RSA-Based Decrypt',
                fmt='-s', capsize=4, linewidth=2, markersize=7)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('File Size (Bytes)', fontsize=12)
    ax.set_ylabel('Execution Time (us)', fontsize=12)
    ax.set_title('Cryptographic Benchmarks — Full Comparison', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/plot_all_combined.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(sizes, y_aes_enc, yerr=err_aes_enc, label='AES-CTR Encrypt',
                fmt='-^', capsize=4, linewidth=2, markersize=7, color='#2196F3')
    ax.errorbar(sizes, y_aes_dec, yerr=err_aes_dec, label='AES-CTR Decrypt',
                fmt='-v', capsize=4, linewidth=2, markersize=7, color='#FF9800')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('File Size (Bytes)', fontsize=12)
    ax.set_ylabel('Execution Time (us)', fontsize=12)
    ax.set_title('AES-256 CTR — Encryption vs Decryption Times', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/plot_aes_enc_dec.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(sizes, y_rsa_enc, yerr=err_rsa_enc, label='RSA-Based Encrypt',
                fmt='-o', capsize=4, linewidth=2, markersize=7, color='#4CAF50')
    ax.errorbar(sizes, y_rsa_dec, yerr=err_rsa_dec, label='RSA-Based Decrypt',
                fmt='-s', capsize=4, linewidth=2, markersize=7, color='#F44336')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('File Size (Bytes)', fontsize=12)
    ax.set_ylabel('Execution Time (us)', fontsize=12)
    ax.set_title('RSA-Based — Encryption vs Decryption Times', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/plot_rsa_enc_dec.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(sizes, y_aes_enc, yerr=err_aes_enc, label='AES-CTR Encrypt',
                fmt='-^', capsize=4, linewidth=2, markersize=7, color='#2196F3')
    ax.errorbar(sizes, y_rsa_enc, yerr=err_rsa_enc, label='RSA-Based Encrypt',
                fmt='-o', capsize=4, linewidth=2, markersize=7, color='#4CAF50')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('File Size (Bytes)', fontsize=12)
    ax.set_ylabel('Execution Time (us)', fontsize=12)
    ax.set_title('AES Encryption vs RSA-Based Encryption', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/plot_aes_vs_rsa.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(sizes, y_aes_enc, yerr=err_aes_enc, label='AES-CTR Encrypt',
                fmt='-^', capsize=4, linewidth=2, markersize=7, color='#2196F3')
    ax.errorbar(sizes, y_sha, yerr=err_sha, label='SHA-256 Digest',
                fmt='-x', capsize=4, linewidth=2, markersize=7, color='#9C27B0')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('File Size (Bytes)', fontsize=12)
    ax.set_ylabel('Execution Time (us)', fontsize=12)
    ax.set_title('AES Encryption vs SHA-256 Digest Generation', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/plot_aes_vs_sha.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(sizes, y_sha, yerr=err_sha, label='SHA-256 Digest',
                fmt='-x', capsize=4, linewidth=2, markersize=7, color='#9C27B0')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('File Size (Bytes)', fontsize=12)
    ax.set_ylabel('Execution Time (us)', fontsize=12)
    ax.set_title('SHA-256 Digest Generation Times', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, which="both", ls="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/plot_sha256.png", dpi=200)
    plt.close(fig)
