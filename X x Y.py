import math
import random


def dectobin(decimal, formatar):  # função para converter um número de decimal para binário e formatar ele para dada
    # quantidade de bits
    lista = list()
    if decimal == 0:
        lista.append('0')
    else:
        while decimal > 1:
            decimal = decimal / 2
            if decimal.is_integer():
                lista.append('0')
            else:
                lista.append('1')
            decimal = int(decimal)
        lista.append('1')
    while len(lista) != formatar:  # laço responsável por normalizar o número binário na quantidade especificada de bits
        lista.append('0')

    lista.reverse()
    string = ''.join(lista)
    return string


def bintodec(binario):  # função para converter um número em base decimal para um em base binária
    binario = list(binario)
    binario.reverse()
    final = 0
    ordem = 0
    for x in binario:
        calculo = 2 ** ordem * int(x)
        final += calculo
        ordem += 1
    return final


potencia_celulas = {  # dicionário usado para traduzir os múltiplos em potências (de dois)
    "K": 10,
    "M": 20,
    "G": 30,
    "None": 0
}

partenumero = []
parteletra = "None"  # define um valor default para caso não haja letra a ser convertida em potência

ram = input("Entre com o número de células da memória: ")

for i in list(ram):  # condicional que vai isolar o número inserido e categorizar o múltiplo
    if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        partenumero.append(i)
    else:
        parteletra = i

partenumero = ''.join(partenumero)  # junta a lista criada no laço condicional em uma string

potencia = int(math.log2(int(partenumero)) + potencia_celulas[parteletra])  # decompõe o número em sua devida
# potência de dois e soma com o valor do múltiplo inserido

ram = [None] * int(2 ** potencia)  # cria uma lista que vai servir como nosso bloco de memória principal,
# onde o index é o endereço da célula e o conteúdo é a palavra contida na célula (aqui cria-se uma memória
# essencialmente vazia)

for i in range(0, int(2 ** potencia)):  # esse laço for será responsável por preencher todas as células da memória com
    # número aleatório (número é dado em decimal e a função dectobin transforma o número em um binário de 8 bits)
    ram[i] = dectobin(random.randint(0, 4096), 12)

razao_bloco = int(potencia * (27 / 32))  # essa razão será usada para delimitar quantos bits do endereço vão
# endereçar os blocos da cache
razao_tag = int(razao_bloco * (7 / 8))  # essa razão será usada para delimitar quantos bits serão usados para endereçar


# a tag na memória cache


def end_cache(end_ram):  # o objetivo dessa função é receber um endereço da memória RAM e separar os devidos bits que
    # vão endereçar a tag, o conjunto e o byte na memória cache
    split_end = [end_ram[0:razao_tag], end_ram[razao_tag: razao_bloco], end_ram[razao_bloco:potencia]]
    return split_end


end_memoria = end_cache(dectobin(2 ** potencia - 1, potencia))  # pega o maior endereço da memória ram e joga na
# função end_cache
print(end_memoria)
n_linha_cache = 2 ** int(len((end_memoria[0] + end_memoria[1])) / 2)  # calcula a quantidade de linhas da cache
print(n_linha_cache)
n_coluna_cache = 1 + 2 ** len(end_memoria[2])  # calcula a quantidade de colunas da cache
n_conj_cache = 2 ** int(len(end_memoria[1]))  # calcula a quantidade de conjuntos da cache
memoria_cache_conj = []
memoria_cache = []  # coloca essa linha dentro de uma lista

for i in range(0, n_linha_cache):  # loop for responsavel por criar a memória cache, já com a separação dos subconjuntos
    memoria_cache += [[None] * n_coluna_cache]  # cria uma linha da memoria cache com o devido número de colunas
    if (i + 1) % (n_linha_cache / n_conj_cache) == 0:  # se o  número de linhas na lista memoria_cache for igual ao
        # número de linhas que cabem em um conjunto, o programa vai armazenar essa lista dentro da lista
        # memoria_cache_conj e vai limpar a lista memoria_cache para que o processo se repita
        memoria_cache_conj.extend([memoria_cache])
        memoria_cache = []

bloco_backup = []  # essa lista armazenará os dados dos blocos (tag e linha) que foram modificados enquanto na
# memória cache
bloco_backup_final = []
for i in memoria_cache_conj:  # loop for responsavel por criar uma matrix para o programa lembrar qual linha foi
    # modificada. a linha especificada dessa matriz funcionará como conjunto e a coluna especificada funcionará como
    # linha da cache
    for j in i:
        bloco_backup.extend(['3'])
    bloco_backup_final.extend([bloco_backup])
    bloco_backup = []

