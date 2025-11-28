import datetime

# Dicionário para armazenar todos os orçamentos, onde a chave é o Mês/Ano (ex: '2025-11')
orcamento_mensal = {}

def obter_mes_ano_simplificado():
    """Pede ao usuário apenas o número do mês e usa o ano atual."""
    
    # 1. Obtém o ano atual do sistema
    ano_atual = datetime.date.today().year
    
    while True:
        mes_str = input(f"Ano: {ano_atual} - Mês: ")
        try:
            mes_num = int(mes_str)
            if 1 <= mes_num <= 12:
                # Formata o mês com zero à esquerda (ex: 5 -> '05')
                mes_formatado = f"{mes_num:02d}"
                # Retorna a chave no formato AAAA-MM
                return f"{ano_atual}-{mes_formatado}"
            else:
                print("❌ Mês inválido. Digite um número entre 1 e 12.")
        except ValueError:
            print("❌ Entrada inválida. Digite um número inteiro para o mês.")

def adicionar_registro(descricao, valor, tipo, mes_ano):
    """Adiciona um novo registro ao mês/ano especificado."""
    tipo = tipo.lower()
    if tipo not in ['receita', 'despesa']:
        print("🚨 Erro: O tipo deve ser 'receita' ou 'despesa'.")
        return

    try:
        valor = float(valor)
        if valor <= 0:
            print("🚨 Erro: O valor deve ser positivo.")
            return

        if tipo == 'despesa':
            valor = -valor  # Despesa é armazenada como valor negativo
    except ValueError:
        print("🚨 Erro: Valor inválido. Insira um número.")
        return

    # Garante que o mês/ano existe no dicionário principal
    if mes_ano not in orcamento_mensal:
        orcamento_mensal[mes_ano] = []
        
    novo_registro = {
        'descricao': descricao,
        'valor': valor,
        'tipo': tipo
    }
    orcamento_mensal[mes_ano].append(novo_registro)
    print(f"\n✅ Registro de '{descricao}' ({tipo}) adicionado para {mes_ano} com sucesso.")

def visualizar_registros():
    """Exibe todos os registros de orçamento, organizados por mês."""
    if not orcamento_mensal:
        print("\n📝 Nenhum registro cadastrado ainda.")
        return

    print("\n--- 📝 Registros de Orçamento Mensal ---")
    
    # Ordena os meses (chaves) do dicionário cronologicamente
    meses_ordenados = sorted(orcamento_mensal.keys())

    for mes_ano in meses_ordenados:
        registros_do_mes = orcamento_mensal[mes_ano]
        
        if not registros_do_mes:
            continue

        saldo_mes = sum(registro['valor'] for registro in registros_do_mes)
        
        print(f"\n*** MÊS: {mes_ano} (Saldo: R$ {saldo_mes:.2f}) ***")
        
        for i, registro in enumerate(registros_do_mes):
            sinal = "+" if registro['valor'] > 0 else ""
            cor = "🟢" if registro['tipo'] == 'receita' else "🔴"

            print(f"  {i+1}. {cor} {registro['descricao']}: {sinal}{registro['valor']:.2f} ({registro['tipo'].capitalize()})")
            
    print("---------------------------------")

def calcular_saldo_total():
    """Calcula e exibe o saldo total acumulado de todos os meses."""
    saldo_total = 0
    
    for mes_ano, registros_do_mes in orcamento_mensal.items():
        saldo_mes = sum(registro['valor'] for registro in registros_do_mes)
        saldo_total += saldo_mes

    if saldo_total >= 0:
        mensagem = "Seu saldo geral está positivo! 🎉"
    else:
        mensagem = "Seu saldo geral está negativo. 😥"
        
    print(f"\n--- 📊 Saldo Total Acumulado ---")
    print(f"Saldo Geral: R$ {saldo_total:.2f}")
    print(mensagem)
    print("------------------------")

def menu():
    """Função principal para o menu de interação."""
    while True:
        print("\n*** Menu de Orçamento Mensal ***")
        print("1. Adicionar Receita")
        print("2. Adicionar Despesa")
        print("3. Visualizar Registros Mensais")
        print("4. Calcular Saldo Geral Acumulado")
        print("5. Sair")

        escolha = input("Escolha uma opção (1-5): ")

        if escolha == '1' or escolha == '2':
            tipo_registro = 'receita' if escolha == '1' else 'despesa'
            print(f"\n--- Adicionar {tipo_registro.capitalize()} ---")
            
            # Pede o mês (simplificado)
            mes_ano = obter_mes_ano_simplificado()
            
            descricao = input("Descrição: ")
            valor_str = input("Valor: ")
            
            adicionar_registro(descricao, valor_str, tipo_registro, mes_ano)
            
        elif escolha == '3':
            visualizar_registros()
            
        elif escolha == '4':
            calcular_saldo_total()
            
        elif escolha == '5':
            print(" Saindo do sistema! ")
            break
            
        else:
            print("❌ Opção inválida. Tente novamente.")

# Inicia o sistema
if __name__ == "__main__":
    menu()