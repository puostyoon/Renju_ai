import numpy as np
from config import params

def eval_one_line(line, player:str)->(int, dict):
    #go through a line(iteratable 1-d list or 1-d numpy array)
    line_length = len(line)
    length = -1
    pure_length = 0
    one_side_closed = True
    blank_exist = False
    len1, len2, len3, len4, len5 = 0, 0, 0, 0, 0
    len_num_list = [len1, len2, len3, len4, len5] # number of stones in a row: o, oo, ooo, oooo, oooo
    dict_for_legal_action_check = {"three without block": 0,
                                   "four": 0,
                                   "six in a row": False,
                                   "is win": False}
    if player == "black":
        for n, i in enumerate(line):
            # n is an index, i indicates an element of the line. i==0 : blank, i == 1: black stone, i == 2: white stone
            # length is length of current stones who are in a row.
            if i == 0:
                pure_length = 0
                if (length > 0 or (one_side_closed == True and length == 0)) and n+1 < line_length and line[n+1] == 1 and blank_exist == False:
                    blank_exist = True #blank exists in the stones in a row. ex> oo_oo
                elif length > 0 and n+1 < line_length and line[n+1] != 1:
                    idx = length - 1
                    if not blank_exist:
                        len_num_list[idx] += 1
                    else:
                        len_num_list[idx] += 0.5 # oo_o and ooo are different. ooo values higher than oo_o
                        blank_exist = False
                    length = 0
                else: # if two or more blank exists (o_o_o), stones don't considered to be in a row.
                    length = 0
                    one_side_closed = False
            elif i == 1 :
                length += 1
                pure_length += 1
                if pure_length == 5 and ((n+1 == line_length) or (n+1<line_length and line[n+1]!=1)):
                    len_num_list[4] += 1
                    dict_for_legal_action_check["is win"] = True
                    length = 0
                    blank_exist = False
                    one_side_closed = False
                elif (length == 5 or (length == 4 and one_side_closed)) and blank_exist:
                    len_num_list[2] += 1 #I think oo_ooo for black stone worth three stones in a row.
                    length = 0
                    blank_exist = False
                    one_side_closed = False
                elif pure_length >= 6: #six or more in a row without blank
                    dict_for_legal_action_check["six in a row"] = True
                    len_num_list[4] -= 1  # six in a row for black is not allowed.
                    length = 0
                    blank_exist = False
                    one_side_closed = False
            if i == 2 or (i==1 and n == line_length-1):
                pure_length = 0
                if length > 1:
                    if one_side_closed == False:
                        idx = (length - 1) - 1
                        if not blank_exist:
                            len_num_list[idx] += 1
                        else:
                            len_num_list[idx] += 0.5  # oo_o and ooo are different. ooo values higher than oo_o
                            blank_exist = False
                        length = 0
                    elif one_side_closed:
                        length = 0
                        one_side_closed = False
                elif length == 1:
                    length = 0
                if n!=0 and n+1<line_length and line[n+1] == 1:
                    length -= 1
                    one_side_closed = True
    #end
    else:  #player == "white", white player
        for n, i in enumerate(line):
            if i == 0:
                pure_length = 0
                if (length > 0 or (one_side_closed == True and length == 0)) and n+1 < line_length and line[n+1] == 2 and blank_exist == False:
                    blank_exist = True
                elif length > 0 and n + 1 < line_length and line[n + 1] != 2:
                    idx = length - 1
                    if not blank_exist:
                        len_num_list[idx] += 1
                    else:
                        len_num_list[idx] += 0.5  # oo_o and ooo are different. ooo values higher than oo_o
                        blank_exist = False
                    length = 0
                else:
                    length = 0
                    one_side_closed = False
            elif i == 2 :
                length += 1
                pure_length += 1
                if pure_length == 5:
                    len_num_list[4] += 1
                    dict_for_legal_action_check["is win"] = True
                    length = 0
                    blank_exist = False
                    one_side_closed = False
                elif (length == 5 or (length == 6 and one_side_closed)) and blank_exist:
                    len_num_list[3] += 1  # something like xoo_oooo or ooo_ooo worth 4 stones in a row
                    length = 0
                    blank_exist = False
                    one_side_closed = False
            if i == 1 or (i==2 and n == line_length-1):
                pure_length = 0
                if length > 1:
                    if one_side_closed == False:
                        idx = (length - 1) - 1
                        if not blank_exist:
                            len_num_list[idx] += 1
                        else:
                            len_num_list[idx] += 0.5  # oo_o and ooo are different. ooo values higher than oo_o
                            blank_exist = False
                        length = 0
                    elif one_side_closed:
                        length = 0
                        one_side_closed = False
                elif length == 1:
                    length = 0
                if n!=0 and n + 1 < line_length and line[n + 1] == 2:
                    length -= 1
                    one_side_closed = True
    #end
    alpha = params['alpha']
    total_score = 0
    for idx, num in enumerate(len_num_list):
        total_score += num*(alpha**idx)
    return total_score, dict_for_legal_action_check


    """
    _ : state 0, o : state 1, x : state 2,
    __ : state 3, _o: state 4,
    __o : state 5, _oo : state 6,
    __oo: state 7, _ooo : state 8,
    __ooo: state 9, _oooo : state 10
    __oooo: state 11
    """
    """
    state = 2
    pattern = ""
    pattern_end = False
    for i in line:
        character = '_' if i == 0 else 'o' if i == 1 else 'x'
        if character == 'x':
            pattern_end = True
        else:
            pattern += character
        if len(pattern)>=3 and pattern[-3:] == "___":
            pattern = pattern[:-1]
        if pattern == "_oo_":
            pass
        elif pattern == ""
    """