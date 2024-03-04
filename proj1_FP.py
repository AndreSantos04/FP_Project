
#1 -Justificar Textos

def limpa_texto(texto):
    ''' 
    texto --> cadeia de caracteres que pode conter caracteres brancos
    Devolve uma string igual à original mas sem os caracteres brancos 

    limpa_texto: str --> str
    '''
    #Transforma a string num tuplo, em que cada palavra é um elemento
    texto= texto.split()      
    #Transforma em string unindo as palavras através de espaços
    texto= ' '.join(texto)

    return texto

def corta_texto(texto, larg):
    ''' 
    texto --> cadeia de caracteres previamente limpa
    larg --> numero inteiro positivo correspondente a uma largura de coluna
    
    Divide a string em duas de acordo com a largura da coluna desejada sendo que:
            uma palavra não pode ficar separada
            a primeira string deve ter uma largura igual ou inferior à largura desejada 
            ficando a segunda string com o resto da cadeia
    
    corta_texto: str x int --> str x str
    '''

    stringi=''
    stringf=''
    #Tamanho do texto menor que a largura ou não separa nenhuma palavra quando atinge a largura:
    if len(texto)<=larg or texto[larg]==' ':       
        stringi = texto[0:larg]      

    #Se separa uma palavra: descobre o início da palavra e divide a string antes do início da palavra    
    else:      
        while larg>0:
            larg-=1
            if texto[larg]== ' ':
               stringi = texto[:larg]
               break
    
                                    #A segunda string é o que sobra da string original
    stringf = texto[larg:].strip()  #Retirar espaços no inicio e no fim da string
    stringi = stringi.strip()

    return stringi, stringf

def insere_espacos (texto, larg):
    ''' 
    texto --> cadeia de caracteres previamente limpa
    larg --> numero inteiro positivo correspondente a uma largura de coluna

    Devolve o mesmo texto com a largura da coluna desejada: 
                se apenas tiver uma palavra adiciona espaços após a mesma
                caso contrário adiciona espaços entre as palavras 
    
    insere_espacos: str x int --> str
    '''

    npalavras=len(texto.split())
    i = 0

    #Se o texto tiver 2 ou mais palavras adiciona um espaçamento antes de outro já existente
    if npalavras>= 2:           
        while len(texto)< larg:
            while i<len(texto):
                if texto[i]== ' ':                        
                    texto = texto[:i] + ' ' + texto[i:]

                    #Parar se já tiver o numero de caracteres pretendido
                    if len(texto) == larg: 
                        break                    
                    while texto[i]==' ': #Seguir até à próxima palavra
                        i+=1                       
                i+=1

                #Se chegou ao fim do texto e ainda não tem o número de caracteres necessário
                if len(texto)!=larg and i>=len(texto): #Voltar ao início
                    i=0       
    #Caso só tenha uma palavra
    else:  
        texto = espaco_uma_palavra(texto, larg) 
    return texto

def espaco_uma_palavra(texto, larg):
    #Adicionar espaçamentos até atinigir a largura necessária
    while len(texto)<larg:          
        texto = texto + ' '
    return texto

def justifica_texto(texto, larg):
    ''' 
    string --> cadeia de caracteres que pode conter caracteres vazios
    larg --> numero inteiro positivo correspondente a uma largura de coluna

    Devolve o texto contido na string, limpo e justificado 
    de acordo com a largura de coluna desejada na forma de um tuplo

    justifica_texto: str x int --> tuple
    '''
    #Verificação da validade dos argumentos
    if type(texto)!=str or len(texto)==0 or type(larg)!=int or larg<=0: 
        raise ValueError('justifica_texto: argumentos invalidos')
    p_maiores = texto.split()
    for i in range(0, len(p_maiores)):
        if len(p_maiores[i])>larg:
            raise ValueError('justifica_texto: argumentos invalidos')
    
    #Limpa o texto e divide em duas strings, num tuplo, ficando a primeira já pronta para ser justificada
    texto = corta_texto(limpa_texto(texto),larg)     
    tfinal = ()
    i=1

    #Divide sucessivamente as strings de modo a estarem prontas para serem justificadas
    while texto[i]!= '':         
        texto = texto[:i] + corta_texto(texto[i],larg)
        i+= 1 
    
    if texto[-1] == '':
        texto = texto[:-1] 

    #Adiciona os espaçamentos necessários entre palavras para cada string do tuplo 
    for i in range (len(texto)):             
        if i == len(texto)-1:              
            x = espaco_uma_palavra(texto[i],larg)
            tfinal+=(x,)
        #Para a última string do tuplo, apenas adiciona espaços até chegar à largura da coluna necessária
        else:
            tfinal += (insere_espacos(texto[i], larg),)
    
    return tfinal


