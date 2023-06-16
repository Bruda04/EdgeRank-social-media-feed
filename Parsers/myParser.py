def load_comments(path):
    output_data = []
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

            content = [data[0], data[1], data[2], comment_text, data[n - 10], data[n - 9], data[n - 8], data[n - 7],
                       data[n - 6], data[n - 5], data[n - 4], data[n - 3], data[n - 2], data[n - 1]]
            output_data.append(content)

            found_open_ellipsis = found_close_ellipsis = False
            comment = ""
    return output_data


def load_statuses(path):
    extracted_statuses = []
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
            extracted_statuses.append([data[0], comment_text, data[n-14], data[n-13], data[n-12], data[n-11],
                             data[n-10], data[n-9], data[n-8], data[n-7], data[n-6], data[n-5], data[n-4],
                             data[n-3], data[n-2], data[n-1]])
            comment = ""
            paired_ellipses = True

    return extracted_statuses



def get_statuses_header():
    return ",".join(['status_id', 'status_message', "link_name", "status_type", "status_link",
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


def load_shares(path):
    shares = []
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            shares.append(line.strip().split(","))
    return shares


def load_reactions(path):
    reactions = []
    with open(path) as file:
        lines = file.readlines()
        for line in lines[1:]:
            reactions.append(line.strip().split(","))
    return reactions