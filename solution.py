from os import remove
import matplotlib.pyplot as plt
import heapq
from ponto import *

class Solution(object):
    """ Funções básicas da classe """
    def __init__(self, n_pontos, lista_de_pontos, matriz_dist,dimension):
        self.__solucao = []
        self.__dist = 0
        self.__n_pontos = int(n_pontos)
        self.__lista_de_pontos = lista_de_pontos
        self.__matriz_dist = matriz_dist
        self.__solType = ""
        self.__dimension = dimension

    def __str__(self):
        for ponto in self.__pontos:
            print("Ponto de numero:",ponto.getNumero()," com coordenadas: ",ponto.getX()," , ",ponto.getY())
        return "Com uma distancia total de " + str(self.__dist)
    
    def printDist(self):
        print(round(self.__dist,2))
    
    def printSolution(self):
        for i in range(len(self.__solucao) - 1):
            n1 = self.__solucao[i] - 1
            n2 = self.__solucao[i + 1] - 1
            print(self.__matriz_dist[n1][n2],end="->")
    
    def printPath(self):
        for i in self.__solucao:
            print(i,end="->")
        print('\n')

    

    def calculateDist(self,solution):
        dist = 0
        for i in range(len(solution) - 1):
            n1 = solution[i]
            n2 = solution[i + 1]
            dist += self.__matriz_dist[n1 - 1][n2 - 1]
        return round(dist,2)

    """ Funções auxiliares """
    def closerPoint(self,index):  #Dado um ponto(index) retorna o ponto mais próximo deste que não esteja na solução
        saiDe = self.__solucao[index] - 1
        lesserDist = -1
        for i in range(self.__dimension):
            dist = self.__matriz_dist[saiDe][i]
            if((dist <= lesserDist ) or (lesserDist==-1)):
                if (i+1) not in self.__solucao:
                    lesserDist = dist
                    newPoint = i
        return newPoint,lesserDist

    def closeToTheWay(self,n):
        pq = []
        for i in self.__solucao:
            for j in range(self.__dimension):
                if i - 1 != j and j+1 not in self.__solucao:
                    heapq.heappush(pq,(self.__matriz_dist[i - 1][j],(i,j+1)))
        pq = heapq.nsmallest(n,pq)
        return pq


    """ Heuristícas construtivas """
    def findSolutionHVMP(self): #Heuristíca do vizinho mais próximo
        self.__solucao.append(1)
        cont = 1
        while(cont < self.__n_pontos):
            pos,dist = self.closerPoint(-1)
            self.__solucao.append(pos + 1)
            self.__dist += dist
            cont += 1
        self.__solType = "HVMP"

    def findSolutionHIMB(self): #Heurística da inserção mais barata
        lista = []
        if self.__solucao == []:
            for i in range(self.__dimension):
                lista.append(i + 1)
            self.__solucao.append(1)
            lista.pop(0)
            self.__dist = 0
            count = 1
        else:
            for i in range(self.__dimension):
                if i+1 not in self.__solucao:
                    lista.append(i+1)
            count = len(self.__solucao)

        listSize = len(lista)
        while(count < self.__n_pontos):
            lesserDist = 0
            for i in range(count):
                for j in range(listSize):
                    if lista[j] not in self.__solucao:
                        indexJ = lista[j] - 1
                        indexI = self.__solucao[i] - 1
                        if i == count - 1:
                            dist = self.__matriz_dist[indexI][indexJ]
                        else:
                            indexNextI = self.__solucao[i+1] - 1
                            dist = self.__matriz_dist[indexI][indexJ] + self.__matriz_dist[indexJ][indexNextI] - self.__matriz_dist[indexI][indexNextI]
                        if dist < lesserDist or lesserDist == 0:
                            lesserDist = dist
                            after = i+1
                            where = j
            count += 1
            self.__solucao.insert(after,lista[where])
            self.__dist += lesserDist
            lista.pop(where)
            listSize -= 1
        self.__dist = self.calculateDist(self.__solucao)
        self.__solType = "HIMB" 

    def HVMP_HIMB(self): # Heuristíca híbrida
        self.findSolutionHVMP()
        biggerDist = 0
        biggerIndex = 0
        lenght = self.__n_pontos - 1
        for i in range(1,lenght):
            dist = self.__matriz_dist[self.__solucao[i] - 1][self.__solucao[i+1] - 1]
            if dist > biggerDist:
                biggerDist = dist
                biggerIndex = i
        self.__solucao = self.__solucao[:biggerIndex]
        self.calculateDist(self.__solucao)
        self.findSolutionHIMB()
        self.__solType = "Hybrid"

    """ Funções auxiliares das buscas locais """
    # Todas as funções nesta seção tem como objetivo recalcular as distancias para cada uma das buscas locais,
    # para evitar refazer o calculo completo da distancia
    def recalculateDist_troca(self,i,j):
        I = self.__solucao[i] - 1
        nextI = self.__solucao[i + 1] - 1
        prevI = self.__solucao[i - 1] - 1
        J = self.__solucao[j] - 1
        nextJ = self.__solucao[j + 1] - 1
        prevJ = self.__solucao[j - 1] - 1
        dist = self.__dist - self.__matriz_dist[prevI][I] - self.__matriz_dist[I][nextI] - self.__matriz_dist[prevJ][J] - self.__matriz_dist[J][nextJ]
        dist = dist + self.__matriz_dist[prevI][J] + self.__matriz_dist[J][nextI] + self.__matriz_dist[prevJ][I] + self.__matriz_dist[I][nextJ]
        return dist

    def recalculateDist_insercao(self,i,j):
        I = self.__solucao[i] - 1
        prevI = self.__solucao[i] - 1
        nextI = self.__solucao[i] - 1
        prevJ = self.__solucao[j - 1] - 1
        nextJ = self.__solucao[j + 1] - 1
        dist = self.__dist - self.__matriz_dist[prevI][I] - self.__matriz_dist[I][nextI]
        dist = dist + self.__matriz_dist[prevJ][I] + self.__matriz_dist[I][nextJ]
        return dist

    def recalculateDist_2OPT(self,i,j):
        I = self.__solucao[i] - 1
        nextI = self.__solucao[i + 1] - 1
        J = self.__solucao[j] - 1
        prevJ = self.__solucao[j - 1] - 1
        dist = self.__dist - self.__matriz_dist[I][nextI] - self.__matriz_dist[prevJ][J] + self.__matriz_dist[i][prevJ] + self.__matriz_dist[nextI][J] 
        return dist

    def recalculateDist_addDrop(self,i,add):
        posRemove = self.__solucao[i - 1] - 1
        preRemove = self.__solucao[i - 2] - 1
        posInsert = add[1][1] - 1
        I = self.__solucao[i] - 1
        if i == self.__n_pontos - 1:
            dist = self.__dist - self.__matriz_dist[posRemove][I] - self.__matriz_dist[preRemove][posRemove]
            dist = dist + self.__matriz_dist[preRemove][I] + self.__matriz_dist[I][posInsert]
        else:
            nextI = self.__solucao[i + 1] - 1
            dist = self.__dist - self.__matriz_dist[posRemove][I] - self.__matriz_dist[I][nextI] - self.__matriz_dist[preRemove][posRemove]
            dist = dist + self.__matriz_dist[preRemove][I] + self.__matriz_dist[I][posInsert] + self.__matriz_dist[posInsert][nextI]
        return dist

    """ Buscas locais """
    def busca_local_troca(self):
        better = True
        while better:
            better = False
            for i in range(1,self.__n_pontos - 1):
                for j in range(i + 1,self.__n_pontos):
                    if j != i - 1 and j != i:
                        dist = self.recalculateDist_troca(i,j)
                        if dist < self.__dist:
                            self.__solucao[i],self.__solucao[j] = self.__solucao[j],self.__solucao[i] 
                            self.__dist = dist
                            better = True

    def busca_local_insercao(self):
        better = True
        while better:
            better = False
            for i in range(1,self.__n_pontos):
                for j in range(1,self.__n_pontos):
                    if j != i - 1 and j != i:
                        dist = self.recalculateDist_insercao(i,j)
                        if dist < self.__dist:
                            valueToInsert = self.__solucao[i]
                            self.__solucao.pop(i)
                            self.__solucao.insert(j,valueToInsert)
                            self.__dist = dist
                            better = True

    def busca_local_2OPT(self):
        better = True
        while better:
            better = False
            for i in range(1,self.__n_pontos):
                for j in range(self.__n_pontos - 1,-1,-1):
                    if j>i:
                        dist = self.recalculateDist_2OPT(i,j)
                        if dist < self.__dist:
                            self.__solucao[i:j+1] = reversed(self.__solucao[i:j+1])
                            self.__dist = dist
                            better = True

    def busca_local_addDrop(self):
        better = True
        pq = self.closeToTheWay(self.__n_pontos)
        while better:
            better = False
            for add in pq:
                for i in range(1,self.__n_pontos):
                    if self.__solucao[i] == add[1][0] and add[1][1] not in self.__solucao:
                        dist = self.recalculateDist_addDrop(i,add)
                        if dist <= self.__dist:
                            print("----------------------------------------------------------------------------------------------")
                            self.__solucao.pop(i-1)
                            self.__solucao.insert(i+1,add[1][1])
                            dist = self.__dist
                            better = True

    """ Plotagem de solução """
    def plotarSolucao(self,nome_do_arquivo):

        solution = []
        for i in self.__solucao:
            solution.append(self.__lista_de_pontos[i-1])
        # Prepara os pontos pertencentes a solução para inserir no gráfico
        x = []
        y = []
        for ponto in solution:
            x.append(ponto.getX())
            y.append(ponto.getY())

        # Prepara os demais pontos para inserir no gráfico
        x1 = []
        y1 = []
        for ponto in self.__lista_de_pontos:
            x1.append(ponto.getX())
            y1.append(ponto.getY())
        
        # Define o tamanho do gráfico a ser gerado
        fig , ax = plt.subplots(figsize=(10,6))
        #Plota os demais pontos no gráfico
        ax.scatter(x1,y1,marker = 'o')
        # Plota os pontos pertencentes a solução no gráfico
        ax.plot(x,y,marker = 'o',color='red')

        # Configura o titulo do gráfico
        titulo = 'Solução da '+ self.__solType + ' para ' + nome_do_arquivo + '\nDistância Total k = ' + str(self.__dist)
        ax.set(title = titulo,xlabel = "Coordenadas x",ylabel = "Coordenadas y")

        # Enumera todos os pontos do gráfico de acordo com seus respectivos numeros
        for ponto in self.__lista_de_pontos:
            if ponto not in solution:
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'small')
        for ponto in solution:
            if ponto.getNumero() == 1:
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'large')
            else : 
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'medium')

        # Salva o gráfico como pdf no diretório do projeto
        posFormat = nome_do_arquivo.find('.')
        nome  = 'Solução da '+ self.__solType + ' para ' + nome_do_arquivo[:posFormat] + '.pdf'
        plt.savefig(nome,format = 'pdf')
        plt.show()
        return plt