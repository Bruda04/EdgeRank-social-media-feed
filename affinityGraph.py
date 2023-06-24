if __name__ == "__main__": 
    from .Parsers.myParser import load_comments, load_friends, load_reactions, load_shares, load_statuses, save_serialize_graph, load_serialize_graph
    from networkx import DiGraph
    from time import time, gmtime, strftime
    from datetime import datetime

    startg = start = time()

    users = load_friends("dataset/friends.csv")
    statuses = load_statuses("dataset/original_statuses.csv")
    shares = load_shares("dataset/original_shares.csv")
    comments = load_comments("dataset/original_comments.csv")
    reactions = load_reactions("dataset/original_reactions.csv")

    stop = time()

    print("Gotovo parstiranje fajlova: " + strftime("%M:%S", gmtime(stop-start)))

    consts = {
        "isFriend": 100,
        "shares": 8,
        "comments": 7,
        "loves": 7,
        "wows": 6,
        "hahas": 2,
        "likes": 1,
        "sads": 0.95,
        "angrys": 0.8,
        "timeDecay": 0.94
    }

    start = time()

    graph = DiGraph()
    lu = str(len(users))
    i = 0
    for posmatraniKorisnik in users.keys():
        i += 1
        for drugiKorisnik in users.keys():
            if posmatraniKorisnik == drugiKorisnik:
                continue

            drugiImaStatus = drugiKorisnik in statuses
            if drugiImaStatus:
                statusiDrugogKorisnika = statuses[drugiKorisnik]

            affinity = 1

            if drugiKorisnik in users[posmatraniKorisnik]["friends"]:
                affinity *= consts["isFriend"]
            
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

            posmatraniImaShares = posmatraniKorisnik in shares
            if posmatraniImaShares and drugiImaStatus:
                for share in  shares[posmatraniKorisnik].keys():
                    if share in statusiDrugogKorisnika:
                        tDelta = (datetime.now() - datetime.strptime(shares[posmatraniKorisnik][share]["status_shared"], "%Y-%m-%d %H:%M:%S")).days // 10
                        affinity *= consts["shares"] * (consts["timeDecay"]**tDelta)

            posmatrainiImaComments = posmatraniKorisnik in comments
            if posmatrainiImaComments and drugiImaStatus:
                for comment in comments[posmatraniKorisnik].keys():
                    if comment in statusiDrugogKorisnika:
                        tDelta = (datetime.now() - datetime.strptime(comments[posmatraniKorisnik][comment]["comment_published"], "%Y-%m-%d %H:%M:%S")).days // 10
                        affinity *= consts["comments"] * (consts["timeDecay"]**tDelta)

            if affinity != 1:
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
