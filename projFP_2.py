#Projeto 2: Minesweeper

#Gerador

#Construtores:

def cria_gerador(b,s):
    '''
    b --> numero de bits do gerador
    s --> seed
    Devolve o gerador correspondente
    cria_gerador: int x int --> gerador
    '''
    if not isinstance(b,int) or not isinstance(s,int) \
    or s<=0 or (b!=32 and b!=64) or s>2**b:
        raise ValueError('cria_gerador: argumentos invalidos')

    
    return [b,s]

def cria_copia_gerador(g):
    '''
    cria_novo_gerador: gerador --> gerador
    '''
    return g.copy()

#Seletores:

def obtem_estado(g):
    '''
    Devolve o estado do gerador
    obtem_estado: gerador -->int
    '''
    return g[1]

#Modificadores:

def define_estado(g, s):
    '''
    Define s como novo valor do estado do gerador
    define estado: gerador x int --> int
    '''
    g[1] = s
    return g[1]

def atualiza_estado(g):
    '''
    Atualiza o estado do gerador segundo o algoritmo xorshift
    atualiza_estado: gerador --> int
    '''
    if g[0]==32:
        g[1] ^=(g[1]<<13) & 0xFFFFFFFF
        g[1] ^=(g[1]>>17) & 0xFFFFFFFF
        g[1] ^=(g[1]<<5)  & 0xFFFFFFFF
    elif g[0] == 64:
        g[1] ^=(g[1]<<13) & 0xFFFFFFFFFFFFFFFF
        g[1] ^=(g[1]>>7)  & 0xFFFFFFFFFFFFFFFF
        g[1] ^=(g[1]<<17) & 0xFFFFFFFFFFFFFFFF

    return obtem_estado(g)

#Reconhecedor:

def eh_gerador(arg):
    '''
    Verifica se o argumento é um gerador 
    (True: é gerador, False: não é)

    eh_gerador: universal --> boolean
    '''
    return isinstance(arg,list) and len(arg) == 2 and isinstance(arg[0],int)\
    and isinstance(arg[1],int) and (arg[0]==32 or arg[0]==64)\
    and arg[1]<2**arg[0] and arg[1]>0

#Teste:

def geradores_iguais (g1,g2):
    '''
    Verifica se os dois geradores são iguais
    geradores_iguais: gerador x gerador --> boolean
    '''
    return g1[0] == g2[0] and obtem_estado(g1)== obtem_estado(g2)

#Transformador:

def gerador_para_str(g):
    '''
    Devolve uma string representativa do gerador
    gerador_para_str: gerador --> str
    '''
    return str('xorshift'+ str(g[0])+'(s='+ str(obtem_estado(g))+')')

#Funcões de alto nível:

def gera_numero_aleatorio(g,n):
    '''
    Atualiza o estado do gerador
    Devolve um número entre 1 e n obtido através da seguinte equação:
    1 + s%n         (s=novo estado do gerador)
    gera_numero_aleatorio: gerador x int --> int
    '''
    return 1 + atualiza_estado(g)%n

def gera_carater_aleatorio(g,c):
    '''
    Devolve o carater numa lista de carateres entre 'A' e c 
    cuja sua posição seja igual a:
    s%l --> (s: estado atualiza do gerador) 
            (l: comprimento da lista)
    
    gera_numero_aleatorio: gerador x str --> str
    '''
    #O comprimento da lista é a diferença entre os codigos 
    #De ambas as letras na tabela Unicode +1
    num_caracter=atualiza_estado(g)%(ord(c)-ord('A')+1)

    return chr(ord('A')+num_caracter)


#Coordenada:

#Construtor:

def cria_coordenada(col,lin):
    '''
    col --> coluna
    lin --> linha
    Devolve a coordenada correspondente

    cria_coordenada: str x int --> coordenada
    '''
    if  not isinstance(col, str) or not isinstance(lin, int) or\
        len(col)!=1 or lin<1 or lin>99 or ord(col)<65 or ord(col)>90:
        raise ValueError('cria_coordenada: argumentos invalidos')

    return {'coluna': col, 'linha': lin}

#Seletores:

def obtem_coluna(c):
    '''
    c --> coordenada
    Devolve a coluna da coordenada

    obtem_coluna: coordenada --> str
    '''
    return c['coluna']

def obtem_linha(c):
    '''
    c --> coordenada
    Devolve a linha da coordenada

    obtem_linha: coordenada --> int
    '''    
    return c['linha']

#Reconhecedor:

