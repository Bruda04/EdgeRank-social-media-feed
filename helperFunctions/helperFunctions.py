from weightCalculator.weightCalc import weightCalc
from timeDecay.calcTimeDecay import calcTimeDecay
from Trie.Trie import Trie
import textwrap
import os
import re

def cls():
    if os.name == 'posix':  # Unix/Linux/MacOS
        os.system('clear')
    elif os.name == 'nt':  # Windows
        os.system('cls')
    else:
        print('\n' * 100)

def login(users):
    validanUnos = False
    while not validanUnos:
        unos = input("Login as: ").strip()
        if unos not in users.keys():
            print("Nepostojeci korisnik pokusajte ponovo!")
        else:
            return unos


def getRelevantneObjave(graph, ulogovan, statuses):
    relevantniStatusi = {}

    for relacija in graph.neighbors(ulogovan):
        if not relacija in statuses:
            continue
        for objava in statuses[relacija]:
            relevantniStatusi[objava] = statuses[relacija][objava]
    
    return relevantniStatusi

def prikaziObjavu(objava):
    autor = objava["author"]
    datumVreme = objava["status_published"]
    status = objava["status_message"]
    lajkova = objava["num_likes"]
    srca = objava["num_loves"]
    vau = objava["num_wows"]
    smejanja = objava["num_hahas"]
    tuzica = objava["num_sads"]
    ljuto = objava["num_angrys"]
    deljenja = objava["num_shares"]
    komentara = objava["num_comments"]

    print()
    print(f"##### {autor} ##### {datumVreme} {'#'*(66 - len(autor) - len(datumVreme))}")
    print()
    print(textwrap.fill(status, width=60))
    print()
    print(f"  👍: {lajkova}  ❤️: {srca}  😯: {vau}  🤣: {smejanja}  😭: {tuzica}  😠: {ljuto}")
    print(f"  💬: {komentara}  🔀: {deljenja}")
    print("#"*80)
    print()


def edgeRank(graph, ulogovan, statuses, tezineObjava, vremeskaKomponentaObjava):
    sumObjave = {}

    for relacija in graph.neighbors(ulogovan):
        if not relacija in statuses:
            continue
        for objava in statuses[relacija]:
            tmpObjava = statuses[relacija][objava]

            a = graph.get_edge_data(ulogovan, tmpObjava["author"])["weight"]

            w = tezineObjava[objava]

            t = vremeskaKomponentaObjava[objava]

            sumObjave[objava] = a * w * t

    return sumObjave

def edgeRankiraneObjave(sumObjave):
    sortedItems = sorted(sumObjave.items(), key=lambda x: x[1], reverse=True)

    return [item[0] for item in sortedItems]

def makeTries(statuses):
    tries = {} #postId: Trie
    
    for objavljivac in statuses:
        for status in statuses[objavljivac]:
            tries[status] = Trie(status, objavljivac, statuses[objavljivac][status]["status_message"])
    
    return tries

def search(text, tries, ranks):
    listaReci = re.findall(r"[\w@#'*]+", text)

    nadjeno = {} #(autor, postId): {rec1: puta, rec2: puta ...}
    
    for trie in tries:
        tmpTrie = tries[trie]
        tmpInnerDict = {} 
        for rec in listaReci:
            if "*" not in rec:
                tmpInnerDict[rec] = tmpTrie.occurrences(rec)
            else:
                tmpInnerDict[rec] = tmpTrie.flexSearchOccurrances(rec)

        for rec in tmpInnerDict:
            if tmpInnerDict[rec] > 0:
                nadjeno[(tmpTrie.objavljivac, tmpTrie.statusId)] = tmpInnerDict

    def sorterFunc(tuple):
        dict = tuple[1]
        brojTrazenihReci = len(dict.values()) 
        brojNadjenihReci = 0
        ukupanBrojNadjenihReci = 0
        for rec in dict:
            if dict[rec] > 0:
                brojNadjenihReci += 1
                ukupanBrojNadjenihReci += dict[rec]

        #    1       2       3

        #    7       0       8  |  15   2    srednji   (2/3)^20*15

        #    1       1       1  |   3   3    najveci   root(4, 3/3)

        #    0       0       1  |   1   1    najmanji  

        rank = 0.0001
        if tuple[0][1] in ranks:
            rank = ranks[tuple[0][1]]*0.5
        
        return ((brojNadjenihReci/brojTrazenihReci)**20) * ukupanBrojNadjenihReci * rank


    sortedItems = sorted(nadjeno.items(), key=sorterFunc, reverse=True)

    return [key for (key , value) in sortedItems]


def prosiriStatuse(statuses, testStatuses): 
    ret = statuses

    for autor in testStatuses:
        if autor in ret:
            for postId in testStatuses[autor]:
                if postId not in ret[autor]:
                    ret[autor][postId] = testStatuses[autor][postId]
        else:
            ret[autor] = testStatuses[autor]

    return ret



if __name__ == "__main__":
    pass