#2 - Método de Hondt

def calcula_quocientes(votos_circulo, numDep):
    '''
    votacoes --> dicionário com os votos de um circulo
    numDep --> inteiro que representa o número de deputados
    
    Devolve um dicionário que associa a cada partido 
    uma lista com os quocientes do método de Hondt 

    calcula_quocientes: dict x int --> dict
    '''
    votacoes_Hondt=votos_circulo.copy()
    for partido in votos_circulo:
        votos_Hondt =[]

        #Aplicação do Método de Hondt a cada partido do circulo eleitoral
        for i in range(1,numDep+1):  
            votos_Hondt+=[votos_circulo[partido]/i]
            votacoes_Hondt[partido] = votos_Hondt

    return votacoes_Hondt

def atribui_mandatos(votacoes, numDep):
    '''
    votacoes --> dicionário com os votos de um circulo eleitoral
    numDep --> inteiro que representa o número de deputados eleitos nesse circulo

    Devolve uma lista com o nome do partido que obteve cada mandato

    atribui_mandatos: dict x int --> list
    '''

    l_mandatos, l_nvotos, partidos_votos_iguais = [], [], []
    votacoes_Hondt = calcula_quocientes(votacoes, numDep)

    #Lista com todos os quocientes dos votos, excluindo os repetidos
    for el in votacoes_Hondt:
        for i in range (len(votacoes_Hondt[el])):
            if votacoes_Hondt[el][i] not in l_nvotos:
                l_nvotos+=[votacoes_Hondt[el][i]]
        l_nvotos.sort(reverse=True)   #Do maior para o menor


    for i in range(len(l_nvotos)):
        partidos_votos_iguais = []

        #Lista com os partidos que obtiveram o quociente
        for el in votacoes_Hondt:
            if l_nvotos[i] in votacoes_Hondt[el]:
                partidos_votos_iguais +=[el]

        #Se houver mais que um partido com o mesmo quociente 
        #Entrega primeiro o mandato ao que tiver menos deputados
        if len(partidos_votos_iguais)>1:
            for k in range(len(partidos_votos_iguais)):
                ordenado=True
                for j in range(len(partidos_votos_iguais)-1-k):
                    if votacoes[partidos_votos_iguais[j]] > votacoes[partidos_votos_iguais[j+1]]:
                        partidos_votos_iguais[j],partidos_votos_iguais[j+1]=partidos_votos_iguais[j+1], partidos_votos_iguais[j]
                        ordenado= False
                if ordenado:
                    break 
        l_mandatos+=partidos_votos_iguais
    
    #Atribui apenas o número de deputados pré-definido
    l_mandatos=l_mandatos[:numDep]        
    return l_mandatos

def obtem_partidos (votacoes):
    '''
    votacoes --> dicionário com a informação sobre as eleiçoes de vários circulos eleitorais

    Devolve uma lista com todas os partidos que participaram nas eleições por ordem alfabética

    obtem_partidos: dict --> list
    '''
    partidos=[]
    #Procura todos os partidos que estejam nas votações e adiciona-os à lista
    for circulo in votacoes:
        for partido in votacoes[circulo]['votos']:   
            if partido not in partidos:      
                partidos+= [partido]

    partidos.sort()
    return partidos

