import math
import numpy as np
from res.word import word


class EditDistanceData:

    def __init__(self, query_word, words_list):     # words_list must be a list of strings!

        self.rows = len(query_word.word)
        self.compared_word = query_word     # word to compare with all the others
        self.ed_schedule = {}           # word-compared-key dict with all the info about the edit-distance
        self.costs_list = {}            # word-compared-key dict with the cost of the edit-distance
        self.words_length = {}          # word-compared-key dict with the length of the word compared

        for w in words_list:
            self.ed_schedule[w] = self.get_ed_schedule(query_word.word, w)
            self.costs_list[w] = self.ed_schedule[w][1]
            self.words_length[w] = self.ed_schedule[w][3]
        # any element in the ed_schedule dict contains a tuple with the following data about edit-distance:
        # {word: (word, edit-cost, op-table, word-length)}

        self.cost = math.inf        # it stores the best cost at the end of the for loop
        self.tmp_words = []         # it temporarily stores the closest words in a list until the next check
        self.closest_words = {}    # dict word-key that associates info from the ed-schedule about the most near word(s)
        for w in words_list:         # search the closest word(s)
            if self.costs_list[w] <= self.cost:
                self.cost = self.costs_list[w]
                self.tmp_words.append(w)
        for w in self.tmp_words:
            if self.costs_list[w] == self.cost:
                self.closest_words[w] = self.ed_schedule[w]     # stores data of the closest word
        self.closest_op_seq = {}       # stores the operations to convert the closest word to the query word
        if self.closest_words:
            for w in self.closest_words:
                self.closest_op_seq[w] = list()
                self.get_op_sequence(self.closest_op_seq[w], self.closest_words[w][2], self.rows, self.closest_words[w][3])

        # self.close_words = self.get_close_words(words_list, d_value)       # salvo le parole più vicine del valore dato (d_value)
        # cost = math.inf
        # self.closest_word = ()
        # for w in self.close_words:         # trovo la parola più vicina
        #     if self.close_words[w] < cost:
        #         cost = self.close_words[w]
        #         self.closest_word = w, cost

    def get_ed_schedule(self, x_str, y_str):
        x_str = " " + x_str
        y_str = " " + y_str
        m = len(x_str)
        n = len(y_str)
        c = np.empty([m, n], dtype=object)
        op = np.empty([m, n], dtype=object)
        c[0, 0] = 0
        for i in range(1, m):
            c[i, 0] = i
            op[i, 0] = f"delete {x_str[i]}"
        for j in range(1, n):
            c[0, j] = j
            op[0, j] = f"insert {y_str[j]}"

        for i in range(1, m):
            for j in range(1, n):
                c[i, j] = math.inf
                if x_str[i] == y_str[j]:
                    c[i, j] = c[i - 1, j - 1]
                    op[i, j] = f"copy {y_str[j]}"
                if (x_str[i] != y_str[j]) and (c[i - 1, j - 1] + 1 < c[i, j]):
                    c[i, j] = c[i - 1, j - 1] + 1
                    op[i, j] = f"replace {x_str[i]} with {y_str[j]}"
                if (i >= 2) and (j >= 2) and (x_str[i] == y_str[j - 1]) and (x_str[i - 1] == y_str[j]) \
                        and (c[i - 2, j - 2] + 1 < c[i, j]):
                    c[i, j] = c[i - 2, j - 2] + 1
                    op[i, j] = f"swap {y_str[j - 1]} <-> {y_str[j]}"
                if c[i - 1, j] + 1 < c[i, j]:
                    c[i, j] = c[i - 1, j] + 1
                    op[i, j] = f"delete {x_str[i]}"
                if c[i, j - 1] + 1 < c[i, j]:
                    c[i, j] = c[i, j - 1] + 1
                    op[i, j] = f"insert {y_str[j]}"
        bundled_word = (y_str, c[m - 1][n - 1], op, n - 1)
        return bundled_word        # it returns a tuple with compared word, edit cost, operations table and word length

    def get_op_sequence(self, op_list, op_table, m, n):
        if m == 0 and n == 0:
            return
        if ("copy" in op_table[m, n]) or ("replace" in op_table[m, n]):
            i = m-1
            j = n-1
        elif "swap" in op_table[m, n]:
            i = m-2
            j = n-2
        elif "delete" in op_table[m, n]:
            i = m-1
            j = n
        else:
            i = m
            j = n-1
        self.get_op_sequence(op_list, op_table, i, j)
        self.create_op_list(op_list, op_table[m, n])

    def create_op_list(self, op_list, operation):
        op_list.append(operation)


def main():
    # word = "OOTO OOTO of the OOTO"
    # new = "OOTO of the OOTO"
    # costs, op = edit_distance(word, new)
    # op_sequence(op, len(word), len(new))
    # value = costs[len(word), len(new)]
    # print(value)
    d = {"b": 3, "a": 4}
    print(d)


if __name__ == "__main__":
    main()
