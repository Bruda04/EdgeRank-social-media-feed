from weightCalculator.weightCalc import weightCalc
from timeDecay.calcTimeDecay import calcTimeDecay
from Trie.Trie import Trie
import textwrap
import os

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


def getRelevantneObjave(graph, ulogovan, statusi):
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

def edgeRankiraneObjave(graph, ulogovan, statuses):
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


    sorted_items = sorted(sumObjave.items(), key=lambda x: x[1], reverse=True)

    return [item[0] for item in sorted_items]

if __name__ == "__main__":
    from Parsers.myParser import load_serialize_graph, load_friends, load_statuses
    users = load_friends("dataset/friends.csv")
    statuses = load_statuses("./dataset/test_statuses.csv")


    ulogovan = login(users)

    graph = load_serialize_graph()
    tezineObjava = weightCalc(graph, ulogovan, statuses)
    vremeskaKomponentaObjava = calcTimeDecay(graph, ulogovan, statuses)
    objave = getRelevantneObjave(graph, ulogovan,statuses)
    rankedKeys = edgeRankiraneObjave(graph, ulogovan,statuses)

    close = False
    while not close:
        cls()
        print("1. Top 10 objava")
        print("2. Pretraga objava")
        print("3. Izlaz")

        validanUnos = False
        while not validanUnos:
            unos = int(input("Odaberite opciju: "))
            if unos == 3:
                validanUnos = True
                close = True
            elif unos == 1 or unos == 2:
                validanUnos = True

        cls()
        if unos == 1:
            for k in rankedKeys[:10]:
                prikaziObjavu(objave[k])
            input("Pritisnite ENTER za nazad")
        elif unos == 2:
            tries = []
            for objavljivac in statuses:
                for status in statuses[objavljivac]:
                    tries.append(Trie(status, statuses[objavljivac][status]["status_message"]))
            searchWord = input("Pretraga: ")
            print(searchWord in tries[0])
            input("Pritisnite ENTER za nazad")