def obtem_resultado_eleicoes(votacoes):
    '''
    votacoes --> dicionario com a informaçao sobre as eleiçoes num território com vários círculos eleitorais
    Devolve uma lista de tuplos, cada tuplo contém:
                o nome de um partido
                o número total de deputados 
                o número total de votos desse partido

    obtem_resultado_eleicoes: dict --> list
    '''
    #Verificação dos erros
    if votacoes =={} or type(votacoes)!= dict or len(votacoes)==0:
        raise ValueError ('obtem_resultado_eleicoes: argumento invalido')

    n_circulos=0
    for circulo in votacoes:
        n_circulos+=1
        n_partidos = 0

        if type(circulo)!= str or type(votacoes[circulo])!=dict or len(votacoes[circulo])!=2 or\
            'votos' not in votacoes[circulo].keys()  or 'deputados' not in votacoes[circulo].keys()\
            or type(votacoes[circulo]['votos'])!=dict or type(votacoes[circulo]['deputados'])!= int:

            raise ValueError ('obtem_resultado_eleicoes: argumento invalido')

        for partido in votacoes[circulo]['votos']:
            if len(votacoes[circulo]['votos'])<1 or type(votacoes[circulo]['votos'][partido])!=int or\
            votacoes[circulo]['votos'][partido]<0 or type(partido)!=str:

                raise ValueError('obtem_resultado_eleicoes: argumento invalido')

            elif votacoes[circulo]['votos'][partido]>0:
                n_partidos+=1

        if n_partidos <1 or votacoes[circulo]['deputados'] <1:
            raise ValueError ('obtem_resultado_eleicoes: argumento invalido')


    mandatos, n_deputados, votos_total=[],{},{}
    partidos_nomes= obtem_partidos(votacoes) #Lista de todos os partidos

    #Lista com o partido que ganhou cada mandato
    for circulo in votacoes:
        mandatos+=atribui_mandatos(votacoes[circulo]['votos'], votacoes[circulo]['deputados'])   
        
    #Dicionário contendo todos os partidos e o número de deputados de cada partido
    for partido in partidos_nomes:  
        n_deputados[partido]=0     
    for partido in mandatos:
        n_deputados[partido]+=1

    #Dicionário contendo o total de votos de cada partido
    for circulo in votacoes:     
        for partido in n_deputados:
            if partido not in votos_total and partido in votacoes[circulo]['votos']:
                votos_total[partido]=votacoes[circulo]['votos'][partido]
            elif partido in votacoes[circulo]['votos']:
                votos_total[partido]+=votacoes[circulo]['votos'][partido]
    
    #Cria a lista de tuplos contendo para cada partido o seu nome, o numero de deputados e o total de votos
    resultados_eleicoes =[]
    for partido in partidos_nomes:
        resultados_eleicoes+=[(partido,n_deputados[partido], votos_total[partido])]

    #Ordena a lista
    for k in range(len(resultados_eleicoes)):
                ordenado=True
                for j in range(len(resultados_eleicoes)-1-k):
                    if resultados_eleicoes[j][1] < resultados_eleicoes[j+1][1]:     #Ordem descendente do número de deputados
                        resultados_eleicoes[j],resultados_eleicoes[j+1]=resultados_eleicoes[j+1], resultados_eleicoes[j]
                        ordenado= False
                    elif resultados_eleicoes[j][1] == resultados_eleicoes[j+1][1]:   #Se o número de deputados for igual:
                        if resultados_eleicoes[j][2] < resultados_eleicoes[j+1][2]:  #Ordem descendente do número de votos 
                            resultados_eleicoes[j],resultados_eleicoes[j+1]=resultados_eleicoes[j+1], resultados_eleicoes[j]
                            ordenado= False
                if ordenado:
                    break 
    return resultados_eleicoes

#3 - Sistemas lineares

def produto_interno (v1,v2):
    '''
    v1, v2: Dois tuplos de números inteiros ou reais com as mesmas dimensões
    Devolve o resultado (real) do produto dos vetores

    produto_interno: tuple x tuple --> float
    '''
    prod_int= 0.0
    for i in range(len(v1)):    
        prod_int += v1[i]*v2[i]
    return prod_int

def verifica_convergencia(mA, vConst, solX, prec):
    '''
    mA: Tuplo consitituído por um conjunto de tuplos que representam uma linha de uma matriz quadrada
    vConst: Tuplo que representa o vetor das constantes
    solX: Tuplo que representa a solução 
    prec: Valor real que indica a precisão pretendida para a solução

    Devolve True se o valor absoluto do erro for inferior à precisão e False caso contrário

    verifica_convergencia: tuple x tuple x tuple x float --> bool
    '''
    resultado=()
    for l in range (len(mA)):
        resultado += (produto_interno(mA[l], solX),)
        if abs(resultado[l]-vConst[l])>=prec:
            return False

    return True