ram[0] = "100110110101"  # GET B5
ram[1] = "100110110110"  # GET B6
ram[2] = "000110110101"  # LDA B5
ram[3] = "001010110111"  # STR B7
ram[4] = "000110110110"  # LDA B6
ram[5] = "010010111000"  # Sub B8
ram[6] = "001010110110"  # STR B6
ram[7] = "000110110101"  # LDA B5
ram[8] = "001110110111"  # ADD B7
ram[9] = "001010110101"  # STR B5
ram[10] = "000110110110"  # LDA B6
ram[11] = "010010111000"  # Sub B8
ram[12] = "001010110110"  # STR B6
ram[13] = "010100001111"  # JZ 0F
ram[14] = "100000000111"  # JMP 07
ram[15] = "101010110101"  # PRT B5
ram[16] = "000000000000"  # HLT

ram[184] = "000000000001"  # B8


def cache(celula_ram):
    cache = end_cache(celula_ram)  # separa o endereço especificado em uma lista com 3 elementos, sendo eles a tag,
    # o subconjunto e a célula
    boole = False  # variavel booleana que será usada para definir se o endereç especificado se encontra na cache ou não
    tag = cache[0]  # coloca a tag em uma variável própria
    subconjunto = int(bintodec(cache[1]))  # coloca o subconjunto em uma variável própria
    celula = int(bintodec(cache[2]))  # transforma o número da célula em decimal e coloca em uma variável própria
    # print(subconjunto)
    for i in range(0, int(n_linha_cache / n_conj_cache)):  # verifica se o bloco se encontra na cache
        if memoria_cache_conj[subconjunto][i][
            0] == tag:  # se o bloco estiver na cache, o programa apenas fará a leitura
            # print("Endereço encontrado na memória cache!! Fazendo a leitura...")
            # print("Byte contido no endereço solicitado:" + memoria_cache_conj[subconjunto][i][celula + 1])
            # print("Na memória principal: " + str(ram[bintodec(celula_ram)]))
            boole = True
            linha = i
            break
    if boole == False:  # se o bloco não estiver na cache o programa irá no endereço especificado na ram e atualizará a linha
        # correspondente da cache
        # print("Endereço não encontrado na memória cache!! Procurando na memória principal...")
        linha = random.randint(0, int(n_linha_cache / n_conj_cache - 1))

        if bloco_backup_final[subconjunto][
            linha] != '3':  # se tiver sido atualizado, ele irá atualizar a memória ram com os
            # novos bytes do bloco
            # print("Celula atualizada enquanto na memoria cache, atualizando na memória principal...")
            for i in range(1, n_coluna_cache):
                ram[int(bintodec(bloco_backup_final[subconjunto][linha] + cache[1] + dectobin(i - 1, len(cache[2]))))] = \
                    memoria_cache_conj[subconjunto][linha][i]
                # print("funcionou")
            bloco_backup_final[subconjunto][linha] = '3'  # como o bloco já foi atualizado na memória ram, ele 'zera'
            # o valor correspondente àquela linha no bloco_backup_final

        memoria_cache_conj[subconjunto][linha][0] = tag  # atualiza a tag na devida linha
        for i in range(1, n_coluna_cache):  # itera por as todas colunas atualizando com o valor de todas as células
            # pertencentes a este bloco da ram
            # print(dectobin(i - 1, len(cache[2])))
            memoria_cache_conj[subconjunto][linha][i] = ram[
                int(bintodec(tag + cache[1] + dectobin(i - 1, len(cache[2]))))]

        # print("Bloco da memória cache atualizada! O byte contido no endereço correspondente é: " + str(memoria_cache_conj[subconjunto][linha][celula + 1]))
        # print("Na memória principal: " + str(ram[bintodec(celula_ram)]))
    return str(memoria_cache_conj[subconjunto][linha][celula + 1])


