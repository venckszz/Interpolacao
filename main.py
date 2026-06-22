# Trabalho realizado para a disciplina de Algoritmos Numericos
# Alunos: Jonathan Alves, Leandro Grazziotin e Victor Toniato

from sympy import symbols, expand

def verifica_condicoes(lista_pontos: list, quantidade_pontos: int, ):

    # Limpa a lista antes de alocar novos valores
    lista_pontos.clear()

    for i in range(quantidade_pontos):
        ponto = list(map(float, input(f"Digite o P{i + 1} (x,y): ").split()))
        x_ponto = ponto[0]
        y_ponto = ponto[1]
        lista_pontos.append([x_ponto, y_ponto])
    
    # Verifica se foram passados menos de 2 pontos
    if len(lista_pontos) < 2:
        print("Inválido! São necessários ao menos 2 pontos para atender às condições")
        return False
    
    # Verifica se valores distintos foram inseridos
    valores_vistos = []
    for i, j in lista_pontos:
        if (i in valores_vistos):
            print("Inválido! É proibida a repetição do mesmo valor para as abcissas")
            return False

        else:
            valores_vistos.append(i)
    
    print("\nVálido! Os pontos que digitou atendem aos requisitos.")
    return lista_pontos


def construir_polinomio_Lagrange(lista_pontos: list):

    if len(lista_pontos) < 2:
        print("Erro! Deve-se inserir inicialmente pelo menos 2 pontos.")
        return

    else:
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

    if len(lista_pontos) < 2:
        print("Erro! Deve-se inserir inicialmente pelo menos 2 pontos.")
        return

    else:
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
    

def calcula_ordenada(lista_pontos: list, abscissa: float, metodo: int):

    if len(lista_pontos) < 2:
        print("Erro! Deve-se inserir inicialmente pelo menos 2 pontos.")
        return

    else:
    
        x = symbols('x')
        
        # Calcula o polinomio e substitui o x pelo valor da abcissa informado
        if metodo == 1:
            resultado = construir_polinomio_Lagrange(lista_pontos)
            polinomio_expandido = expand(resultado)
            ordenada = polinomio_expandido.subs(x, abscissa).evalf()
            print(f"\nA ordenada para x = {abscissa} é: {ordenada:.4f}")
        
        elif metodo == 2:
            resultado = construir_polinomio_Newton(lista_pontos)
            polinomio_expandido = expand(resultado)
            ordenada = polinomio_expandido.subs(x, abscissa).evalf()
            print(f"\nA ordenada para x = {abscissa} é: {ordenada:.4f}")
        
        else:
            print("\nErro! Valor informado incompatível")
            return


def estima_erro_lagrange(lista_pontos: list, abscissa: float):

    if len(lista_pontos) < 2:
        print("Erro! Deve-se inserir inicialmente pelo menos 2 pontos.")
        return

    else:
        x = symbols('x')
        
        # Calcula o polinomio P(n+1)
        resultado1 = construir_polinomio_Lagrange(lista_pontos)
        polinomio_expandido = expand(resultado1)
        ordenada1 = polinomio_expandido.subs(x, abscissa).evalf()
        
        # Calcula o polinomio P(n)
        lista_copiada = []
        lista_copiada.extend(lista_pontos)
        lista_copiada.pop()
        resultado2 = construir_polinomio_Lagrange(lista_copiada)
        polinomio_expandido = expand(resultado2)
        ordenada2 = polinomio_expandido.subs(x, abscissa).evalf()
        
        # Aplica a formula E(x) = |P(n+1) - P(n)|
        erro = abs(ordenada1 - ordenada2)
        return erro 


def estima_erro_newton(lista_pontos: list, abscissa: float):

    if len(lista_pontos) < 2:
        print("Erro! Deve-se inserir inicialmente pelo menos 2 pontos.")
        return
    
    else:    
        x = symbols('x')
        
        # Calcula o polinomio P(n+1)
        resultado1 = construir_polinomio_Newton(lista_pontos)
        polinomio_expandido = expand(resultado1)
        ordenada1 = polinomio_expandido.subs(x, abscissa).evalf()
        
        lista_copiada = []
        lista_copiada.extend(lista_pontos)
        lista_copiada.pop()
        
        # Calcula o polinomio P(n)
        resultado2 = construir_polinomio_Newton(lista_copiada)
        polinomio_expandido = expand(resultado2)
        ordenada2 = polinomio_expandido.subs(x, abscissa).evalf()
        
        # Aplica a formula E(x) = |P(n+1) - P(n)|
        erro = abs(ordenada1 - ordenada2)
        return erro


