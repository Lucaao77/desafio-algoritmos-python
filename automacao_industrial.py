# =================================================================
# VARIÁVEIS GLOBAIS DE ARMAZENAMENTO
# =================================================================

pecas_cadastradas = []
caixa_atual = []       # Caixa em preenchimento (máx. 10 peças)
caixas_fechadas = []   # Caixas completas
total_aprovadas = 0
total_reprovadas = 0

reprovacao_motivos = {
    "Peso Incorreto": 0,
    "Cor Incorreta": 0,
    "Comprimento Incorreto": 0
}

CAPACIDADE_CAIXA = 10

# =================================================================
# FUNÇÃO CENTRAL DE QUALIDADE
# =================================================================
def avaliar_peca(peca):
    """
    Avalia a peça com base nos critérios:
    - Peso: 95g a 105g
    - Cor: azul ou verde
    - Comprimento: 10cm a 20cm
    Retorna ('Aprovada' ou 'Reprovada', motivo ou 'N/A')
    """
    peso = peca['peso']
    cor = peca['cor'].lower()
    comprimento = peca['comprimento']
    reprovado_por = []

    if not (95 <= peso <= 105):
        reprovado_por.append("Peso Incorreto")
    if cor not in ("azul", "verde"):
        reprovado_por.append("Cor Incorreta")
    if not (10 <= comprimento <= 20):
        reprovado_por.append("Comprimento Incorreto")

    if reprovado_por:
        return "Reprovada", ", ".join(reprovado_por)
    return "Aprovada", "N/A"

# =================================================================
# FUNÇÃO DE CADASTRO DE PEÇAS E GERENCIAMENTO DE CAIXAS
# =================================================================
def cadastrar_nova_peca():
    global total_aprovadas, total_reprovadas
    global caixa_atual, caixas_fechadas

    print("\n--- CADASTRO DE NOVA PEÇA ---")
    try:
        id_peca = input("ID da Peça: ").strip()
        peso = float(input("Peso da Peça (g): "))
        cor = input("Cor da Peça: ").strip()
        comprimento = float(input("Comprimento da Peça (cm): "))
    except ValueError:
        print("ERRO: Peso e Comprimento devem ser números válidos.")
        return

    peca = {'id': id_peca, 'peso': peso, 'cor': cor, 'comprimento': comprimento}
    status, motivo = avaliar_peca(peca)
    peca['status'] = status
    peca['motivo'] = motivo
    pecas_cadastradas.append(peca)

    if status == "Aprovada":
        total_aprovadas += 1
        caixa_atual.append(peca)
        print(f"\n✅ PEÇA {peca['id']} APROVADA ({len(caixa_atual)}/10).")

        if len(caixa_atual) >= CAPACIDADE_CAIXA:
            caixas_fechadas.append(caixa_atual)
            caixa_atual = []
            print("📦 CAIXA FECHADA! Capacidade máxima atingida.")
    else:
        total_reprovadas += 1
        print(f"\n❌ PEÇA {peca['id']} REPROVADA. Motivo: {motivo}")
        for m in motivo.split(', '):
            if m in reprovacao_motivos:
                reprovacao_motivos[m] += 1

# =================================================================
# FUNÇÃO DE REMOÇÃO ROBUSTA (Versão para pontuação máxima)
# =================================================================
def remover_peca_cadastrada():
    """
    Remove uma peça cadastrada de forma completa:
    - Atualiza contadores de aprovadas/reprovadas
    - Remove da caixa_atual ou caixas_fechadas (se existir)
    - Atualiza motivos de reprovação (se necessário)
    """
    global pecas_cadastradas, caixa_atual, caixas_fechadas
    global total_aprovadas, total_reprovadas, reprovacao_motivos

    print("\n--- REMOVER PEÇA ---")
    id_para_remover = input("Digite o ID da peça para remover: ").strip()

    # Localizar a peça no cadastro geral
    peca_encontrada = None
    for p in pecas_cadastradas:
        if p['id'] == id_para_remover:
            peca_encontrada = p
            break

    if not peca_encontrada:
        print(f"ERRO: Peça com ID {id_para_remover} não encontrada.")
        return

    # 1️⃣ Atualizar contadores globais
    if peca_encontrada['status'] == "Aprovada":
        total_aprovadas = max(0, total_aprovadas - 1)
    else:
        total_reprovadas = max(0, total_reprovadas - 1)
        for m in peca_encontrada['motivo'].split(', '):
            if m in reprovacao_motivos and reprovacao_motivos[m] > 0:
                reprovacao_motivos[m] -= 1

    # 2️⃣ Remover da caixa atual (se estiver lá)
    for p in list(caixa_atual):
        if p['id'] == id_para_remover:
            caixa_atual.remove(p)
            print(f"🔄 Peça {id_para_remover} removida da caixa atual.")
            break

    # 3️⃣ Remover de caixas fechadas (caso a peça esteja lá)
    for caixa in caixas_fechadas:
        for p in list(caixa):
            if p['id'] == id_para_remover:
                caixa.remove(p)
                print(f"🔄 Peça {id_para_remover} removida de uma caixa fechada.")
                if len(caixa) == 0:
                    caixas_fechadas.remove(caixa)
                    print("📦 Caixa estava vazia e foi removida.")
                break

    # 4️⃣ Remover da lista geral
    pecas_cadastradas.remove(peca_encontrada)
    print(f"✅ Peça {id_para_remover} removida com sucesso e contadores atualizados!")

