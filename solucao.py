from typing import Sized
from ponto import *
import random

import matplotlib.pyplot as plt

from mip import Model, xsum, minimize, BINARY

class Solucao(object):
    def __init__(self,numero_de_pontos):
        self.__pontos = []
        self.__distTotal = 0
        self.__numero_de_pontos = int(numero_de_pontos)

    def __str__(self):
        for ponto in self.__pontos:
            print("Ponto de numero:",ponto.getNumero()," com coordenadas: ",ponto.getX()," , ",ponto.getY())
        return "Com uma distancia total de " + str(self.__distTotal)

    def calcularDistTotal(self,matriz_de_distancia):
        distTotal = 0
        for i in range(self.__numero_de_pontos - 1):
            n1 = self.__pontos[i].getNumero()
            n2 = self.__pontos[i + 1].getNumero()
            # O - 1 é devido ao fato da lista começar em 0 , não em 1 , portanto o ponto 1 está na posição 0 , o ponto 2 na posição e por ai vai 
            distTotal += matriz_de_distancia[n1 - 1][n2 - 1]
        self.__distTotal = distTotal


    def encontrarSolucaoRandomica(self,lista_de_pontos,matriz_de_distancias):
        # A lista aux é necessária para poder remover os pontos já utilizados na solução da lista sem alterar a lista de pontos.
        # Já que o processo para encontrar uma solução poderá ocorrer mais de 1 vez
        aux = lista_de_pontos
        # Como a leitura é feita de forma a seguir o numero dos pontos e o primeiro ponto de toda solução tem que ser o ponto 1
        # Podemos fazer essa atribuição diretamente com a posicao 0 da lista de pontos
        self.__pontos.append(aux[0])
        aux.pop(0)
        # Enquanto o tamanho da solução(__pontos) for menor que o numero de pontos pedidos ele escolhe uma posicao aleatoaria do array
        # Entao adiciona essa solucao ao vetor __pontos e deleta do vetor auxiliar para evitar repeticoes
        while(len(self.__pontos)<self.__numero_de_pontos):
            index = random.randint(0,len(aux)-1)
            self.__pontos.append(aux[index])
            aux.pop(index)
        self.calcularDistTotal(matriz_de_distancias)


    def encontrarPontoMaisProximo(self,lista_de_pontos,matriz_de_distancias,size,ponto):
    # Size é passado como paramentro simplesmente para evitar fazer a operaçao len(lista_de_pontos) repetidas vezes 
        posNovoPonto = 0
        # Representa o ponto de saída de determinado trecho da rota
        saiDe = lista_de_pontos[ponto]
        menorDist = 0
        for i in range(size):
            if((matriz_de_distancias[saiDe][i]<=menorDist) or (menorDist==0)):
                # Somente escolhe como ponto mais proximo , pontos que não estejam na solução
                if i not in lista_de_pontos:
                    menorDist = matriz_de_distancias[saiDe][i]
                    posNovoPonto = i
        return posNovoPonto

    def encontrarSolucaoVizinhoProximo(self,lista_de_pontos,matriz_de_distancias): 
        pontos_utilizados = []
        pontos_utilizados.append(0)

        # A matriz_de_distancias possui dimensão size X size , como precisamos percorrer linhas/colunas da matriz o valor size já
        # foi definido previamente
        size = len(lista_de_pontos)
        while(len(pontos_utilizados) < self.__numero_de_pontos):
            # Como queremos encontrar o ponto mais proximo do ultimo inserido no array , basta passar -1 como ultimo paramentro
            pontos_utilizados.append(self.encontrarPontoMaisProximo(pontos_utilizados,matriz_de_distancias,size,-1))

        for i in range(self.__numero_de_pontos):
            self.__pontos.append(lista_de_pontos[pontos_utilizados[i]])
        self.calcularDistTotal(matriz_de_distancias)

    def encontrarSolucaoInsercaoMaisBarata(self,lista_de_pontos,matriz_de_distancias):
        # Tamanho da lista de pontos , utilizada para achar os pontos mais próximos de um determinado ponto
        size = len(lista_de_pontos)
        # Array auxiliar que representa os pontos que viram a ser utilizado na solução e a inserção do ponto inicial , que neste caso é o ponto 1 
        pontos_utilizados = []
        pontos_utilizados.append(0)
        # Variáveis auxiliares
        posBestInsertion = 0
        index = 0
        while(len(pontos_utilizados) < self.__numero_de_pontos):
            bestInsertion = -1
            for i in range(len(pontos_utilizados)):
                # Para cada ponto já presente na solução , ele encontra seu respectivo ponto mais proximo
                ponto = self.encontrarPontoMaisProximo(pontos_utilizados,matriz_de_distancias,size,i)
                # Caso em que o ponto que está sendo analisado , possivelmente, será inserido após o ultimo ponto que já está na solução
                if(i+1 >= len(pontos_utilizados)):
                    dist = matriz_de_distancias[pontos_utilizados[i]][ponto]
                else:
                    # Caso geral
                    dist = matriz_de_distancias[pontos_utilizados[i]][ponto] + matriz_de_distancias[ponto][pontos_utilizados[i+1]] - matriz_de_distancias[pontos_utilizados[i]][pontos_utilizados[i+1]]
                # caso a distancia calculcada seja menor que a atual inserção mais barata ela o substitui
                if (dist <= bestInsertion or bestInsertion == -1):
                    bestInsertion = dist
                    posBestInsertion = ponto
                    index = i
            # Apos a execucação de todo o loop , insere no array de pontos utilizados a posição do ponto , dentro do array lista de pontos que resulta na inserção mais barata
            pontos_utilizados.insert(index+1,posBestInsertion)

        # Por fim, passa os pontos encontrados para a lista de pontos que a classe possui como atributo. 
        for i in range(self.__numero_de_pontos):
            self.__pontos.append(lista_de_pontos[pontos_utilizados[i]])
        self.calcularDistTotal(matriz_de_distancias)

    def encontrarSolucaoModelo(self,lista_de_pontos,matriz_de_distancias):
        # size1 é utilizado em restrições que iniciam desde o primeiro ponto , enquanto o size2 exclui esse ponto
        size1 = set(range(len(lista_de_pontos)))
        size2 = set(range(1,len(lista_de_pontos)))

        model = Model()
        x = [[model.add_var(var_type=BINARY) for j in size1] for i in size1]
        y = [model.add_var(var_type=BINARY) for i in size1]
        F = [[model.add_var() for i in size1] for j in size1]

        model.objective = minimize(xsum(matriz_de_distancias[i][j]*x[i][j] for i in size1 for j in size1))

        # Restricao 2 : Garante que só haverá uma rota saindo do ponto inicial
        model += xsum(x[0][j] for j in size2) == 1
        # Restricao 3 : Garante que não terá nenhuma rota chegando no ponto inicial
        model += xsum(x[i][0] for i in size2) == 0

        # Restricoes 4 e 5 : Garantem que só haverá uma rota saindo e uma chegando em cada ponto
        for j in size1:
            model += xsum(x[i][j] for i in size1 if i!=j) <= 1

        for i in size1:
            model += xsum(x[i][j] for j in size1 if i!=j) <= 1
        
        # Restriçao 6 : Garante que o número de pontos do modelo será igual ao número de pontos requisitado.
        model += xsum(y[i] for i in size1) == self.__numero_de_pontos

        # Restriçao 7
        for i in size2:
            model += (xsum(F[h][i]for h in size1) - xsum(F[i][j] for j in size1)) == y[i]
        # Restriçao 8
        for i in size1:
            for j in size1:
                model+= F[i][j] <= (self.__numero_de_pontos - 1)*x[i][j]
        # Restriçao 9 : 
        for j in size1:
            model += (xsum(x[i][j] for i in size1) - xsum(x[j][h] for h in size2)) <=1

        model.optimize(max_seconds=3600)
        pontos_utilizados = []
        if model.num_solutions:
            self.__distTotal = model.objective_value
            posSaida = 0
            pontos_utilizados.append(0)
            while True:
                for i in size2:
                    if(x[posSaida][i].x >= 0.90 and i not in pontos_utilizados):
                        pontos_utilizados.append(i)
                        posSaida = i
                        print(posSaida)
                        break
                if(len(pontos_utilizados) == self.__numero_de_pontos):
                    break
            for i in range(self.__numero_de_pontos):
                self.__pontos.append(lista_de_pontos[pontos_utilizados[i]])

    def plotarSolucao(self,nome_do_arquivo,lista_de_pontos):
        # Prepara os pontos pertencentes a solução para inserir no gráfico
        x = []
        y = []
        for ponto in self.__pontos:
            x.append(ponto.getX())
            y.append(ponto.getY())
        # Prepara os demais pontos para inserir no gráfico

        x1 = []
        y1 = []
        for ponto in lista_de_pontos:
            x1.append(ponto.getX())
            y1.append(ponto.getY())
        
        # Define o tamanho do gráfico a ser gerado
        fig , ax = plt.subplots(figsize=(10,6))
        #Plota os demais pontos no gráfico
        ax.scatter(x1,y1,marker = 'o')
        # Plota os pontos pertencentes a solução no gráfico
        ax.plot(x,y,marker = 'o',color='red')

        # Configura o titulo do gráfico
        titulo = 'Solução para ' + nome_do_arquivo + '\nDistância Total k = ' + str(self.__distTotal)
        ax.set(title = titulo,xlabel = "Coordenadas x",ylabel = "Coordenadas y")

        # Enumera todos os pontos do gráfico de acordo com seus respectivos numeros
        for ponto in self.__pontos:
            if ponto.getNumero() == 1:
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'large')
            else : 
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'medium')

        # Salva o gráfico como pdf no diretório do projeto
        posFormat = nome_do_arquivo.find('.')
        nome  = 'Solução para ' + nome_do_arquivo[:posFormat] + '.pdf'
        plt.savefig(nome,format = 'pdf')
        plt.show()
        return plt
        