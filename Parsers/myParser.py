import pickle
from networkx import DiGraph

def load_comments(path):
    output_data = {}
    with open(path) as file:
        lines = file.readlines()
        comment = ""
        found_open_ellipsis = False
        found_close_ellipsis = False

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                comment += line

            if line[-1] == "\n":
                line = line[:-1]

            first_index = line.index("\"") if "\"" in line else -1
            if first_index > -1:
                found_open_ellipsis = True

            next_index = line.index("\"", first_index + 1) if "\"" in line[first_index + 1:] else -1
            if next_index > -1:
                found_close_ellipsis = True

            if found_open_ellipsis and not found_close_ellipsis:
                comment += line
                continue
            else:
                comment = line

            data = comment.split(",")
            n = len(data)

            if n < 14:
                raise Exception("Comment does not contain necessary data.")
            elif n > 14:
                comment_text = "".join(data[3:n - 10])
            else:
                comment_text = data[3]

#comment_id,status_id,parent_id,comment_message,comment_author,comment_published,num_reactions,num_likes,num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special
            content = {"comment_id": data[0],
                       "status_id": data[1],
                        "parent_id": data[2],
                        "comment_message": comment_text,
                        "comment_author": data[n - 10],
                        "comment_published": data[n - 9],
                        "num_reactions": data[n - 8],
                        "num_likes": data[n - 7],
                        "num_loves": data[n - 6],
                        "num_wows": data[n - 5],
                        "num_hahas": data[n - 4],
                        "num_sads": data[n - 3],
                        "num_angrys": data[n - 2],
                        "num_special": data[n - 1]}
            
            if data[4] not in output_data:
                output_data[data[4]] = {data[0] : content}
            else: 
                output_data[data[4]][data[0]] = content

            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
    return output_data


def load_statuses(path):
    extracted_statuses = {}
    with open(path) as file:
        lines = file.readlines()
        comment = ""
        paired_ellipses = True

        for index in range(1, len(lines)):

            line = lines[index]

            if line == "\n":
                comment += line
                continue

            # if line[-1] == "\n":
            #     line = line[:-1]
            line = line.strip()

            previous_index = -1

            while True:
                index = line.index("\"", previous_index+1) if "\"" in line[previous_index+1:] else -1
                if index == -1:
                    break
                paired_ellipses = not paired_ellipses
                previous_index = index

            comment += line
            if not paired_ellipses:
                continue

            data = comment.split(",")
            n = len(data)

            if n < 16:
                raise Exception("Status does not contain necessary data.")
            elif n > 16:
                comment_text = "".join(data[1:n-14])
            else:
                comment_text = data[1]

#status_id,status_message,link_name,status_type,status_link,status_published,author,num_reactions,num_comments,num_shares,num_likes,num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special
            content = {"status_id": data[0],
                       "status_message": comment_text,
                       "status_type": data[n-14],
                       "status_link": data[n-13],
                       "status_published": data[n-12],
                       "author": data[n-11],
                       "num_reactions": data[n-10],
                       "num_comments": data[n-9],
                       "num_shares": data[n-8],
                       "num_likes": data[n-7],
                       "num_loves": data[n-6],
                       "num_wows": data[n-5],
                       "num_hahas": data[n-4],
                       "num_sads": data[n-3],
                       "num_angrys": data[n-2],
                       "num_special": data[n-1]}
            
            if data[n-11] not in extracted_statuses:
                extracted_statuses[data[n-11]] = {data[0] : content}
            else:
                extracted_statuses[data[n-11]][data[0]] = content
            comment = ""
            paired_ellipses = True

    return extracted_statuses

def load_shares(path):
    shares = {}
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            share = {"status_id" : data[0], "sharer": data[1], "status_shared" : data[2]}
            if data[1] not in shares:
                shares[data[1]] = {data[0]: share}
            else:
                shares[data[1]][data[0]] = share
    return shares


def load_reactions(path):
    reactions = {}
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            reaction = {"status_id": data[0], "type_of_reaction": data[1], "reactor": data[2], "reacted": data[3]}
            if data[2] not in reactions:
                reactions[data[2]] = {data[0]: reaction}
            else:
                reactions[data[2]][data[0]] = reaction
    return reactions

def load_friends(path):
    users = {}
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            data = line.strip().split(",")
            friends = data[2: 2+int(data[1])]
            user = {"person": data[0], "number_of_friends": data[1], "friends": friends}
            users[data[0]] = user
            
    return users

def get_statuses_header():
    return ",".join(['status_id', 'status_message', "status_type", "status_link",
                             "status_published", "author" "num_reactions", "num_comments", "num_shares",
                             "num_likes", "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys",
                             "num_special"])

def get_reaction_header():
    return "status_id,type_of_reaction,reactor,reacted"


def get_share_header():
    return "status_id,sharer,status_shared"


def get_comment_header():
    return "comment_id,status_id,parent_id,comment_message,comment_author,comment_published,num_reactions,num_likes," \
           "num_loves,num_wows,num_hahas,num_sads,num_angrys,num_special"

def get_friends_header():
    return "person,number_of_friends,friends"


def save_serialize_graph(data):
    with open("save.pickle", "wb") as pickleFile:
        pickle.dump(data, pickleFile)

def load_serialize_graph() -> DiGraph:
    with open("save.pickle", "rb") as pickleFile:
        data = pickle.load(pickleFile)
        return data

if __name__ == "__main__":
    pass