# =================================================================
# FUNÇÕES DE RELATÓRIO E LISTAGEM
# =================================================================
def gerar_relatorio_final():
    print("\n=============================================")
    print("        RELATÓRIO CONSOLIDADO DE PRODUÇÃO")
    print("=============================================")
    print(f"Total de Peças Aprovadas: {total_aprovadas}")
    print(f"Total de Peças Reprovadas: {total_reprovadas}")

    print("\nMOTIVOS DE REPROVAÇÃO:")
    for motivo, contagem in reprovacao_motivos.items():
        print(f"  - {motivo}: {contagem}")

    total_caixas_utilizadas = len(caixas_fechadas) + (1 if caixa_atual else 0)
    print("\nGERENCIAMENTO DE CAIXAS:")
    print(f"Caixas Fechadas: {len(caixas_fechadas)}")
    print(f"Peças na Caixa Atual: {len(caixa_atual)}")
    print(f"Total de Caixas Utilizadas: {total_caixas_utilizadas}")
    print("=============================================")

def listar_pecas_por_status():
    print("\n--- LISTAGEM DE PEÇAS ---")
    aprovadas = [p for p in pecas_cadastradas if p['status'] == 'Aprovada']
    reprovadas = [p for p in pecas_cadastradas if p['status'] == 'Reprovada']

    print(f"\nAPROVADAS ({len(aprovadas)}):")
    if aprovadas:
        for p in aprovadas:
            print(f"  ID: {p['id']} | Peso: {p['peso']}g | Cor: {p['cor']} | Comp.: {p['comprimento']}cm")
    else:
        print("  (Nenhuma peça aprovada ainda.)")

    print(f"\nREPROVADAS ({len(reprovadas)}):")
    if reprovadas:
        for p in reprovadas:
            print(f"  ID: {p['id']} | Motivo: {p['motivo']}")
    else:
        print("  (Nenhuma peça reprovada ainda.)")

def listar_caixas_fechadas():
    print("\n--- CAIXAS FECHADAS ---")
    if not caixas_fechadas:
        print("Nenhuma caixa foi fechada ainda.")
        return
    for i, caixa in enumerate(caixas_fechadas, 1):
        ids = ", ".join([p['id'] for p in caixa])
        print(f"📦 Caixa {i} ({len(caixa)}/10 peças) | IDs: {ids}")

# =================================================================
# MENU PRINCIPAL
# =================================================================
def menu_interativo():
    while True:
        print("\n=============================================")
        print("        DESAFIO DE AUTOMAÇÃO DIGITAL")
        print("=============================================")
        print("1. Cadastrar nova peça")
        print("2. Listar peças aprovadas/reprovadas")
        print("3. Remover peça cadastrada")
        print("4. Listar caixas fechadas")
        print("5. Gerar relatório final")
        print("0. Sair")
        print("---------------------------------------------")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_nova_peca()
        elif opcao == '2':
            listar_pecas_por_status()
        elif opcao == '3':
            remover_peca_cadastrada()
        elif opcao == '4':
            listar_caixas_fechadas()
        elif opcao == '5':
            gerar_relatorio_final()
        elif opcao == '0':
            print("Encerrando o sistema. Obrigado!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# =================================================================
# EXECUÇÃO DO PROGRAMA
# =================================================================
if __name__ == "__main__":
    menu_interativo()