def eh_coordenada(arg):
    '''
    Verifica se um argumento é uma coordenada

    eh_coordenada: universal --> boolean
    '''
    return isinstance(arg, dict) and len(arg)==2 and 'linha' in arg\
    and 'coluna' in arg and isinstance(obtem_linha(arg), int)\
    and isinstance(obtem_coluna(arg), str)\
    and 0<obtem_linha(arg)<=99 and 65<=ord(obtem_coluna(arg))<=90

#Teste:

def coordenadas_iguais(c1,c2):
    '''
    c1 e c2 --> coordenada1 e coordenada2
    Verifica se as coordenadas são iguais
    
    coordenadas_iguais: coordenada x coordenada --> boolean
    '''
    return obtem_coluna(c1)==obtem_coluna(c2)\
        and obtem_linha(c1)==obtem_linha(c2)

#Transformador:

def coordenada_para_str(c):
    '''
    c --> coordenada
    Devolve a coordenada sob a forma de string:
    Primeiro aparece a letra correspondente à coluna
    Depois o inteiro correspondente a linha

    coordenada_para_string: coordenada --> str
    '''

    return str(obtem_coluna(c)+(str(obtem_linha(c))if obtem_linha(c)>9\
                            else ('0'+str(obtem_linha(c)))))

def str_para_coordenada(s):
    '''
    s --> string correspondente a uma coordenada
    Devolve a coordenada correspondente

    str_para_coordenada: str -->coordenada
    '''

    #Se a coordenada estiver entre as linhas 1 e 9
    #Na string estará representado '0X'
    #Nesse caso retiramos apenas o 'X'
    lin = int(s[1:]) if int(s[1:])>9 else int(s[2])
    return cria_coordenada(s[0],lin)
      
#Funções de Alto Nível

def obtem_coordenadas_vizinhas(c):
    '''
    c --> coordenada
    Devolve um tuplo com as coordenadas vizinhas
    Primeiro a da diagonal acima-esquerda 
    e as seguintes no sentido horário

    obtem_coordenadas_vizinhas: coordenada --> tuple
    '''

    t=()
    def try_coordenada(col,lin,t):
        '''
        Testa se a coordenada existe e, caso exista 
        Adiciona-a ao tuplo t
        '''
        try:
            cria_coordenada(col,lin)
        except:
            ''
        else:
            t+=(cria_coordenada(col,lin),)
        finally:   
            return t

    #Linha acima da coordenada
    for coluna in range (-1,2):
        linha=-1
        t = try_coordenada(chr(ord(obtem_coluna(c))+coluna), obtem_linha(c)+linha,t)

    #Coordenada à direita
    t = try_coordenada(chr(ord(obtem_coluna(c))+1),obtem_linha(c),t)

    #Linha abaixo da coordenada
    for coluna in range (1,-2,-1):
        linha = 1
        t = try_coordenada(chr(ord(obtem_coluna(c))+coluna), obtem_linha(c)+linha,t)
    
    #Coordenada à esquerda
    t = try_coordenada(chr(ord(obtem_coluna(c))-1),obtem_linha(c),t)
    
    return t

def obtem_coordenada_aleatoria(c, g):
    '''
    c --> coordenada(maior coluna e maior linha possíveis)
    g --> gerador

    Devolve uma coordenada gerada aleatoriamente
    obtem_coordenada_aleatoria: coordenada x gerador --> coordenada
    '''
    return cria_coordenada(gera_carater_aleatorio(g,obtem_coluna(c)),\
                            gera_numero_aleatorio(g,obtem_linha(c)))


#Parcelas

#Construtores:

def cria_parcela():
    '''
    Devolve uma parcela tapada e sem mina

    cria_parcela:{}-->parcela
    '''
    return {'estado': 'tapada', 'mina': 'não'}

def cria_copia_parcela(p):
    '''
    Devolve uma nova cópia da parcela p

    cria_copia_parcela:parcela --> parcela
    '''
    p_copy ={'estado': p['estado'], 'mina': p['mina']}

    return p_copy

#Modificadores:

def limpa_parcela(p):
    '''
    Modifica o estado da parcela para limpa
    Devolve a própria parcela (modificada)

    limpa_parcela: parcela --> parcela
    '''

    p['estado'] = 'limpa'
    return p

def marca_parcela(p):
    '''
    Modifica o estado da parcela para marcada
    Devolve a própria parcela (modificada)

    marcaa_parcela: parcela --> parcela
    ''' 
    p['estado'] = 'marcada'
    return p

def desmarca_parcela(p):
    '''
    Modifica o estado da parcela para tapada
    Devolve a própria parcela (modificada)

    desmarca_parcela: parcela --> parcela
    '''    
    p['estado'] = 'tapada'
    return p

