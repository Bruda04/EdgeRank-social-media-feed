if __name__ == "__main__":
    from Parsers.myParser import load_serialize_graph, load_friends, load_statuses, load_serialize_tries, save_serialize_tries
    from helperFunctions.helperFunctions import *
    

    users = load_friends("dataset/friends.csv")
    ulogovan = login(users)

    print("Loading...")
    statuses = load_statuses("./dataset/original_statuses.csv")
    tries = load_serialize_tries()
    graph = load_serialize_graph()
    
    # testStatuses = load_statuses("./testProsireno/test_statuses.csv") # Linije za prosirenje Grapha
    # statuses = prosiriStatuse(statuses, testStatuses)
    # tries = makeTries(statuses)

    tezineObjava = weightCalc(graph, ulogovan, statuses)
    vremeskaKomponentaObjava = calcTimeDecay(graph, ulogovan, statuses)
    objave = getRelevantneObjave(graph, ulogovan,statuses)
    rankiraneObjave = edgeRank(graph, ulogovan, statuses, tezineObjava, vremeskaKomponentaObjava)
    rankedKeys = edgeRankiraneObjave(rankiraneObjave)

    close = False
    while not close:
        cls()
        print("1. Top 10 objava")
        print("2. Pretraga objava")
        print("3. Izlaz")

        validanUnos = False
        while not validanUnos:
            unos = input("Odaberite opciju: ")
            if not unos.isnumeric():
                continue
            unos = int(unos)
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
            searchWord = input("Pretraga: ").lower().strip()
            
            rezultetPretrage = search(searchWord, tries, rankiraneObjave)

            for k in rezultetPretrage[:10]:
                prikaziObjavu(statuses[k[0]][k[1]])
            
            input("Pritisnite ENTER za nazad")