def troca_linhas(lA,lConst,linha,col):
    '''
    lA: lista que representa uma matriz
    lConst: lista que representa o vetor das constantes
    linha: linha da matriz
    col: coluna da matriz

    Devolve a matriz e o vetor das constantes com as linhas trocadas

    troca_linhas: list x list x int x int --> list x list
    '''
    l_trocar=0
    while l_trocar<len(lA):
        if lA[l_trocar][col]!=0 and lA[linha][l_trocar]!=0:
            lA[linha],lA[l_trocar]=lA[l_trocar],lA[linha]
            lConst[linha],lConst[l_trocar]=lConst[l_trocar],lConst[linha]

            return lA,lConst
        l_trocar+=1

def retira_zeros_diagonal(mA, vConst):
    '''
    mA: tuplo que representa uma matriz
    vConst: tuplo que representa o vetor das constantes
    Devolve dois tuplos: 
                a matriz original reordenada 
                o vetor das constantes reordenada de acordo com a matriz
    
    retira_zeros_diagonal: tuple x tuple --> tuple x tuple
    '''
    lA, lConst=list(mA), list(vConst)
    
    for linha in range(len(mA)):
        #Se o valor da entrada da diagonal for 0
        if mA[linha][linha]==0:
            troca_linhas(lA,lConst,linha,linha)       

    return tuple(lA), tuple(lConst) 

def eh_diagonal_dominante(mA):
    '''
    mA:Tuplo que representa uma matriz quadrada
    Devolve True se a matriz for diagonal dominante e False caso contrário

    eh_diagonal_dominante: tuple --> bool
    '''

    for l in range(len(mA)):
        i_diag, soma_el, c = 0, 0, 0
        
        while c<len(mA[l]): 
            if c == l:
                i_diag =abs(mA[l][c])
            else:
                soma_el+=abs(mA[l][c])
            c+=1

        if i_diag<soma_el:
            return False
            
    return True
            
def resolve_sistema(mA,vConst,prec):
    '''
    mA: tuplo que representa uma matriz quadrada
    vConst: tuplo que representa um vetor de constantes
    prec: valor real que representa a precisão pretendida para a solução

    Valida as entradas e caso sejam válidas resolve o sistema utilizando o método de Jacobi
    Devolve a solução

    resolve_sistema: tuple x tuple x float --> tuple
    '''
    
    #Validação os argumentos
    if not isinstance(mA,tuple) or len(mA)==0 or not isinstance (vConst,tuple)\
       or not isinstance(prec,(int,float)) or prec>=1 or prec<=0:
        raise ValueError('resolve_sistema: argumentos invalidos')

    for el in vConst:
        if not isinstance(el,(int,float)):
            raise ValueError('resolve_sistema: argumentos invalidos')

    for i in range(len(mA)):
        num_el_lin = len(mA[0])

        if not isinstance(mA[i],tuple) or len(mA)!=len(mA[i]) or num_el_lin!=len(mA[i]) or len(mA[i])!=len(vConst):
            raise ValueError('resolve_sistema: argumentos invalidos')

        for c in range(len(mA[i])):
            if not isinstance(mA[i][c],(int,float)):
                raise ValueError('resolve_sistema: argumentos invalidos')
    
    mA, vConst = retira_zeros_diagonal(mA, vConst)
    if eh_diagonal_dominante(mA) is False:
        raise ValueError('resolve_sistema: matriz nao diagonal dominante')

    #De acordo com o método de Jacobi a solução inicial é o vetor nulo
    lsolX=[0 for i in range(len(mA))]

    #Aplicação do método de Jacobi e da fórmula dada 
    while not verifica_convergencia(mA, vConst, tuple(lsolX), prec):
        solXa= lsolX.copy()   #solução da iteração anterior                                              
        for i in range(len(mA)):
            f = produto_interno(mA[i],tuple(solXa))
            lsolX[i] =lsolX[i] +(((vConst[i]-f))/mA[i][i])

    return tuple(lsolX)