def esconde_mina(p):
    '''
    Modifica a parcela para conter uma mina
    Devolve a própria parcela (modificada)

    esconde_mina: parcela --> parcela
    '''
    p['mina'] = 'sim'
    return p

#Reconhecedores:

def eh_parcela(arg):
    '''
    Verifica se um dado argumento é uma parcela

    eh_parcela:universal --> boolean
    '''
    return isinstance(arg,dict) and len(arg)==2 and 'estado' in arg and 'mina' in arg\
        and isinstance(arg['estado'], str) and arg['estado'] in ['limpa', 'marcada', 'tapada']\
        and isinstance(arg['mina'], str) and arg['mina'] in ['sim', 'não']

def eh_parcela_tapada(p):
    '''
    Verifica se uma dada parcela está tapada

    eh_parcela_tapada:parcela --> boolean
    '''
    return p['estado'] == 'tapada'

def eh_parcela_marcada(p):
    '''
    Verifica se uma dada parcela está marcada

    eh_parcela_marcada:parcela --> boolean
    '''
    return p['estado'] == 'marcada'

def eh_parcela_limpa(p):
    '''
    Verifica se uma dada parcela está limpa

    eh_parcela_limpa:parcela --> boolean
    '''
    return p['estado'] == 'limpa'

def eh_parcela_minada(p):
    '''
    Verifica se uma dada parcela contém uma mina

    eh_parcela_minada:parcela --> boolean
    '''
    return p['mina'] == 'sim'

#Teste:

def parcelas_iguais(p1,p2):
    '''
    Verifica se duas parcelas são iguais

    parcelas_iguais:parcela x parcela --> boolean
    '''
    return p1['estado']==p2['estado'] and\
        eh_parcela_minada(p1)==eh_parcela_minada(p2)

#Transformadores:

def parcela_para_str(p):
    '''
    Devolve a string que representa o estado da parcela:
    # --> parcela tapada
    @ --> parcea marcada
    ? --> parcela limpa e não minada
    X --> parcela limpa e minada

    parcela_para_str:parcela --> str
    '''
    if eh_parcela_tapada(p):
        return '#'
    elif eh_parcela_marcada(p):
        return '@'
    elif eh_parcela_limpa(p) and not eh_parcela_minada(p):
        return '?'
    elif eh_parcela_limpa(p) and eh_parcela_minada(p):
        return 'X'

#Funçoes de Alto Nível:

def alterna_bandeira(p):
    '''
    Modifica uma parcela da seguinte forma:
    Desmarca se estiver marcada
    Marca se estiver tapada

    Se a parcela for modifica devolve True

    alterna_bandeira:parcela --> boolean
    '''

    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    return False


#Campo

#Construtor:

def cria_campo(c,l):
    '''
    c --> última coluna do campo
    l --> última linha do campo

    Devolve o campo formado por parcelas tapadas sem minas

    cria_campo:str x int --> campo
    '''
    if not isinstance(c,str) or not isinstance(l,int)\
        or len(c)!=1 or l<1 or l>99 or ord(c)<65 or ord(c)>90:
        raise ValueError('cria_campo: argumentos invalidos')
    campo={}
    for lin in range(1,l+1):
        for col in range(65,ord(c)+1):
            if lin not in campo.keys():
                campo[lin]=[cria_parcela()]
            else:
                campo[lin]+=[cria_parcela()]

    return campo

def cria_copia_campo(m):
    '''
    Devolve uma cópia do campo m

    cria_copia_campo:campo --> campo
    '''
    m_copy={}
    for key in m:
        for parcela in m[key]:
            if key not in m_copy:
                m_copy[key]=[cria_copia_parcela(parcela)]
            else:
                m_copy[key]+=[cria_copia_parcela(parcela)]
    return m_copy

#Seletores:

def obtem_ultima_coluna(m):
    '''
    Devolve a str correspondente à ultima coluna

    obtem_ultima_coluna:campo --> str
    '''
    return chr(64+len(m[1]))

def obtem_ultima_linha(m):
    '''
    Devolve o inteiro correspondente à ultima linha

    obtem_ultima_linha:campo --> int
    '''
    return len(m)

def obtem_parcela(m,c):
    '''
    Devolve a parcela que se encontra na coordenada c

    obtem_parcela:campo x coordenada --> parcela
    '''
    return m[obtem_linha(c)][ord(obtem_coluna(c))-65]

