# A/B Testing Statistical Framework

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![R](https://img.shields.io/badge/R-4.0+-276DC3.svg)
![SciPy](https://img.shields.io/badge/SciPy-1.11+-8CAAE6.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Comprehensive A/B testing framework with statistical tests, power analysis, and sequential testing**

[English](#english) | [Português](#português)

</div>

---

## English

### 📋 Overview

Professional A/B testing framework implementing rigorous statistical methods for experiment design and analysis. Features include sample size calculation, power analysis, multiple testing correction, sequential testing, Bayesian A/B testing, multi-armed bandits, and comprehensive reporting.

### 🎯 Key Features

- **Statistical Tests**: t-test, chi-square, Mann-Whitney, ANOVA
- **Power Analysis**: Sample size and effect size calculation
- **Sequential Testing**: Early stopping with alpha spending
- **Bayesian Methods**: Bayesian A/B testing with credible intervals
- **Multi-armed Bandits**: Thompson sampling, UCB
- **Multiple Testing**: Bonferroni, Benjamini-Hochberg correction
- **Visualization**: Confidence intervals, posterior distributions
- **Reporting**: Automated experiment reports with insights

### 🚀 Quick Start

```bash
git clone https://github.com/galafis/ab-testing-statistical-framework.git
cd ab-testing-statistical-framework
pip install -r requirements.txt

# Calculate sample size
python src/utils/sample_size.py \
  --baseline-rate 0.10 \
  --mde 0.02 \
  --power 0.80

# Run A/B test
python src/models/ab_test.py \
  --control data/control.csv \
  --treatment data/treatment.csv \
  --metric conversion_rate

# Bayesian analysis
python src/models/bayesian_test.py \
  --data data/experiment.csv \
  --prior beta
```

### 📊 Test Results Example

| Metric | Control | Treatment | Lift | p-value | Significant |
|--------|---------|-----------|------|---------|-------------|
| Conversion | 10.2% | 12.5% | +22.5% | 0.003 | ✓ |
| Revenue | $45.30 | $48.90 | +7.9% | 0.042 | ✓ |
| Engagement | 3.2 min | 3.4 min | +6.3% | 0.156 | ✗ |

### 👤 Author

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)

---

## Português

### 📋 Visão Geral

Framework profissional de testes A/B implementando métodos estatísticos rigorosos para design e análise de experimentos. Recursos incluem cálculo de tamanho de amostra, análise de poder, correção para testes múltiplos, testes sequenciais, testes A/B bayesianos, multi-armed bandits e relatórios abrangentes.

### 🎯 Características Principais

- **Testes Estatísticos**: t-test, qui-quadrado, Mann-Whitney, ANOVA
- **Análise de Poder**: Cálculo de tamanho de amostra e tamanho de efeito
- **Testes Sequenciais**: Parada antecipada com alpha spending
- **Métodos Bayesianos**: Testes A/B bayesianos com intervalos credíveis
- **Multi-armed Bandits**: Thompson sampling, UCB
- **Testes Múltiplos**: Correção de Bonferroni, Benjamini-Hochberg
- **Visualização**: Intervalos de confiança, distribuições posteriores
- **Relatórios**: Relatórios automatizados de experimentos com insights

### 👤 Autor

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
