# Desafio de Automação Digital: Gestão de Peças, Qualidade e Armazenamento

## 🎯 Visão Geral do Projeto

[cite_start]Este projeto consiste em um protótipo de software em Python para automatizar o controle de qualidade e a gestão de estoque (caixas) de peças industriais[cite: 62]. [cite_start]O objetivo é substituir a inspeção manual, que gera atrasos, falhas de conferência e aumento no custo de operação[cite: 63].

---

## ⚙️ Explicação Detalhada do Funcionamento

O sistema é construído em torno de três lógicas principais, organizadas em funções:

### 1. Avaliação de Qualidade (`avaliar_peca`)
[cite_start]Esta função aplica os critérios de aprovação[cite: 66]:
* [cite_start]**Peso:** Entre 95g e 105g[cite: 67].
* [cite_start]**Cor:** Azul ou Verde[cite: 69].
* [cite_start]**Comprimento:** Entre 10cm e 20cm[cite: 70].
* **Lógica:** O sistema usa condicionais (estrutura de decisão) para determinar se a peça é aprovada (se todos os critérios forem atendidos) ou reprovada (se houver falha em um ou mais critérios).

### 2. Gestão de Caixas e Estoque (`cadastrar_nova_peca`)
* [cite_start]As peças aprovadas são armazenadas em caixas de capacidade limitada: 10 peças por caixa[cite: 71].
* [cite_start]O sistema fecha a caixa quando atinge a capacidade máxima e inicia uma nova[cite: 72].
* **Lógica:** Este processo utiliza o loop e a condição de controle para automatizar a separação.

### 3. Remoção Robusta e Relatórios
* **Remoção (Opção 3):** A lógica de remoção localiza a peça por ID e a remove de forma completa, atualizando os contadores globais e as listas de caixas, garantindo a integridade dos dados.
* [cite_start]**Relatório (Opção 5):** Gera relatórios consolidados com o total de peças aprovadas/reprovadas e a quantidade de caixas utilizadas[cite: 73, 75, 76].

---

## 💻 Como Rodar o Programa (Passo a Passo)

Para executar o sistema, você deve ter o Python instalado (versão 3.x).

1.  **Baixe/Clone** este repositório para o seu computador.
2.  Abra o Terminal ou PowerShell na pasta raiz do projeto.
3.  Execute o script com o comando:
    ```bash
    python automacao_industrial.py
    ```
4.  O Menu Interativo será iniciado, permitindo o cadastro e a gestão das peças.

## 📝 Exemplos de Entradas e Saídas

| Ação | ID / Peso / Cor / Comp. | Saída do Sistema |
| :--- | :--- | :--- |
| **Peça Aprovada** | P001 / 100g / Azul / 15cm | ✅ PEÇA P001 APROVADA (1/10). |
| **Peça Reprovada** | P002 / 50g / Vermelho / 5cm | ❌ PEÇA P002 REPROVADA. Motivo: Peso Incorreto, Cor Incorreta, Comprimento Incorreto. |
| **Fechamento de Caixa**| (Após cadastrar a 10ª peça aprovada) | 📦 CAIXA FECHADA! Capacidade máxima atingida. |
