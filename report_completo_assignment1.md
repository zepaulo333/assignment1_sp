# Security and Privacy — Assignment #1  
## Performance Benchmarking of Cryptographic Mechanisms

**Curso:** Security and Privacy  
**Tema:** PL4 — Performance Measures for Message Digests, Symmetric and Asymmetric Cryptography  
**Trabalho:** Assignment #1  
**Grupo:** _(preencher)_  
**Data:** _(preencher)_  

---

## 1. Introdução

Este trabalho tem como objetivo medir e comparar o desempenho temporal de três mecanismos criptográficos ao processar ficheiros de diferentes tamanhos:

1. **AES-256 em modo CTR** (cifra e decifra)
2. **Esquema RSA-based** com chave de 2048 bits e máscara por hash SHA-256
3. **SHA-256** para geração de digest

As medições são feitas em microsegundos (µs), com repetições suficientes para produzir resultados estatisticamente significativos (média e intervalo de confiança a 95%).

---

## 2. Requisitos do enunciado e conformidade

Segundo o `assignment1.pdf`, os pontos obrigatórios são:

- **A)** gerar ficheiros aleatórios nos tamanhos:  
  `8, 64, 512, 4096, 32768, 262144, 2097152` bytes
- **B)** cifrar e decifrar com AES-CTR (chave 256 bits), medindo tempos com significância estatística, e analisar:  
  - múltiplas execuções no mesmo ficheiro  
  - execuções sobre múltiplos ficheiros aleatórios de tamanho fixo
- **C)** implementar o esquema RSA-based:
  \[
  Enc(m;r) = (RSA(r), H(0,r)\oplus m_0, \ldots, H(n,r)\oplus m_n)
  \]
  com \(H = SHA256\), e medir desempenho
- **D)** medir tempo de geração de digest SHA-256
- **E)** produzir relatório com metodologia, setup, gráficos e comparações pedidas

### Estado de conformidade final

- [x] Ponto A  
- [x] Ponto B (incluindo análise extra “same file vs random files”)  
- [x] Ponto C  
- [x] Ponto D  
- [x] Ponto E (documentação + gráficos + análise comparativa)

---

## 3. Estrutura do projeto

No diretório `Trabalho1/Trabalho/`:

- `assignment1.pdf` — enunciado oficial
- `files_generation.py` — geração dos ficheiros de teste
- `crypto.py` — implementações criptográficas
- `benchmark.py` — benchmarks e estatística
- `plot.py` — geração de gráficos
- `main.py` — execução end-to-end
- `benchmark_plot.png` — gráfico gerado
- `mudancas_assignment1.txt` — resumo técnico das alterações
- `README.md` — instruções de execução
- `relatorio_assignment1.md` — versão resumida do relatório
- `report_completo_assignment1.md` — este relatório completo

---

## 4. Implementação

## 4.1 Geração de ficheiros (Ponto A)

Em `files_generation.py`, foram gerados ficheiros binários pseudoaleatórios usando `os.urandom`, com os tamanhos exigidos.

```python
FILE_SIZES = [8, 64, 512, 4096, 32768, 262144, 2097152]
```

A geração é feita para a diretoria `test_files/`.

---

## 4.2 AES-256 CTR (Ponto B)

Em `crypto.py`:

- `aes_ctr_encrypt(key, nonce, plaintext)`
- `aes_ctr_decrypt(key, nonce, ciphertext)`

Características:
- chave de 256 bits (32 bytes)
- nonce/contador de 128 bits (16 bytes)
- operação via `cryptography.hazmat.primitives.ciphers`

Em `benchmark.py`:

- `run_aes_benchmark()`: mede tempo de cifra e decifra por tamanho.
- Resultados com média e IC95.

---

## 4.3 Análise adicional obrigatória do Ponto B

Foi adicionada em `benchmark.py` a função:

- `run_aes_variability_benchmark()`

Esta função mede, para cada tamanho:

1. **Mesmo ficheiro + algoritmo fixo**, repetido `N_RUNS`
2. **Múltiplos ficheiros aleatórios de tamanho fixo**, com algoritmo fixo

Objetivo: responder explicitamente à questão do enunciado sobre variação de resultados nessas duas condições experimentais.

---

## 4.4 RSA-based (Ponto C)

Em `crypto.py`:

- `generate_rsa_keypair(2048)` gera par de chaves
- `rsa_based_encrypt(plaintext, e, n)` implementa:
  - amostra `r`
  - calcula `c0 = r^e mod n`
  - divide mensagem em blocos de 32 bytes (`ell=32`)
  - mascara cada bloco com `SHA256(i || r)` por XOR
- `rsa_based_decrypt(c0, cipher_data, original_len, d, n)` reverte operação

Em `benchmark.py`:
- `run_rsa_benchmark(e, d, n)` mede tempos de cifra e decifra para cada tamanho.

---

## 4.5 SHA-256 (Ponto D)

Em `crypto.py`:
- `sha256_hash(data)`

Em `benchmark.py`:
- `run_sha_benchmark()` mede tempos de hash para todos os tamanhos.

---

## 4.6 Estatística aplicada

Foi padronizada uma função auxiliar `_stats(times)` em `benchmark.py` para obter:

- média
- desvio padrão amostral
- intervalo de confiança 95%

