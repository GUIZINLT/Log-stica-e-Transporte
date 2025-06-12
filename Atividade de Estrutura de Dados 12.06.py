# Atividade de Estrutura de Dados ( Logística e Transporte)

import heapq

class Cidade:
    
    def __init__(self, nome):
        
        self.nome = nome
        self.vizinhos = {}

    def __lt__(self, other):
        return self.nome < other.nome

class GrafoLogistica:
    
    def __init__(self):
        self.cidades = {}

    def adicionar_cidade(self, nome_cidade):
        if nome_cidade not in self.cidades:
            self.cidades[nome_cidade] = Cidade(nome_cidade)
            print(f"Cidade '{nome_cidade}' foi adicionada.")
        else:
            print(f"Aviso: A cidade '{nome_cidade}' já existe no mapa.")

    def adicionar_rota(self, nome_origem, nome_destino, distancia):
        if nome_origem in self.cidades and nome_destino in self.cidades:
            if not isinstance(distancia, (int, float)) or distancia <= 0:
                print("Erro: A distância deve ser um número positivo.")
                return

            cidade_origem = self.cidades[nome_origem]
            cidade_destino = self.cidades[nome_destino]
            
            cidade_origem.vizinhos[cidade_destino] = distancia
            cidade_destino.vizinhos[cidade_origem] = distancia
            print(f"Rota de {distancia}km entre '{nome_origem}' e '{nome_destino}' foi adicionada.")
        else:
            print("Erro: Uma ou ambas as cidades especificadas não foram encontradas.")

    def exibir_malha(self):
        if not self.cidades:
            print("A malha logística está vazia.")
            return
            
        print("\n--- Malha Logística Atual ---")
        for nome, cidade in self.cidades.items():
            rotas_str = ', '.join(f"{v.nome} ({d}km)" for v, d in cidade.vizinhos.items()) or "Nenhuma rota cadastrada"
            print(f"{nome} -> [ {rotas_str} ]")
        print("-----------------------------")

    def calcular_menor_rota(self, nome_origem, nome_destino):
        if nome_origem not in self.cidades or nome_destino not in self.cidades:
            print("Erro: A cidade de origem ou de destino não foi encontrada.")
            return

        distancias = {nome: float('inf') for nome in self.cidades}
        predecessores = {nome: None for nome in self.cidades}
        distancias[nome_origem] = 0
        
        fila_prioridade = [(0, self.cidades[nome_origem])]

        while fila_prioridade:
            distancia_atual, cidade_atual = heapq.heappop(fila_prioridade)

            if distancia_atual > distancias[cidade_atual.nome]:
                continue

            if cidade_atual.nome == nome_destino:
                break

            for vizinho, distancia_rota in cidade_atual.vizinhos.items():
                nova_distancia = distancia_atual + distancia_rota
                
                if nova_distancia < distancias[vizinho.nome]:
                    distancias[vizinho.nome] = nova_distancia
                    predecessores[vizinho.nome] = cidade_atual.nome
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

        if distancias[nome_destino] == float('inf'):
            print(f"\nNão foi encontrada uma rota entre '{nome_origem}' e '{nome_destino}'.")
            return
    
        caminho = []
        passo_atual = nome_destino
        while passo_atual is not None:
            caminho.append(passo_atual)
            passo_atual = predecessores[passo_atual]
        caminho.reverse()

        print("\n--- Resultado do Cálculo de Rota ---")
        print(f"Melhor Rota: {' -> '.join(caminho)}")
        print(f"Distância Total: {distancias[nome_destino]} km")
        print("------------------------------------")


def menu_logistica():
    malha = GrafoLogistica()
    malha.adicionar_cidade("Palmas")
    malha.adicionar_cidade("Araguaína")
    malha.adicionar_cidade("Gurupi")
    malha.adicionar_cidade("Porto Nacional")
    malha.adicionar_cidade("Paraíso do Tocantins")
    malha.adicionar_rota("Palmas", "Porto Nacional", 60)
    malha.adicionar_rota("Palmas", "Paraíso do Tocantins", 70)
    malha.adicionar_rota("Paraíso do Tocantins", "Gurupi", 170)
    malha.adicionar_rota("Palmas", "Araguaína", 380)
    malha.adicionar_rota("Gurupi", "Araguaína", 550)

    while True:
        print("\n--- Menu Principal do Sistema de Logística ---")
        print("1. Adicionar Cidade/Centro de Distribuição")
        print("2. Adicionar Rota")
        print("3. Exibir Malha Logística Completa")
        print("4. Calcular Menor Rota entre duas Cidades")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Digite o nome da cidade a ser inserida: ").strip()
            if nome:
                malha.adicionar_cidade(nome)
            else:
                print("Nome da cidade não pode ser vazio.")
        
        elif opcao == '2':
            try:
                origem = input("Digite a cidade de origem: ").strip()
                destino = input("Digite a cidade de destino: ").strip()
                distancia_str = input("Digite a distância da rota (em km): ")
                distancia = int(distancia_str)
                malha.adicionar_rota(origem, destino, distancia)
            except ValueError:
                print("Erro: Distância inválida. Por favor, insira um número inteiro.")

        elif opcao == '3':
            malha.exibir_malha()

        elif opcao == '4':
            origem = input("Digite a cidade de origem da rota: ").strip()
            destino = input("Digite a cidade de destino da rota: ").strip()
            malha.calcular_menor_rota(origem, destino)
        
        elif opcao == '5':
            print("Encerrando o sistema...")
            break
            
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    menu_logistica()
