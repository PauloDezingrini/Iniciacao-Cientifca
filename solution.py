from math import ceil, floor
from random import randint

import matplotlib.pyplot as plt
import heapq

from ponto import *


class Solution(object):
    """ Funções básicas da classe """

    def __init__(self, n_pontos, lista_de_pontos, matriz_dist, dimension):
        self.__solucao = []
        self.__dist = 0
        self.__n_pontos = int(n_pontos)
        self.__lista_de_pontos = lista_de_pontos
        self.__matriz_dist = matriz_dist
        self.__solType = ""
        self.__dimension = dimension

    def __str__(self):
        for ponto in self.__pontos:
            print("Ponto de numero:", ponto.getNumero(),
                  " com coordenadas: ", ponto.getX(), " , ", ponto.getY())
        return "Com uma distancia total de " + str(self.__dist)

    def getDist(self):
        return round(self.__dist, 2)

    def printDist(self):
        print(round(self.__dist, 2))

    def printSolution(self):
        for i in range(len(self.__solucao) - 1):
            n1 = self.__solucao[i] - 1
            n2 = self.__solucao[i + 1] - 1
            print(self.__matriz_dist[n1][n2], end="->")

    def printPath(self):
        for i in self.__solucao:
            print(i, end="->")
        print('\n')

    def calculateDist(self, solution):
        dist = 0
        for i in range(len(solution) - 1):
            n1 = solution[i]
            n2 = solution[i + 1]
            dist += self.__matriz_dist[n1 - 1][n2 - 1]
        return round(dist, 2)

    """ Funções auxiliares """

    # Dado um ponto(index) retorna o ponto mais próximo deste que não esteja na solução
    def closerPoint(self, index):
        saiDe = self.__solucao[index] - 1
        lesserDist = -1
        for i in range(self.__dimension):
            dist = self.__matriz_dist[saiDe][i]
            if((dist <= lesserDist) or (lesserDist == -1)):
                if (i+1) not in self.__solucao:
                    lesserDist = dist
                    newPoint = i
        return newPoint, lesserDist

    def closeToTheWay(self, n):
        pq = []
        for i in self.__solucao:
            for j in range(self.__dimension):
                if i - 1 != j and j+1 not in self.__solucao:
                    heapq.heappush(
                        pq, (self.__matriz_dist[i - 1][j], (i, j+1)))
        pq = heapq.nsmallest(n, pq)
        return pq

    def closeToThePoint(self, i):
        lesserDist = -1
        for j in range(len(self.__dimension)):
            dist = self.__matriz_dist[i][j]
            if (dist < lesserDist) and (j + 1 not in self.__solucao):
                lesserDist = dist
                point = j + 1
        return point

    def longerDist(self, n):
        pq = []
        for i in range(1, self.__n_pontos - 1):
            I = self.__solucao[i] - 1
            nextI = self.__solucao[i + 1] - 1
            heapq.heappush(pq, (self.__matriz_dist[I][nextI], nextI + 1))
        pq = heapq.nlargest(n, pq)
        return pq

    def auxHIMB(self):
        pointList = self.__solucao[1:]
        self.__solucao = []
        self.__solucao.append(1)
        count = 1
        listSize = len(pointList)
        self.__dist = 0
        while(count < self.__n_pontos):
            lesserDist = -1
            for i in range(count):
                for j in range(listSize):
                    J = pointList[j] - 1
                    I = self.__solucao[i] - 1
                    dist = self.__matriz_dist[I][J]
                    if i != count - 1:
                        nextI = self.__solucao[i + 1] - 1
                        dist = dist + \
                            self.__matriz_dist[J][nextI] - \
                            self.__matriz_dist[I][nextI]
                    if dist < lesserDist or lesserDist == -1:
                        lesserDist = dist
                        after = i + 1
                        where = j
            count += 1
            self.__solucao.insert(after, pointList[where])
            self.__dist += lesserDist
            pointList.pop(where)
            listSize -= 1
        self.__solType = "Hybrid"

    """ Heuristícas construtivas """

    def findSolutionHVMP(self):  # Heuristíca do vizinho mais próximo
        self.__solucao.append(1)
        cont = 1
        while(cont < self.__n_pontos):
            pos, dist = self.closerPoint(-1)
            self.__solucao.append(pos + 1)
            self.__dist += dist
            cont += 1
        self.__solType = "HVMP"

    def findSolutionHIMB(self):  # Heurística da inserção mais barata
        lista = []
        if self.__solucao == []:
            for i in range(1, self.__dimension):
                lista.append(i + 1)
            self.__solucao.append(1)
            self.__dist = 0
            count = 1
        else:
            for i in range(self.__dimension):
                if i+1 not in self.__solucao:
                    lista.append(i+1)
            count = len(self.__solucao)

        listSize = len(lista)
        while(count < self.__n_pontos):
            lesserDist = -1
            for i in range(count):
                for j in range(listSize):
                    if lista[j] not in self.__solucao:
                        indexJ = lista[j] - 1
                        indexI = self.__solucao[i] - 1
                        if i == count - 1:
                            dist = self.__matriz_dist[indexI][indexJ]
                        else:
                            indexNextI = self.__solucao[i+1] - 1
                            dist = self.__matriz_dist[indexI][indexJ] + \
                                self.__matriz_dist[indexJ][indexNextI] - \
                                self.__matriz_dist[indexI][indexNextI]
                        if dist < lesserDist or lesserDist == -1:
                            lesserDist = dist
                            after = i+1
                            where = j
            count += 1
            self.__solucao.insert(after, lista[where])
            self.__dist += lesserDist
            lista.pop(where)
            listSize -= 1
        self.__solType = "HIMB"

    def HVMP_HIMB(self):  # Heuristíca híbrida
        self.findSolutionHVMP()
        biggerDist = 0
        biggerIndex = 0
        lenght = self.__n_pontos - 1
        for i in range(1, lenght):
            dist = self.__matriz_dist[self.__solucao[i] -
                                      1][self.__solucao[i+1] - 1]
            if dist > biggerDist:
                biggerDist = dist
                biggerIndex = i
        self.__solucao = self.__solucao[:biggerIndex]
        self.calculateDist(self.__solucao)
        self.findSolutionHIMB()
        self.__solType = "Hybrid"

    def HVMP_HIMB2(self, np):
        while np >= self.__n_pontos:
            np = floor(np/2)
        self.findSolutionHVMP()
        closer = self.closeToTheWay(np)
        longer = self.longerDist(np)
        for point in longer:
            self.__solucao.remove(point[1])
        for point in closer:
            if len(self.__solucao) == self.__n_pontos:
                break
            if point[1][0] in self.__solucao:
                index = self.__solucao.index(point[1][0])
                self.__solucao.insert(index+1, point[1][1])
        if len(self.__solucao) < self.__n_pontos:
            self.findSolutionHIMB()
        self.auxHIMB()
        print(len(self.__solucao))

    """ Funções auxiliares das buscas locais """
    # Todas as funções nesta seção tem como objetivo recalcular as distancias para cada uma das buscas locais,
    # para evitar refazer o calculo completo da distancia

    def recalculateDist_brute(self, i, j):
        I = self.__solucao[i] - 1
        prevI = self.__solucao[i - 1] - 1
        dist = self.__dist - self.__matriz_dist[prevI][I]
        dist += self.__matriz_dist[prevI][j]
        if i != self.__n_pontos - 1:  # Caso o ponto que está sendo testada a remoção não seja o último ponto temos que considerar as distância até o próximo após ele
            nextI = self.__solucao[i + 1] - 1
            dist = dist - \
                self.__matriz_dist[I][nextI] + self.__matriz_dist[j][nextI]
        return dist

    """ Buscas locais """

    def busca_local_troca(self):
        better = True
        while better:
            better = False
            s = self.__solucao[:]
            for i in range(1, self.__n_pontos - 1):
                for j in range(i + 1, self.__n_pontos):
                    s[i], s[j] = s[j], s[i]
                    dist = self.calculateDist(s)
                    if dist < self.__dist:
                        self.__dist = dist
                        self.__solucao = s
                        better = True
                    else:
                        s[i], s[j] = s[j], s[i]

    def busca_local_insercao(self):
        better = True
        while better:
            better = False
            for i in range(1, self.__n_pontos):
                for j in range(1, self.__n_pontos):
                    if j != i - 1 and j != i:
                        s = self.__solucao[:]
                        valueToInsert = s[i]
                        s.pop(i)
                        s.insert(j, valueToInsert)
                        dist = self.calculateDist(s)
                        if dist < self.__dist:
                            self.__solucao = s
                            self.__dist = dist
                            better = True

    def busca_local_2OPT(self):
        better = True
        while better:
            better = False
            for i in range(1, self.__n_pontos - 1):
                for j in range(self.__n_pontos - 1, -1, -1):
                    if j > i:
                        s = self.__solucao[:]
                        s[i:j+1] = reversed(s[i:j+1])
                        dist = self.calculateDist(s)
                        if dist < self.__dist:
                            self.__solucao[i:j +
                                           1] = reversed(self.__solucao[i:j+1])
                            self.__dist = dist
                            better = True
                    else:
                        break

    def busca_local_addDrop(self):
        _out = []
        _in = []
        better = True
        pq = self.closeToTheWay(self.__n_pontos)
        while better:
            better = False
            for add in pq:
                if add[1][0] in self.__solucao:
                    index = self.__solucao.index(add[1][0])
                    for i in range(1, self.__n_pontos):
                        if add[1][1] not in self.__solucao and add[1][0] != self.__solucao[i]:
                            s = self.__solucao[:]
                            s.pop(i)
                            s.insert(index+1, add[1][1])
                            dist = self.calculateDist(s)
                            if dist < self.__dist:
                                self.__solucao = s
                                _out.append(self.__solucao[i])
                                _in.append(add[1][1])
                                self.__dist = dist
                                break
        # print("Saiu : ", _out)
        # print("Entrou : ", _in)
        # print("Distancia esperada: ",self.calculateDist(self.__solucao))

    def busca_local_bruta(self):
        _out = []
        _in = []
        better = True
        while better:
            better = False
            for i in range(1, self.__n_pontos):  # Para cada ponto na solução
                in_ = -1
                newDist = 0
                # Olhar cada ponto que não está na solução
                for j in range(1, self.__dimension):
                    if j + 1 not in self.__solucao:
                        dist = self.recalculateDist_brute(i, j)
                        if dist < self.__dist:
                            in_ = j
                            newDist = dist
                if in_ != -1:
                    _out.append(self.__solucao[i])
                    self.__solucao.pop(i)
                    self.__solucao.insert(i, in_ + 1)
                    _in.append(self.__solucao[i])
                    self.__dist = newDist
                    better = True
        print("Saiu : ", _out)
        print("Entrou : ", _in)
        print(len(self.__solucao))
        print("Distancia esperada: ", self.calculateDist(self.__solucao))
        print("Distancia Obtida: ", self.__dist)

    """ Metaheurísticas """

    def buscaLocalRVND(self):
        """
            Ao invés de utilizar um vetor com as buscas locais, optei por utilizar simplesmente
            um randint(1,3) que retorna um número aleatório x tal que 1 <= x <= 3
            onde cada número será uma busca local diferente. A relação de buscas locais será:
            1 = Add-Drop
            2 = 2-OPT
            3 = Inserção
        """
        localSearchs = randomizeLocalSearchs()
        k = 1
        while k <= 3:
            oldDist = self.getDist()
            chosenLS = localSearchs.pop()
            if chosenLS == 1:
                self.busca_local_addDrop()
            elif chosenLS == 2:
                self.busca_local_2OPT()
            else:
                self.busca_local_insercao()

            if self.__dist < oldDist:
                k = 1
                localSearchs = randomizeLocalSearchs()
            else:
                k += 1

    def ILS(self):
        self.buscaLocalRVND()

        k = 0
        while k < 100:

            # Perturb
            j = 0
            while j < 4:
                index = randint(0, len(self.__solucao))
                point_to_drop = self.__solucao[index]
                new_point = self.closeToThePoint(point_to_drop - 1)
                self.__solucao[index] = new_point

            # Local Search
            self.buscaLocalRVND()

            pass

    """ Plotagem de solução """

    def plotarSolucao(self, nome_do_arquivo):

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
        fig, ax = plt.subplots(figsize=(10, 6))
        # Plota os demais pontos no gráfico
        ax.scatter(x1, y1, marker='o')
        # Plota os pontos pertencentes a solução no gráfico
        ax.plot(x, y, marker='o', color='red')

        # Configura o titulo do gráfico
        titulo = 'Solução da ' + self.__solType + ' para ' + \
            nome_do_arquivo + '\nDistância Total k = ' + str(self.__dist)
        ax.set(title=titulo, xlabel="Coordenadas x", ylabel="Coordenadas y")

        # Enumera todos os pontos do gráfico de acordo com seus respectivos numeros
        for ponto in self.__lista_de_pontos:
            if ponto not in solution:
                plt.text(ponto.getX(), ponto.getY(), str(
                    ponto.getNumero()), fontsize='small')
        for ponto in solution:
            if ponto.getNumero() == 1:
                plt.text(ponto.getX(), ponto.getY(), str(
                    ponto.getNumero()), fontsize='large')
            else:
                plt.text(ponto.getX(), ponto.getY(), str(
                    ponto.getNumero()), fontsize='medium')

        # Salva o gráfico como pdf no diretório do projeto
        posFormat = nome_do_arquivo.find('.')
        nome = 'Solução da ' + self.__solType + \
            ' para ' + nome_do_arquivo[:posFormat] + '.pdf'
        plt.savefig(nome, format='pdf')
        plt.show()
        return plt

    """ Não funcionando corretamente """

    def recalculateDist_troca(self, i, j):
        print(self.__dist)
        dist = 0.0
        I = self.__solucao[i] - 1
        prevI = self.__solucao[i - 1] - 1
        J = self.__solucao[j] - 1
        prevJ = self.__solucao[j - 1] - 1
        dist = self.__dist - self.__matriz_dist[prevI][I] - self.__matriz_dist[prevJ][J] + \
            self.__matriz_dist[prevI][J] + self.__matriz_dist[prevJ][I]
        if i != self.__n_pontos - 1:
            nextI = self.__solucao[i + 1] - 1
            dist = dist - \
                self.__matriz_dist[I][nextI] + self.__matriz_dist[J][nextI]
        if j != self.__n_pontos - 1:
            nextJ = self.__solucao[j + 1] - 1
            dist = dist - \
                self.__matriz_dist[J][nextJ] + self.__matriz_dist[I][nextJ]
        return dist

    def recalculateDist_insercao(self, i, j):
        I = self.__solucao[i] - 1
        prevI = self.__solucao[i - 1] - 1
        J = self.__solucao[j] - 1
        dist = self.__dist - \
            self.__matriz_dist[prevI][I] + self.__matriz_dist[J][I]
        dist += self.__matriz_dist[J][I]
        if i != self.__n_pontos - 1:
            nextI = self.__solucao[i + 1] - 1
            dist = dist - \
                self.__matriz_dist[I][nextI] + self.__matriz_dist[prevI][nextI]
        if j != self.__n_pontos - 1:
            nextJ = self.__solucao[j + 1] - 1
            dist = dist - \
                self.__matriz_dist[J][nextJ] + self.__matriz_dist[I][nextJ]
        return dist

    def recalculateDist_addDrop(self, i, add, index):

        dist = 0.0
        I = self.__solucao[i] - 1
        prevI = self.__solucao[i - 1] - 1
        insertAfter = add[1][0] - 1
        insert = add[1][1] - 1
        if i == self.__n_pontos - 1:
            nextInsertAfter = self.__solucao[index + 1] - 1
            dist = self.__dist - self.__matriz_dist[prevI][I]
            dist = dist - self.__matriz_dist[insertAfter][nextInsertAfter] + \
                add[0] + self.__matriz_dist[insert][nextInsertAfter]
        else:
            nextI = self.__solucao[i + 1] - 1
            dist = self.__dist - \
                self.__matriz_dist[prevI][I] - self.__matriz_dist[I][nextI] + \
                self.__matriz_dist[prevI][nextI]
            if index == self.__n_pontos - 1:
                dist += add[0]
            else:
                nextInsertAfter = self.__solucao[index + 1] - 1
                dist = dist - self.__matriz_dist[insertAfter][nextInsertAfter] + \
                    add[0] + self.__matriz_dist[insert][nextInsertAfter]
        return dist
    """
    def busca_local_addDrop(self):
        _out = []
        _in = []
        better = True
        pq = self.closeToTheWay(self.__n_pontos)
        while better:
            better = False
            for add in pq:
                for i in range(1,self.__n_pontos):
                    if add[1][1] not in self.__solucao and add[1][0] != self.__solucao[i] and add[1][0] in self.__solucao:
                        index = self.__solucao.index(add[1][0])
                        dist = self.recalculateDist_addDrop(i,add,index)
                        if dist < self.__dist:
                            self.__solucao.pop(i)
                            self.__solucao.insert(index+1,add[1][1])
                            _out.append(self.__solucao[i])
                            _in.append(add[1][1])
                            self.__dist = dist
                            break
        print("Saiu : ", _out)
        print("Entrou : ", _in)
        print(len(self.__solucao))
        print("Distancia esperada: ",self.calculateDist(self.__solucao))
    """


""" Funções auxiliares das metaheurísticas """


def randomizeLocalSearchs():
    localSearchs = []
    availableValues = [1, 2, 3]
    while len(availableValues) != 0:
        newInsert = randint(0, len(availableValues) - 1)
        localSearchs.append(availableValues.pop(newInsert))

    return localSearchs
