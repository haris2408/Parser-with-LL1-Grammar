import copy
import csv


def compute_ll1_parse_table(first_set, follow_set, grammar, terminals):
    arr = []
    print("terminals")
    print(terminals)
    for i in range(len(list(first_set.keys())) + 1):
        arr.append([])
        for j in range(len(terminals) + 1):
            arr[i].append("__")
    terminals.remove('~')
    terminals_index = dict()
    for i, terminal in zip(range(1, (len(arr[0]) - 1)), terminals):
        terminals_index[terminal] = i
        arr[0][i] = terminal
    arr[0][(len(arr[0]) - 1)] = "$"
    terminals_index["$"] = len(arr[0]) - 1
    print("terminals_index")
    print(terminals_index)
    non_terminal_index = dict()
    for i, non_terminal in zip(range(0, len(first_set.keys())), first_set.keys()):
        non_terminal_index[non_terminal] = i + 1
        arr[i + 1][0] = non_terminal
    print("non_terminal_index")
    print(non_terminal_index)
    print(arr)
    prod_no = 1
    prods = dict()
    for key in grammar.keys():
        for i in range(len(grammar[key])):
            si = 0
            if grammar[key][i][si].isupper():
                # print("i" + str(i))
                # print("si" + str(si))
                # print("terminator" + str(non_terminal_index[key]))
                # print("no keyy not" + str((grammar[key][i][si])))
                # print("keyy" + str(key))
                # print("terminator" + str(terminals_index[(grammar[key][i][si])]))
                for x in first_set[grammar[key][i][si]]:
                    if x == "~":
                        for y in follow_set[key]:
                            arr[non_terminal_index[key]][terminals_index[y]] = prod_no
                    else:
                        arr[non_terminal_index[key]][terminals_index[x]] = prod_no
            elif grammar[key][i][si] == '~':
                for y in follow_set[key]:
                    arr[non_terminal_index[key]][terminals_index[y]] = prod_no
            else:
                arr[non_terminal_index[key]][terminals_index[(grammar[key][i][si])]] = prod_no
            prods[prod_no] = grammar[key][i]
            if "~" in prods[prod_no]:
                prods[prod_no].remove("~")
            prod_no += 1

    for i in arr:
        for j in i:
            print(j, end="")
        print()
    return arr, prods, terminals_index, non_terminal_index


def compute_followset(s, grammar, first_set, follow_set_helper):
    follow_set = set()
    if s == list(grammar.keys())[0]:
        follow_set.add("$")
    for key in grammar.keys():
        for i in range(len(grammar[key])):

            if s in grammar[key][i]:

                si = grammar[key][i].index(s)
                # if s == "Z":
                #     print("here")
                #     print("this is smthn")
                #     print(si)
                #     print(s)
                #     print(key)
                if si < len(grammar[key][i]) - 1:
                    si += 1
                    while si < len(grammar[key][i]):
                        try:
                            if not grammar[key][i][si].isupper():
                                follow_set.add(grammar[key][i][si])
                                follow_set_helper[s] = follow_set
                                break
                            else:
                                # follow_set_new = compute_firstset(grammar[key][i][si], grammar)
                                follow_set_new = first_set[grammar[key][i][si]]
                                if '~' not in follow_set_new:
                                    for a in follow_set_new:
                                        follow_set.add(a)
                                    follow_set_helper[s] = follow_set
                                    break
                                elif '~' in follow_set_new and si < len(grammar[key][i]) - 1:
                                    follow_set_new.remove("~")
                                    for a in follow_set_new:
                                        follow_set.add(a)
                                    follow_set_helper[s] = follow_set

                                elif '~' in follow_set_new and si == len(grammar[key][i]) - 1:
                                    follow_set_new.remove("~")
                                    for a in follow_set_new:
                                        follow_set.add(a)
                                    follow_set_helper[s] = follow_set
                                    if key in follow_set_helper.keys():
                                        follow_set_new = follow_set_helper[key]
                                    else:
                                        follow_set_new = compute_followset(key, grammar, first_set, follow_set_helper)
                                    for a in follow_set_new:
                                        follow_set.add(a)
                                    follow_set_helper[s] = follow_set
                        except IndexError:
                            pass
                            # print("ERORRR")
                            # print(key)
                            # print(i)
                            # print(s)
                            # print(si)
                        si += 1
                else:
                    if grammar[key][i][si] == key:
                        break
                    else:
                        # print('hello')
                        if key in follow_set_helper.keys():
                            follow_set_new = follow_set_helper[key]
                        else:
                            follow_set_helper[key] = compute_followset(key, grammar, first_set, follow_set_helper)
                            follow_set_new = follow_set_helper[key]
                        for a in follow_set_new:
                            follow_set.add(a)

    return follow_set