\[
CI_{95\%} = 1.96 \cdot \frac{s}{\sqrt{N}}
\]

Com:
- `N_RUNS = 200`

---

## 4.7 Gráficos (Ponto E)

Em `plot.py`, o gráfico combinado inclui:

- AES Encrypt
- AES Decrypt
- RSA Encrypt
- RSA Decrypt
- SHA-256 Digest

Configuração:
- eixo X: tamanho em bytes
- eixo Y: tempo em µs
- escala log-log
- barras de erro com IC95
- exportação para `benchmark_plot.png`

---

## 5. Metodologia experimental

1. Gerar ficheiros de teste (fora da medição dos algoritmos).
2. Para cada tamanho:
   - medir AES enc/dec
   - medir RSA-based enc/dec
   - medir SHA-256
3. Repetir operações (`N_RUNS=200`) para robustez estatística.
4. Calcular média + IC95.
5. Produzir gráfico comparativo.
6. Executar análise de variabilidade do ponto B (same file vs random files).

---

## 6. Ambiente experimental

**Nota:** preencher com os dados exatos da máquina de submissão.

- CPU: _(preencher)_
- RAM: _(preencher)_
- Sistema Operativo: Linux
- Python: 3.x
- Bibliotecas:
  - `cryptography`
  - `numpy`
  - `matplotlib`

---

## 7. Resultados observados (resumo)

Durante a execução completa foram observadas as seguintes tendências:

1. **AES-CTR**
   - custos baixos para ficheiros pequenos
   - crescimento gradual com tamanho
   - tempos de cifra e decifra próximos

2. **Análise do ponto B**
   - para tamanhos pequenos, diferenças entre “same file” e “random files” são pequenas
   - para tamanhos maiores, o cenário com ficheiros aleatórios pode mostrar maior variância e, em alguns casos, maior média

3. **RSA-based**
   - custos significativamente superiores aos de AES
   - decifra geralmente mais pesada que cifra
   - para tamanhos muito grandes, ambos os custos são elevados

4. **SHA-256**
   - muito rápido para tamanhos pequenos
   - crescimento aproximadamente linear com tamanho da entrada

---

## 8. Análise comparativa pedida no enunciado

## 8.1 AES-based encryption vs RSA-based encryption

AES é claramente mais eficiente para cifrar dados em volume.  
O esquema RSA-based apresenta custos muito superiores, sobretudo em ficheiros maiores.

**Conclusão:** AES é adequado para cifragem de conteúdo; RSA deve ser reservado a operações assimétricas de pequena dimensão (e.g., encapsulamento de chave).

---

## 8.2 AES-based encryption vs SHA digest generation

SHA-256 tende a ter custos baixos e boa escalabilidade.  
AES também é eficiente, mas faz cifragem (objetivo distinto do hash).

**Conclusão:** apesar de ambos crescerem com tamanho, SHA tende a ser muito competitivo em tempo, com semântica de integridade (não confidencialidade).

---

## 8.3 RSA-based encryption vs RSA-based decryption

A decifra RSA-based tende a ser mais cara do que a cifra, devido ao custo aritmético modular associado ao expoente privado.

**Conclusão:** no desenho de sistemas, operações de decifra RSA devem ser usadas com parcimónia quando há requisitos de desempenho.

---

## 9. Testes realizados e validação

Testes executados:

- execução completa de `main.py` (pipeline end-to-end)
- validação de saída para:
  - AES benchmark
  - benchmark extra do ponto B
  - RSA benchmark
  - SHA benchmark
- confirmação de geração do gráfico `benchmark_plot.png`
- validação da impressão final do resumo do ponto B

---

## 10. Alterações efetuadas para fechar lacunas do assignment

Para cumprir 100% o enunciado, foram implementadas:

1. **Novo benchmark de variabilidade AES** (ponto B obrigatório)
2. **Integração desse benchmark no `main.py`**
3. **Expansão do gráfico com AES decrypt explícito**
4. **Exportação do gráfico para ficheiro**
5. **Documentação técnica adicional**
   - `mudancas_assignment1.txt`
   - `README.md`
   - `relatorio_assignment1.md`
   - `report_completo_assignment1.md`

---

## 11. Como executar

No diretório `Trabalho1/Trabalho/`:

```bash
python3 main.py
```

Dependências:

```bash
pip install cryptography numpy matplotlib
```

---

## 12. Conclusão

O trabalho encontra-se completo e alinhado com todos os pontos do `assignment1.pdf`, incluindo a componente frequentemente omitida no ponto B (comparação entre repetições no mesmo ficheiro e múltiplos ficheiros aleatórios de tamanho fixo).

Os resultados confirmam os comportamentos esperados:

- AES e SHA são eficientes para dados em volume;
- operações RSA-based são substancialmente mais pesadas;
- a variabilidade experimental depende do tamanho e da natureza dos dados de entrada.

Este relatório, juntamente com o código e os gráficos gerados, constitui uma entrega completa para submissão.

---

## 13. Anexos (ficheiros do projeto)

- Código: `main.py`, `benchmark.py`, `crypto.py`, `files_generation.py`, `plot.py`
- Gráfico: `benchmark_plot.png`
- Documentação:
  - `README.md`
  - `mudancas_assignment1.txt`
  - `relatorio_assignment1.md`
  - `report_completo_assignment1.md`