def obtem_coordenadas(m,s):
    '''
    Devolve um tuplo com todas as coordenadas cujas parcelas 
    tenham o mesmo valor de s

    obtem_coordenadas:campo x str --> tuple
    '''
    t=()
    if s == 'limpas':
        estado = eh_parcela_limpa
    elif s == 'tapadas':
        estado = eh_parcela_tapada
    elif s == 'marcadas':
        estado = eh_parcela_marcada
    elif s == 'minadas':
        estado= eh_parcela_minada

    for l in range(1,obtem_ultima_linha(m)+1):
        for c in range(ord('A'), ord(obtem_ultima_coluna(m))+1):
            parc = obtem_parcela(m,cria_coordenada(chr(c),l))

            if estado(parc): 
                t+=(cria_coordenada(chr(c),l),)

    return t
 
def obtem_numero_minas_vizinhas(m,c):
    '''
    Devolve o numero de parcelas vizinhas que escondem uma bomba

    obtem_numero_minas_vizinhas:campo x coordenada --> int
    '''
    num_minas=0
    c_vizinhas = obtem_coordenadas_vizinhas(c)
    for coord in c_vizinhas:
        if eh_coordenada_do_campo(m,coord):
            if eh_parcela_minada(obtem_parcela(m,coord)):
                num_minas +=1
    
    return num_minas

#Reconhecedores:

def eh_campo(arg):
    '''
    Verifica se um dado argumento é um campo

    eh_campo:universal --> boolean
    '''
    val = False
    if isinstance(arg, dict):
        for lin in arg.keys():
            val = len(arg[lin])==len(arg[1]) 
            if not val:
                break
        return val and 0<len(arg)<99 and 0<len(arg[1])<27
    return val

def eh_coordenada_do_campo(m,c):
    '''
    Verifica se a coordenada c é válido no campo m

    eh_coordenada_do_campo:campo x coordenada --> boolean
    '''
    return 0<obtem_linha(c)<=obtem_ultima_linha(m) and\
         ord('A')<=ord(obtem_coluna(c))<=ord(obtem_ultima_coluna(m))

#Teste:

def campos_iguais(m1,m2):
    '''
    Verifica se os dois campos são iguais

    campos_iguais:campo x campo --> boolean
    '''

    val = False
    if eh_campo(m1) and eh_campo(m2):
        if obtem_ultima_coluna(m1)==obtem_ultima_coluna(m2) and\
             obtem_ultima_linha(m1)==obtem_ultima_linha(m2):
            
            val = True
            for lin in m1.keys():
                for parc in range(len(m1[lin])):
                    if not parcelas_iguais(obtem_parcela(m1,cria_coordenada(chr(65+parc),lin)), obtem_parcela(m2,cria_coordenada(chr(65+parc),lin))):
                        val = False
                        break
                        
    return  val

#Transformador:

def campo_para_str(m):
    '''
    Devolve uma str que representa o campo de minas

    campo_para_str:campo --> str
    '''
    #String com todas as letras das colunas
    colunas = ''.join([chr(x) for x in range(ord('A'),\
                ord(obtem_ultima_coluna(m))+1)])

    sep = '+'+str('-'*(len(colunas)))+'+'

    #Transforma as parcelas nos seus simbolos
    m_copy = cria_copia_campo(m)
    for lin in m:
        for col in range(len(m[lin])):
            coord = cria_coordenada(chr(65+col),lin)
            parc = obtem_parcela(m_copy,coord)
            if not eh_parcela_limpa(parc) or\
            (eh_parcela_limpa(parc) and eh_parcela_minada(parc)): 

                m_copy[lin][col] = parcela_para_str(parc)
            else:
            
                m_copy[lin][col] = str(obtem_numero_minas_vizinhas(m,coord))\
                    if obtem_numero_minas_vizinhas(m,coord)!=0 else ' '

    #String com as linhas e os simbolos para cada parcela
    linhas = '\n'.join([(str(lin) +'|'+ ''.join(m_copy[lin])+'|') if lin>9 else\
         ('0'+str(lin)+'|'+ ''.join(m_copy[lin])+'|') for lin in m.keys()])

    return str('   '+str(colunas)+'\n'+'  '+sep+'\n'+linhas+'\n  '+sep)

#Funções de Alto Nível

def coloca_minas(m,c,g,n):
    '''
    Devolve o campo m com n minas escondidas em coordenadas não
    coincidentes com c nem com as suas coordenadas vizinhas

    coloca_minas:campo x coordenada x gerador x inteiro --> campo
    '''    
    
    coordenadas_excluidas=obtem_coordenadas_vizinhas(c) + (c,)
    while n>0:
        coordenada_aleatoria=obtem_coordenada_aleatoria(cria_coordenada\
                      (obtem_ultima_coluna(m),obtem_ultima_linha(m)),g)
     
        if coordenada_aleatoria not in coordenadas_excluidas and\
        not eh_parcela_minada(obtem_parcela(m,coordenada_aleatoria)):

            esconde_mina(obtem_parcela(m,coordenada_aleatoria))
            
            n-=1

    return m

