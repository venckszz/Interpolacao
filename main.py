# Trabalho realizado para a disciplina de Algoritmos Numericos
# Alunos: Jonathan Alves, Leandro Grazziotin e Victor Toniato

from sympy import symbols, simplify, expand
import math

def verifica_condicoes(lista_pontos: list):
    
    # Verifica se foram passados menos de 2 pontos
    if len(lista_pontos) < 4:
        print("Inválido! São necessários ao menos 2 pontos para atender às condições")
        return False
    
    # Verifica se valores distintos foram inseridos
    valores_vistos = []
    for i, j in lista_pontos:
        if (i in valores_vistos):
            print("Inválido! É proibida a repetição do mesmo valor para as abcissas")
            return False

        else:
            valores_vistos.append(lista_pontos[i])
    
    return True


def construir_polinomio_Lagrange(lista_pontos: list):
    soma = 0
    
    # Declaracao de um X alvo
    x = symbols('x')
    
    # Itera por ponto e calcula a interpolacao pelo metodo de Lagrange
    for i, k in lista_pontos:
        produto = 1
        xi = i
        for j, l in lista_pontos:
            xj = j
            if xi == xj:
                 continue
            else:
                
                # Calcula o produtorio
                produto *= (x - xj) / (xi - xj)
        
        # Calcula o somatorio L(x) * f(x)
        soma += k * produto
    return soma


def construir_polinomio_Newton(lista_pontos: list):
    tamanho = len(lista_pontos)
    
    # Cria tabela para os valores de cada iteracao
    tabela = [[0.0 for _ in range(tamanho)] for _ in range(tamanho)]
    
    x = symbols('x')
    
    # Preenche a primeira coluna com os valores de y
    for i in range(tamanho):
        tabela[i][0] = lista_pontos[i][1]
    
    for j in range(1, tamanho):
        for i in range(tamanho - j):
            
            # Calcula o numerador pela formula f(x1) - f(x0)
            numerador = tabela[i + 1][j - 1] - tabela[i][j - 1]
            
            # Calcula o denominador pela formula x1 - x0
            denominador = lista_pontos[i + j][0] - lista_pontos[i][0]
            
            # Calcula o valor para a posicao atual da tabela pela formula f(x1) - f(x0) / x1 - x0
            tabela[i][j] = numerador / denominador
    
    resultado = tabela[0][0]
    produto = 1
    
    # Itera pela  quantidade de ponto e calcula a interpolacao pelo metodo de Newton
    for j in range(1, len(lista_pontos)):
        produto *= x - lista_pontos[j - 1][0]
        
        # Calcula o somatorio pela formula x0 + f(x0, x1, ..., xk) * (x -x0)(x - x1)...(x - xk-1)
        resultado += tabela[0][j] * produto
    
    return resultado
    

def calcula_ordenada(pontos: list, abcissa: float, metodo: int):
    x = symbols('x')
    
    # Calcula o polinomio e substitui o x pelo valor da abcissa informado
    if metodo == 1:
        resultado = construir_polinomio_Lagrange(pontos)
        polinomio_expandido = simplify(expand(resultado))
        ordenada = polinomio_expandido.subs(x, abcissa).evalf()
        print(f"\nA ordenada para x = {abcissa} é: {ordenada:.4f}")
    
    elif metodo == 2:
        resultado = construir_polinomio_Newton(pontos)
        polinomio_expandido = simplify(expand(resultado))
        ordenada = polinomio_expandido.subs(x, abcissa).evalf()
        print(f"\nA ordenada para x = {abcissa} é: {ordenada:.4f}")
    
    else:
        print("\nErro! Valor informado incompatível")
        return


def estima_erro_lagrange(pontos: list, abcissa: float):
    x = symbols('x')
    
    # Calcula o polinomio P(n+1)
    resultado1 = construir_polinomio_Lagrange(pontos)
    polinomio_expandido = simplify(expand(resultado1))
    ordenada1 = polinomio_expandido.subs(x, abcissa).evalf()
    
    # Calcula o polinomio P(n)
    lista_copiada = []
    lista_copiada.extend(pontos)
    lista_copiada.pop()
    resultado2 = construir_polinomio_Lagrange(lista_copiada)
    polinomio_expandido = simplify(expand(resultado2))
    ordenada2 = polinomio_expandido.subs(x, abcissa).evalf()
    
    # Aplica a formula E(x) = |P(n+1) - P(n)|
    erro = abs(ordenada1 - ordenada2)
    return erro 


def estima_erro_newton(pontos: list, abcissa: float):
    x = symbols('x')
    
    # Calcula o polinomio P(n+1)
    resultado1 = construir_polinomio_Newton(pontos)
    polinomio_expandido = simplify(expand(resultado1))
    ordenada1 = polinomio_expandido.subs(x, abcissa).evalf()
    
    lista_copiada = []
    lista_copiada.extend(pontos)
    lista_copiada.pop()
    
    # Calcula o polinomio P(n)
    resultado2 = construir_polinomio_Newton(lista_copiada)
    polinomio_expandido = simplify(expand(resultado2))
    ordenada2 = polinomio_expandido.subs(x, abcissa).evalf()
    
    # Aplica a formula E(x) = |P(n+1) - P(n)|
    erro = abs(ordenada1 - ordenada2)
    return erro


