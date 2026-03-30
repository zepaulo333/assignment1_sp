# Assignment #1 - Cryptographic Performance Benchmark

Projeto da cadeira **Security and Privacy** para medir desempenho de:
- **AES-256 CTR** (encrypt/decrypt)
- **RSA-based** (encrypt/decrypt) com `H = SHA-256`
- **SHA-256** (digest)

para ficheiros com tamanhos:
`8, 64, 512, 4096, 32768, 262144, 2097152` bytes.

---

## Estrutura

- `main.py` - executa o fluxo completo
- `files_generation.py` - gera ficheiros de teste
- `crypto.py` - implementações criptográficas
- `benchmark.py` - benchmarks e estatística (média + IC95)
- `plot.py` - geração de gráfico (`benchmark_plot.png`)
- `assignment1.pdf` - enunciado
- `relatorio_assignment1.md` - relatório em Markdown
- `mudancas_assignment1.txt` - registo das alterações

---

## Ambiente

### Com Conda (recomendado)

```bash
conda env create -f environment.yml
conda activate assignment1_sp
```

### Com pip

```bash
pip install cryptography numpy matplotlib
```

---

## Como executar

No diretório `Trabalho1/Trabalho`:

```bash
python3 main.py
```

Isto vai:
1. gerar os ficheiros de teste;
2. correr benchmark de AES;
3. correr benchmark extra do ponto B (mesmo ficheiro vs ficheiros aleatórios de tamanho fixo);
4. correr benchmark RSA;
5. correr benchmark SHA-256;
6. gerar gráfico `benchmark_plot.png`;
7. imprimir resumo da análise do ponto B no terminal.

---

## Saídas esperadas

- Tabelas no terminal com médias e **IC 95%** para AES, RSA e SHA.
- Tabela extra do ponto B:
  - same-file mean ± CI
  - random-files mean ± CI
- Gráfico:
  - `benchmark_plot.png`

---

## Conformidade com o assignment1.pdf

- [x] Geração de ficheiros nos tamanhos exigidos
- [x] AES-CTR 256-bit (encrypt/decrypt) com significância estatística
- [x] Análise pedida no ponto B (mesmo ficheiro vs ficheiros aleatórios)
- [x] RSA-based com SHA-256 (encrypt/decrypt) e benchmark
- [x] SHA-256 benchmark
- [x] Gráfico com X em bytes e Y em microsegundos

---

## Notas

- O benchmark RSA para ficheiros grandes pode demorar significativamente mais.
- Para submissão, usar também:
  - `relatorio_assignment1.md`
  - `mudancas_assignment1.txt`
  - código-fonte comprimido (conforme pedido no enunciado).