def funcionamento(lista_pontos: list, opcao: int):
    
    if opcao == 1:
        print("\n======= Iniciando a inserção e verificação de pontos =======")
        print("\nDigite a quantidade de pontos que deseja informar")

        # Recebe os pontos de acordo com a quantidade informada pelo usuario
        qtd = int(input("\nEntrada: "))

        verifica_condicoes(lista_pontos, qtd)
        
    elif opcao == 2:
        print("\n=== Iniciando a interpolação pelo métdo de Lagrange ===")
        
        # Chama a funcao e simplifica para a impressao
        resultado = construir_polinomio_Lagrange(lista_pontos)

        # retorna para a main caso não hajam pontos alocados
        if resultado is None:
            return
        
        print(f"\nPolinômio resultante: {resultado}")
        polinomio_expandido = expand(resultado)
        print(f"\nPolinômio expandido resultante: {polinomio_expandido}")
        
    elif opcao == 3:
        print("\n=== Iniciando a interpolação pelo método de Newton ===")
        
        # Chama a funcao e simplifica para a impressao
        resultado = construir_polinomio_Newton(lista_pontos)

        if resultado is None:
            return
        
        print(f"\nPolinômio resultante: {resultado}")
        polinomio_expandido = expand(resultado)
        print(f"\nPolinômio resultante: {polinomio_expandido}")
    
    elif opcao == 4:
        if len(lista_pontos) < 2:
            print("Você deve primeiro definir os pontos!")
            return
        
        print("\n=== Iniciando o cálculo da função para um determinado ponto ===")
        
        aux = int(input("Digite o método que deseja utilizar (1 - Lagrange ou 2 - Newton): "))
        abscissa = float(input("Digite o valor da abscissa para o ponto desejado: "))
        
        # Chama a funcao para calcular o valor de acordo com o metodo escolhido
        resultado = calcula_ordenada(lista_pontos, abscissa, aux)
    
    elif opcao == 5:
        if len(lista_pontos) < 2:
            print("Você deve primeiro definir os pontos!")
            return
        
        print("\n=== Iniciando a estimativa de erro para o método de Lagrange ===")

        abscissa = float(input("Digite o valor da abcissa para o ponto desejado: "))
        
        # Chama a funcao para calcular o valor de acordo com o metodo escolhido
        resultado = estima_erro_lagrange(lista_pontos, abscissa)
        print(f"\nErro pelo metodo de Lagrange: {resultado}")
    
    elif opcao == 6:
        if len(lista_pontos) < 2:
            print("Você deve primeiro definir os pontos!")
            return
        
        print("\n=== Iniciando a estimativa de erro para o método de Newton ===")
        
        abscissa = float(input("Digite o valor da abcissa para o ponto desejado: "))
        
        # Chama a funcao para calcular o valor de acordo com o metodo escolhido
        resultado = estima_erro_lagrange(lista_pontos, abscissa)
        print(f"\nErro pelo metodo de Newton: {resultado}")
        

def main():
    
    aux = 1
    lista_pontos = []
    while (aux != 0):
        print("\n======= Menu de Opções =======")
        print("1. Inserir e Verificar a validade dos pontos")
        print("2. Construir polinômio pelo método de Lagrande")
        print("3. Construir polinômio pelo método de Newton")
        print("4. Avaliar a função em um ponto informado")
        print("5. Estimar o erro do método de Lagrange")
        print("6. Estimar o erro do método de Newton")
        print("7. Sair")
    
        opcao = int(input("Escolha: "))
        
        if(opcao == 7):
            print("Encerrando o programa...")
            aux = 0
            continue
        
        funcionamento(lista_pontos, opcao)


if __name__ == "__main__":
    main()