def limpa_campo(m,c):
    '''
    Devolve o campo com a parcela na coordenada c limpa
    Se não houver nenhuma mina vizinha escondida 
    Limpa todas as parcelas vizinhas tapadas

    limpa_campo:campo x coordenada --> campo
    '''
    limpa_parcela(obtem_parcela(m,c))
    coordenadas_vizinhas=obtem_coordenadas_vizinhas(c)
    if eh_parcela_limpa(obtem_parcela(m,c)) and\
       obtem_numero_minas_vizinhas(m,c)==0\
       and not eh_parcela_minada(obtem_parcela(m,c)):

        for coords in coordenadas_vizinhas:
            if eh_coordenada_do_campo(m,coords):
            
                if eh_parcela_tapada(obtem_parcela(m,coords))\
                   and not eh_parcela_minada(obtem_parcela(m,coords)):
                    limpa_campo(m,coords)                
    return m

#Funções Adicionais:

def jogo_ganho(m):
    '''
    Verifica se todas as parcelas sem minas se encontram limpas

    jogo_ganho:campo --> boolean
    '''
    tamanho_campo = (1+(ord(obtem_ultima_coluna(m))-ord('A')))*\
                    obtem_ultima_linha(m)
    return tamanho_campo-len(obtem_coordenadas(m,'minadas'))\
        == len(obtem_coordenadas(m,'limpas'))

def escolhe_coordenada(m):
    coord= ''
    def coord_error(m, coord):
        '''
        Verifica se o input recebido é uma coordenada válida
        '''

        try: 
            eh_coordenada_do_campo(m, str_para_coordenada(coord))  
        except:
            return False
        else:
            return eh_coordenada_do_campo(m,str_para_coordenada(coord))
    
    while not coord_error(m,coord):
        coord = input('Escolha uma coordenada:')
    
    return str_para_coordenada(coord)

def turno_jogador(m):
    '''
    Oferece ao jogador a hipótese de escolher:
    Uma coordenada e uma ação

    Modifica o campo de acordo com a ação escolhida:
    Marcar ou Limpar

    Caso limpe uma mina devolve False 

    turno_jogador:campo --> boolean
    '''
    acao = input('Escolha uma ação, [L]impar ou [M]arcar:')
    while acao not in ['M','L']:
        acao= input('Escolha uma ação, [L]impar ou [M]arcar:')
    

    coord = escolhe_coordenada(m)

    if acao == 'M':
        alterna_bandeira(obtem_parcela(m,coord))
    elif acao == 'L':
        limpa_campo(m,coord)
        return not eh_parcela_minada(obtem_parcela(m,coord))
    return True

#Função Principal do Jogo:

def minas(c,l,n,d,s):
    '''
    c --> última coluna (str)
    l --> última linha (int)
    n --> número de parcelas com minas (int)
    d --> dimensão do gerador (int)
    s --> estado inicial/seed do gerador (int)

    Função principal do jogo
    Devolve True se o jogador conseguir ganhar o jogo

    minas:str x int x int x int x int --> boolean
    '''
    try:
        cria_campo(c,l)
    except:
        raise ValueError('minas: argumentos invalidos')
    try:
        cria_gerador(d,s)
    except:
        raise ValueError('minas: argumentos invalidos')

    if not isinstance(n,int) or n<1 or n>(((ord(c)-ord('A'))*l)-9):
         raise ValueError('minas: argumentos invalidos')
    
    g = cria_gerador(d,s)
    m = cria_campo(c,l)

    def layout_campo(m):
        '''
        Dá print ao layout do campo
        '''
        bandeiras = len(obtem_coordenadas(m,'marcadas'))
        print(f'   [Bandeiras {bandeiras}/{n}]\n{campo_para_str(m)}')
    
    layout_campo(m)
    c_inicial = escolhe_coordenada(m)
    coloca_minas(m,c_inicial,g,n)
    limpa_campo(m,c_inicial)

    #Continua o jogo até todas as parcelas sem minas tenham sido limpas
    while not jogo_ganho(m):
        layout_campo(m)
        
        #Caso uma parcela com mina tenha sido limpa
        #Acaba o jogo
        for coords in obtem_coordenadas(m, 'minadas'):
            if coords in obtem_coordenadas(m,'limpas'):
                print('BOOOOOOOM!!!')
                return False 
        
        turno_jogador(m)
    
    layout_campo(m)    
    print('VITORIA!!!')
    return True
