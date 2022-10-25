import math
import numpy as np
from res.word import word


class EditDistanceData:
    def __init__(self, query_word, words_list, d_value=3):

        self.rows = len(query_word.word)
        self.compared_word = query_word
        self.ed_schedule = {}
        self.costs_list = {}
        self.words_length = {}
        for w in words_list:
            self.ed_schedule[w.word] = self.get_ed_schedule(query_word.word, w.word)
            self.costs_list[w.word] = self.ed_schedule[w.word][0]
            self.words_length[w.word] = self.ed_schedule[w.word][2]
        # crea un dizionario di parole di cui si è calcolato l'edit distance con la query_word, a cui associamo informazioni sull'editing
        # è implementata con un dizionario di tuple: {word: (edit-cost, op-table, word-length)}

        self.close_words = self.get_close_words(words_list, d_value)       # salvo le parole più vicine del valore dato (d_value)
        cost = math.inf
        self.closest_word = ()
        for w in self.close_words:         # trovo la parola più vicina
            if self.close_words[w] < cost:
                cost = self.close_words[w]
                self.closest_word = w, cost

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
        bundled_word = (c[m - 1][n - 1], op, n - 1)
        return bundled_word        # ritorna una tupla con costo di editing, tabella delle operazioni e lunghezza parola

    def get_op_sequence(self, op_list, op_table, m, n):
        if m == 0 and n == 0:
            return
        if ("copy" in op_table[m, n]) or ("replace" in op_table[m, n]):
            i = m-1
            j = n-1
        elif "twiddle" in op_table[m, n]:
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

    def op_scheduler(self, schedule):
        op_schedule = []
        for w in schedule:
            op_list = []
            self.get_op_sequence(op_list, schedule[w][1], self.rows, schedule[w][2])
            op_schedule.append(tuple(op_list))
        return op_schedule

    def get_close_words(self, w_list, v):
        close_words = {}
        for w in w_list:
            if self.costs_list[w.word] <= v:
                close_words[w.word] = self.costs_list[w.word]
        return close_words




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