def compute_firstset(s, grammar):
    first_set_ans = set()
    for i in range(len(grammar[s])):
        for j in range(len(grammar[s][i])):
            charac = grammar[s][i][j]
            if charac.isalpha() and charac.isupper():
                first_set_of_non_terminal = compute_firstset(charac, grammar)
                if '~' not in first_set_of_non_terminal:
                    for a in first_set_of_non_terminal:
                        first_set_ans.add(a)
                    break
                else:
                    if j < len(grammar[s][i]):
                        first_set_of_non_terminal.remove('~')
                        for a in first_set_of_non_terminal:
                            first_set_ans.add(a)
                    else:
                        for a in first_set_of_non_terminal:
                            first_set_ans.add(a)
            else:
                first_set_ans.add(charac)
                break

    # print(first_set_ans)
    return first_set_ans


def get_grammar(filename):
    non_terminals = set()
    file = open(filename, "r")
    lines = file.readlines()
    print("grammar")
    grammar = {}

    for line in lines:
        nexti = 0
        line_splitted = line.split()
        # print(line_splitted)
        # grammar.append(line_splitted)
        if line_splitted[0] not in grammar.keys():
            grammar[line_splitted[0]] = []
        else:
            nexti = len(grammar[line_splitted[0]])
        grammar[line_splitted[0]].append([])
        for i in range(1, len(line_splitted)):
            if not line_splitted[i].isupper():
                non_terminals.add(line_splitted[i])
            grammar[line_splitted[0]][nexti].append(line_splitted[i])
    return grammar, non_terminals


def top_down_parser(parse_table, prods, terminals_index, non_terminal_index, tokken_filename):
    input_stream = []
    with open(tokken_filename) as f:
        input_stream = f.readlines()
        for i in range(len(input_stream)):
            input_stream[i] = input_stream[i].replace("\n", "")
    input_stream.append("$")
    print(input_stream)
    stack = ["$"]
    stack.append(parse_table[1][0])
    # print(stack)
    look_ahead_i = 0
    while look_ahead_i < len(input_stream):
        if "InvalidToken" in input_stream[look_ahead_i]:
            look_ahead_i += 1
        if input_stream[look_ahead_i] == "$" and not stack[-1].isupper() and stack[-1] != "$":
            print("Input cannot be parsed")
            break
        if stack[-1].isupper():
            non_term = stack.pop()
            prod_no = parse_table[non_terminal_index[non_term]][terminals_index[input_stream[look_ahead_i]]]
            if prod_no != '__':
                for i in range(len(prods[prod_no]) - 1, -1, -1):
                    stack.append(prods[prod_no][i])
        else:
            if stack[-1] == input_stream[look_ahead_i]:
                if stack[-1] == "$" and input_stream[look_ahead_i] == "$":
                    break
                stack.pop()
                look_ahead_i += 1
            else:
                print(f"{stack[-1]} is missing")
                while look_ahead_i < len(input_stream):
                    look_ahead_i += 1
                    if look_ahead_i == len(input_stream) or input_stream[look_ahead_i] == "$":
                        print("Input cannot be parsed")
                        return
                    if stack[-1] == input_stream[look_ahead_i]:
                        stack.pop()
                        look_ahead_i += 1
                        break
        print("----------------------------------------------------")
        print("input stream")
        print(input_stream[look_ahead_i:])
        print("Stack")
        print(stack)
        print("----------------------------------------------------")
    print("input parsed")


if __name__ == '__main__':
    grammar, non_terminals = get_grammar("4bgrammar.txt")
    for key in grammar.keys():
        print(key, grammar[key])

    print("--------------------")
    print("first_set")
    first_set = {}
    for s in grammar.keys():
        first_set[s] = compute_firstset(s, grammar)
    for key in first_set.keys():
        print(key, first_set[key])
    with open("first.txt", "w") as firstfile:
        for key in first_set.keys():
            a = key
            for b in first_set[key]:
                a += (" " + b)
            a += "\n"
            firstfile.write(a)
    print("--------------------")
    print("follow_set")
    follow_set = {}
    for s in grammar.keys():
        follow_set[s] = compute_followset(s, grammar, first_set, follow_set)
    for key in follow_set.keys():
        print(key, follow_set[key])

    with open("follow.txt", "w") as followfile:
        for key in follow_set.keys():
            a = key
            for b in follow_set[key]:
                a += (" " + b)
            a += "\n"
            followfile.write(a)
    first_set_copy = copy.copy(first_set)
    follow_set_copy = copy.copy(follow_set)
    ll1_parse_table, prods, terminals_index, non_terminal_index = compute_ll1_parse_table(first_set_copy,
                                                                                          follow_set_copy, grammar,
                                                                                          non_terminals)
    # for prod in prods.keys():
    #     print(str(prod) + ": ")
    #     print(prods[prod])

    with open("SPL-Parsing.csv", "w") as parsetable_file:
        for item in ll1_parse_table:
            for i in range(len(item)):

                if i == 0:
                    if item[i] == "__":
                        parsetable_file.write(" ")
                    else:
                        parsetable_file.write(str(item[i]))
                else:
                    if item[i] == "__":
                        parsetable_file.write(',' + " ")
                    else:
                        parsetable_file.write(',' + str(item[i]))
            parsetable_file.write('\n')

    top_down_parser(ll1_parse_table, prods, terminals_index, non_terminal_index, "input1.txt")
