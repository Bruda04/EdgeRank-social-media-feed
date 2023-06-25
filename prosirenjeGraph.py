if __name__ == "__main__": 
    from Parsers.myParser import load_comments, load_friends, load_reactions, load_shares, load_statuses, save_serialize_graph, load_serialize_graph
    from networkx import DiGraph
    from time import time, gmtime, strftime
    from datetime import datetime

    startg = start = time()

    users = load_friends("testProsireno/friends.csv")
    statuses = load_statuses("testProsireno/test_statuses.csv")
    shares = load_shares("testProsireno/test_shares.csv")
    comments = load_comments("testProsireno/test_comments.csv")
    reactions = load_reactions("testProsireno/test_reactions.csv")

    stop = time()

    print("Gotovo parstiranje fajlova: " + strftime("%M:%S", gmtime(stop-start)))

    consts = {
        "isFriend": 100,
        "shares": 1.7,
        "comments": 1.5,
        "loves": 1.5,
        "wows": 1.4,
        "hahas": 1.3,
        "likes": 1.1,
        "sads": 0.95,
        "angrys": 0.8,
        "timeDecay": 0.94
    }

    start = time()

    graph = load_serialize_graph()
    lu = str(len(users))
    i = 0
    for posmatraniKorisnik in users.keys():
        i += 1
        for drugiKorisnik in users.keys():
            if posmatraniKorisnik == drugiKorisnik:
                continue
            
            imaAfinitet = False

            drugiImaStatus = drugiKorisnik in statuses
            if drugiImaStatus:
                statusiDrugogKorisnika = statuses[drugiKorisnik]

            if graph.has_edge(posmatraniKorisnik, drugiKorisnik):
                affinity = graph[posmatraniKorisnik][drugiKorisnik]["weight"]
            else: 
                affinity = 1

            if drugiKorisnik in users[posmatraniKorisnik]["friends"]:
                affinity *= consts["isFriend"]
                imaAfinitet = True
            
            posmatraniImaReactions = posmatraniKorisnik in reactions
            if posmatraniImaReactions and drugiImaStatus:
                for reaction in reactions[posmatraniKorisnik].keys():
                    if reaction in statusiDrugogKorisnika:
                        tmpReaction = reactions[posmatraniKorisnik][reaction]
                        
                        tmpAffinity = 1
                        if tmpReaction["type_of_reaction"] == "loves":
                            tmpAffinity = consts["loves"]
                        elif tmpReaction["type_of_reaction"] == "wows":
                            tmpAffinity = consts["wows"]
                        elif tmpReaction["type_of_reaction"] == "hahas":
                            tmpAffinity = consts["hahas"]
                        elif tmpReaction["type_of_reaction"] == "likes":
                            tmpAffinity = consts["likes"]
                        elif tmpReaction["type_of_reaction"] == "sads":
                            tmpAffinity = consts["sads"]
                        elif tmpReaction["type_of_reaction"] == "angrys":
                            tmpAffinity = consts["angrys"]

                        tDelta = (datetime.now() - datetime.strptime(tmpReaction["reacted"], "%Y-%m-%d %H:%M:%S")).days // 10


                        affinity *= tmpAffinity * (consts["timeDecay"]**tDelta)
                        imaAfinitet = True


            posmatraniImaShares = posmatraniKorisnik in shares
            if posmatraniImaShares and drugiImaStatus:
                for share in  shares[posmatraniKorisnik].keys():
                    if share in statusiDrugogKorisnika:
                        tDelta = (datetime.now() - datetime.strptime(shares[posmatraniKorisnik][share]["status_shared"], "%Y-%m-%d %H:%M:%S")).days // 10
                        affinity *= consts["shares"] * (consts["timeDecay"]**tDelta)
                        imaAfinitet = True


            posmatrainiImaComments = posmatraniKorisnik in comments
            if posmatrainiImaComments and drugiImaStatus:
                for comment in comments[posmatraniKorisnik].keys():
                    if comment in statusiDrugogKorisnika:
                        tDelta = (datetime.now() - datetime.strptime(comments[posmatraniKorisnik][comment]["comment_published"], "%Y-%m-%d %H:%M:%S")).days // 10
                        affinity *= consts["comments"] * (consts["timeDecay"]**tDelta)
                        imaAfinitet = True


            if imaAfinitet:
                if graph.has_edge(posmatraniKorisnik, drugiKorisnik):
                    graph[posmatraniKorisnik][drugiKorisnik]["weight"] = affinity
                else:
                    graph.add_edge(posmatraniKorisnik, drugiKorisnik, weight=affinity)

        print(str(i) + "/" + lu)
    
    stop = time()

    print("Gotvo kreiranje grafa: " + strftime("%M:%S", gmtime(stop-start)))

    print(graph)

    start = time()

    save_serialize_graph(graph)

    stop = time()

    print("Gotova serijalizacija grafa: " + strftime("%M:%S", gmtime(stop-start)))

    start = time()

    graphLoad = load_serialize_graph()

    stopg = stop = time()

    print("Gotovo učitavanje grafa: " + strftime("%M:%S", gmtime(stop-start)))

    print(graphLoad)

    print("Gotovo sve: " + strftime("%M:%S", gmtime(stopg-startg)))
