class Projeto:
    def __init__(self, codigo, vagas, nota_min):
        self.codigo = codigo
        self.vagas = vagas
        self.nota_min = nota_min
        self.alunos = []
        self.alunos_assinalados = 0
        self.tem_aluno_assinalado = False 

    def is_full(self):
        return len(self.alunos) == self.vagas

    def add_aluno(self, aluno):
        if not self.is_full() and aluno not in self.alunos:
            self.alunos.append(aluno)
            self.alunos_assinalados += 1
            self.tem_aluno_assinalado = True
            return True
        return False

    def remove_aluno(self, aluno):
        if aluno in self.alunos:
            self.alunos.remove(aluno)
            self.alunos_assinalados -= 1
            if self.alunos_assinalados == 0:
                self.tem_aluno_assinalado = False
    
    def get_numero_alunos(self):
        return len(self.alunos) 

class Aluno:
    def __init__(self, codigo, preferencias, nota):
        self.codigo = codigo
        self.preferencias = preferencias
        self.nota = nota
        self.projeto = None

    
def ler_arquivo(caminho_arquivo):
    projetos = {}
    alunos = {}

    with open(caminho_arquivo, 'r') as file:
        linhas = file.readlines()

    for linha in linhas:
        if linha.startswith("(P"): #maneira encontrada pra corretamente conseguir pegar os dados dos projetos
            parts = linha.strip().split(',')
            codigo = parts[0][1:].strip()
            vagas = int(parts[1].strip())
            nota_min = int(parts[2][:-1].strip())
            projetos[codigo] = Projeto(codigo, int(vagas), int(nota_min))
        elif linha.startswith("(A"): #maneira encontrada pra corretamente conseguir pegar os dados dos alunos
            parts = linha.strip().split(':')
            codigo1 = parts[0][1:].strip()
            codigo = codigo1[:-1]



            
            if len(parts) == 2:
                preferencias = [projeto.strip() for projeto in parts[1][1:-5].split(',')]
                nota1 = (parts[1][-2:])
                nota = int(nota1[:-1])
                alunos[codigo] = Aluno(codigo, preferencias, int(nota))


            else:
                print(f"Pulando linha invalida: {linha}") #checando erros


    return projetos, alunos


def gale_shapley(projetos, alunos):

    alunos_naoconect = list(alunos.values())

    while alunos_naoconect: #enquanto tiverem alunos a ser conectados
        aluno = alunos_naoconect.pop(0) #a partir do primeiro da lista(já o removendo)
        for preferencia in aluno.preferencias: 
            projeto = projetos[preferencia] 
            if not projeto.is_full(): #se o proj nao estiver cheio
                if aluno.nota >= projeto.nota_min and aluno.projeto == None: #se o aluno tiver nota pro proj e quiser o proj
                    projeto.add_aluno(aluno)#designa o aluno ao projeto
                    aluno.projeto = projeto #designa o projeto ao aluno
                    print(f'Aluno {aluno.codigo} adicionado ao projeto {projeto.codigo}.')

                    break

            
            else:
                for alunoassinalado in projeto.alunos:
                    if aluno.nota > alunoassinalado.nota and aluno.projeto == None: #se a nota do aluno que quer o proj for maior que a do aluno que ja esta no proj
                        projeto.remove_aluno(alunoassinalado) #remove o que ja esta
                        projeto.add_aluno(aluno) #coloca o novo
                        print(f'Aluno {alunoassinalado.codigo} removido, aluno {aluno.codigo} adicionado do/ao projeto {projeto.codigo}')
                        aluno.projeto = projeto
                        alunoassinalado.projeto = None
                        alunos_naoconect.append(alunoassinalado) #volta o aluno que foi removido para a lista de alunos nao conectados
                        break
                    else:
                        print(f'O projeto {projeto.codigo} prefere o aluno {alunoassinalado.codigo} ao aluno {aluno.codigo} pela nota maior ou igual.') #do contrario o projeto prefere o aluno que ja esta no proj
                        
  


            




    resultado = {}
    for projeto in projetos.values():
        for aluno in projeto.alunos:
            resultado[aluno] = projeto.codigo

    return resultado

def print_alocacao(alocacao):
    for aluno, projeto_codigo in alocacao.items():
        print(f"Aluno {aluno.codigo} assinalado ao Projeto {projeto_codigo}.") #printa a alocação no formato desejado

iteracoes = 0 #inicializa as iterações
if __name__ == "__main__":
    while iteracoes < 10: #repetir 10 vezes
        arquivo_entrada = "entradaProj2TAG.txt"
        projetos, alunos = ler_arquivo(arquivo_entrada)


        alocacao = gale_shapley(projetos, alunos)


        print("Pares finais Aluno x Projeto:")
        print_alocacao(alocacao)
        total_alunos = sum(projeto.get_numero_alunos() for projeto in projetos.values())
        print(f"Número de alunos com projetos: {total_alunos}.")
        projetos_com_alunos = sum(projeto.tem_aluno_assinalado for projeto in projetos.values())
        print(f"Número de projetos com no mínimo um aluno assinalado: {projetos_com_alunos}.")
        iteracoes += 1