def cache_escrita(celula_ram, gravar):
    cache = end_cache(celula_ram)  # separa o endereço especificado em uma lista com 3 elementos, sendo eles a tag,
    # o subconjunto e a célula
    boole = False  # variavel booleana que será usada para definir se o endereç especificado se encontra na cache ou não
    tag = cache[0]  # coloca a tag em uma variável própria
    subconjunto = int(bintodec(cache[1]))  # coloca o subconjunto em uma variável própria
    celula = int(bintodec(cache[2]))  # transforma o número da célula em decimal e coloca em uma variável própria
    # print(subconjunto)
    for i in range(0, int(n_linha_cache / n_conj_cache)):  # verifica se o bloco se encontra na cache
        if memoria_cache_conj[subconjunto][i][
            0] == tag:  # se o bloco estiver na cache, o programa apenas fará a leitura
            # print("Endereço encontrado na memória cache!! Fazendo a leitura...")
            # print("Byte contido no endereço solicitado:" + memoria_cache_conj[subconjunto][i][celula + 1])
            # print("Na memória principal: " + str(ram[bintodec(celula_ram)]))
            boole = True
            linha = i
            break
    if boole == False:  # se o bloco não estiver na cache o programa irá no endereço especificado na ram e atualizará a linha
        # correspondente da cache
        # print("Endereço não encontrado na memória cache!! Procurando na memória principal...")
        linha = random.randint(0, int(n_linha_cache / n_conj_cache - 1))

        if bloco_backup_final[subconjunto][
            linha] != '3':  # se tiver sido atualizado, ele irá atualizar a memória ram com os
            # novos bytes do bloco
            # print("Celula atualizada enquanto na memoria cache, atualizando na memória principal...")
            for i in range(1, n_coluna_cache):
                ram[int(bintodec(bloco_backup_final[subconjunto][linha] + cache[1] + dectobin(i - 1, len(cache[2]))))] = \
                    memoria_cache_conj[subconjunto][linha][i]
                # print("funcionou")
            bloco_backup_final[subconjunto][linha] = '3'  # como o bloco já foi atualizado na memória ram, ele 'zera'
            # o valor correspondente àquela linha no bloco_backup_final

        memoria_cache_conj[subconjunto][linha][0] = tag  # atualiza a tag na devida linha
        for i in range(1, n_coluna_cache):  # itera por as todas colunas atualizando com o valor de todas as células
            # pertencentes a este bloco da ram
            # print(dectobin(i - 1, len(cache[2])))
            memoria_cache_conj[subconjunto][linha][i] = ram[
                int(bintodec(tag + cache[1] + dectobin(i - 1, len(cache[2]))))]

        # print("Bloco da memória cache atualizada! O byte contido no endereço correspondente é: " + str(memoria_cache_conj[subconjunto][linha][celula + 1]))
        # print("Na memória principal: " + str(ram[bintodec(celula_ram)]))

    memoria_cache_conj[subconjunto][linha][celula + 1] = dectobin(bintodec(gravar),
                                                                  12)  # sobrescreve o endereço especificado na memória cache
    bloco_backup_final[subconjunto][linha] = tag  # armazena o endereço do bloco que foi modificado

    return str(memoria_cache_conj[subconjunto][linha][celula + 1])


CI = "00000000"
R0 = "000000000000"
while True:
    REM = CI
    RDM = ram[bintodec(CI)]
    RI = RDM

    cOp = RI[0:4]
    Op = RI[4:12]

    if bintodec(cOp) == 0:  # HLT
        print("HLT")
        break

    elif bintodec(cOp) == 1:  # LDA Op
        print("LDA Op")
        REM = Op
        RDM = cache(REM)
        R0 = RDM

    elif bintodec(cOp) == 2:  # STR Op
        print("STR Op")
        cache_escrita(Op, R0)
        # print(cache(Op))

    elif bintodec(cOp) == 3:  # ADD Op
        print("ADD Op")
        REM = Op
        RDM = cache(Op)
        R0 = bintodec(R0)
        R0 += bintodec(RDM)
        R0 = dectobin(R0, 12)
        print("Soma: " + R0)

    elif bintodec(cOp) == 4:  # Sub Op
        print("Sub Op")
        REM = Op
        RDM = cache(Op)
        R0 = bintodec(R0)
        R0 = R0 - bintodec(RDM)
        R0 = dectobin(R0, 12)


    elif bintodec(cOp) == 5:  # JZ Op
        print("JZ Op")
        if bintodec(R0) == 0:
            CI = Op
            continue

    elif bintodec(cOp) == 6:  # JP Op
        print("JP Op")
        if bintodec(R0) > 0:
            CI = Op
            continue

    elif bintodec(cOp) == 7:  # JN Op
        print("JN Op")
        if bintodec(R0) < 0:
            CI = Op
            continue

    elif bintodec(cOp) == 8:  # JMP Op
        print("JMP Op")
        CI = Op
        continue

    elif bintodec(cOp) == 9:  # GET Op
        print("GET Op")
        get = dectobin(int(input("Entre com um número entre 0 e 4095: ")), 12)
        cache_escrita(Op, get)

    elif bintodec(cOp) == 10:  # PRT Op
        print("PRT Op")
        print(bintodec(cache(Op)))

    CI = dectobin(bintodec(CI) + 1, 8)
    print(bintodec(R0))