def funcionamento(opcao: int):
    if opcao == 1:
        lista_pontos = []
        
        print("\n=== Iniciando a verificação de pontos ===")
        qtd = int(input("Digite a quantidade de pontos que deseja informar: "))
        for i in range(qtd):
            ponto = list(map(float, input(f"Digite o ponto P{i + 1} (x,y): ").split()))
            x_ponto = ponto[0]
            y_ponto = ponto[1]
            lista_pontos.append([x_ponto, y_ponto])
        
        verifica_condicoes(lista_pontos)
        
    elif opcao == 2:
        print("\n=== Iniciando a interpolação pelo métdo de Lagrange ===")
        print("Digite a quantidade de pontos que deseja informar")
        
        qtd = int(input("Entrada: "))
        lista_pontos = []
        
        # Recebe os pontos de acordo com a quantidade informada pelo usuario
        for i in range(qtd):
            ponto = list(map(float, input(f"Digite o P{i + 1} (x,y): ").split()))
            x_ponto = ponto[0]
            y_ponto = ponto[1]
            lista_pontos.append([x_ponto, y_ponto])
        
        # Chama a funcao e simplifica para a impressao
        resultado = construir_polinomio_Lagrange(lista_pontos)
        polinomio_expandido = simplify(expand(resultado))
        print(f"\nPolinômio resultante: {polinomio_expandido}")
        
    elif opcao == 3:
        print("\n=== Iniciando a interpolação pelo método de Newton ===")
        print("Digite a quantidade de pontos que deseja informar")
        
        qtd = int(input("Entrada: "))
        lista_pontos = []
        
        # Recebe os pontos de acordo com a quantidade informada pelo usuario
        for i in range(qtd):
            ponto = list(map(float, input(f"Digite o ponto P{i + 1} (x,y): ").split()))
            x_ponto = ponto[0]
            y_ponto = ponto[1]
            lista_pontos.append([x_ponto, y_ponto])
        
        # Chama a funcao e simplifica para a impressao
        resultado = construir_polinomio_Newton(lista_pontos)
        polinomio_expandido = simplify(expand(resultado))
        print(f"\nPolinômio resultante: {polinomio_expandido}")
    
    elif opcao == 4:
        print("\n=== Iniciando o cálculo da função para um determinado ponto ===")
        print("Digite a quantidade de pontos que deseja informar")
        
        qtd = int(input("Entrada: "))
        lista_pontos = []
        
        # Recebe os pontos de acordo com a quantidade informada pelo usuario
        for i in range(qtd):
            ponto = list(map(float, input(f"Digite o ponto P{i + 1} (x,y): ").split()))
            x_ponto = ponto[0]
            y_ponto = ponto[1]
            lista_pontos.append([x_ponto, y_ponto])
        
        aux = int(input("Digite o método que deseja utilizar (1 - Lagrange ou 2 - Newton): "))
        abcissa = float(input("Digite o valor da abcissa para o ponto desejado: "))
        
        # Chama a funcao para calcular o valor de acordo com o metodo escolhido
        resultado = calcula_ordenada(lista_pontos, abcissa, aux)
    
    elif opcao == 5:
        print("\n=== Iniciando a estimativa de erro para o método de Lagrange ===")
        print("Digite a quantidade de pontos que deseja informar")
        
        qtd = int(input("Entrada: "))
        lista_pontos = []
        
        # Recebe os pontos de acordo com a quantidade informada pelo usuario
        for i in range(qtd):
            ponto = list(map(float, input(f"Digite o ponto P{i + 1} (x,y): ").split()))
            x_ponto = ponto[0]
            y_ponto = ponto[1]
            lista_pontos.append([x_ponto, y_ponto])
        
        abcissa = float(input("Digite o valor da abcissa para o ponto desejado: "))
        
        # Chama a funcao para calcular o valor de acordo com o metodo escolhido
        resultado = estima_erro_lagrange(lista_pontos, abcissa)
        print(f"Erro pelo metodo de Lagrange: {resultado:.4f}")
    
    elif opcao == 6:
        print("\n=== Iniciando a estimativa de erro para o método de Newton ===")
        print("Digite a quantidade de pontos que deseja informar")
        
        qtd = int(input("Entrada: "))
        lista_pontos = []
        
        # Recebe os pontos de acordo com a quantidade informada pelo usuario
        for i in range(qtd):
            ponto = list(map(float, input(f"Digite o ponto P{i + 1} (x,y): ").split()))
            x_ponto = ponto[0]
            y_ponto = ponto[1]
            lista_pontos.append([x_ponto, y_ponto])
        
        abcissa = float(input("Digite o valor da abcissa para o ponto desejado: "))
        
        # Chama a funcao para calcular o valor de acordo com o metodo escolhido
        resultado = estima_erro_lagrange(lista_pontos, abcissa)
        print(f"Erro pelo metodo de Newton: {resultado:.4f}")
    
        
    elif opcao == 7:
        print("Encerrando o programa...")
        

def main():
    
    aux = 1
    while (aux != 0):
        print("\n======= Menu de Opções =======")
        print("1. Verificar a validade dos pontos")
        print("2. Construir polinômio pelo método de Lagrande")
        print("3. Construir polinômio pelo método de Newton")
        print("4. Avaliar a função em um ponto informado")
        print("5. Estimar o erro do método de Lagrange")
        print("6. Estimar o erro do método de Newton")
        print("7. Sair")
    
        opcao = int(input("Escolha: "))
        funcionamento(opcao)
        
        if(opcao == 7): aux = 0


if __name__ == "__main__":
    main()
