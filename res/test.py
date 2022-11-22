from res.edit_distance import edit_distance
from res.word import word
from timeit import default_timer as timer


class Test:
    def __init__(self, t_name, words_to_cmp, cmp_dict, ng_dim=2, j_val=0.5, t_type="edit_charts"):

        self.name = t_name
        self.compared_dict = cmp_dict
        self.j = j_val
        self.ng_dim = ng_dim

        with open(f"res/words_lists/{cmp_dict}.txt", encoding="utf8") as f:
            lines = f.readlines()
            f.close()

        self.ng_creation_time = 0           # time spent to enumerate the n-grams for all the words
        self.words_list = []                # vocabulary used for comparison, it stores Words
        self.words_to_compare = []          # list of words to compare
        self.ed_words_list = []             # vocabulary used for edit distance only, it stores Strings

        [self.ed_words_list.append(line.strip()) for line in lines]

        # enumerating n-grams for all the words
        start = timer()
        [self.words_to_compare.append(word.Word(words_to_cmp[x].strip(), ng_dim)) for x in range(0, len(words_to_cmp))]
        [self.words_list.append(word.Word(line.strip(), ng_dim)) for line in lines]
        end = timer()

        self.ng_creation_time = round(end - start, 5)

        self.close_words = {}
        # this word-compared-key dict associates to any compared word the list of words in the vocabulary with greater
        # jaccard as a tuple (word, j)
        self.ordered_j_words = {}
        # this word-compared-key dict stores the (word, j) tuples of the close_words dict ordered by j for every
        # compared word
        self.ng_finding_time = {}
        # word-compared-key dict that stores the times needed for finding the words in the vocabulary with a greater
        # jaccard value for each word compared

        for w in self.words_to_compare:
            start = timer()
            ng_data = word.NGramIndex(w, self.words_list, j_val)
            self.close_words[w] = ng_data.close_words
            end = timer()
            self.ng_finding_time[w] = round(end - start, 7)
            self.ordered_j_words[w] = ng_data.inorder_j_words(self.close_words[w])

        self.ed_time = {}
        # word-compared-key dict that stores the times needed for finding the closest words with edit-distance
        self.ed_data = {}
        # word-compared-key dict that stores the edit-distance data for every word

        for w in self.words_to_compare:
            start = timer()
            self.ed_data[w] = edit_distance.EditDistanceData(w.word, self.close_words[w])
            end = timer()
            self.ed_time[w] = round(end - start, 5)

        self.ed_only_data = {}
        # word-compared-key dict that stores data of edit-distance between the compared word with the whole words list
        self.ed_only_time = {}
        # word-compared-key dict that stores the times needed for finding the closest word with edit-distance only

        for w in self.words_to_compare:
            start = timer()
            self.ed_only_data[w] = edit_distance.EditDistanceData(w.word, self.ed_words_list)
            end = timer()
            self.ed_only_time[w] = round(end - start, 5)

        # start = timer()
        # self.ed_data = edit_distance.EditDistanceData(self.word_to_compare, self.words_list, ed_dist)
        # self.ed_closest = self.ed_data.closest_word
        # if self.ed_closest:
        #     self.ed_op_closest = list()
        #     self.ed_data.get_op_sequence(self.ed_op_closest, self.ed_data.ed_schedule[self.ed_closest[0]][1], len(words_to_cmp),
        #                                  self.ed_data.ed_schedule[self.ed_closest[0]][2])
        # end = timer()
        # self.ed_time = end - start

        # print(self.n_grams.close_j_words)
        # print(self.edited_list.close_words_schedule)
        # print(self.n_grams.close_words_schedule)

    def create_docs(self):
        with open(f"docs/{self.name}.txt", "w") as f:
            for w in self.words_to_compare:
                f.write(f"Test per trovare la parola piu' vicina a '{w.word}' nella lista '{self.compared_dict}' "
                        f"utilizzando l'algoritmo di edit-distance con indici di {self.ng_dim}-grams e coefficiente di jaccard J={self.j}:\n\n" +
                        f"- tempo creazione indici di {self.ng_dim}-grams: {self.ng_creation_time}\n" +
                        f"- tempo ricerca parole vicine: {self.ng_finding_time[w]}\n" +
                        f"- tempo algoritmo edit-distance + {self.ng_dim}-grams: {self.ed_time[w]}\n" +
                        f"- tempo totale utilizzo edit-distance + {self.ng_dim}-grams con J={self.j}: " +
                        f"{round(self.ng_creation_time + self.ng_finding_time[w] + self.ed_time[w], 5)}\n" +
                        f"- trovate parole con J>{self.j}: {self.ordered_j_words[w]}\n" +
                        f"- trovate parole piu' vicine con edit-distance = {self.ed_data[w].cost} e lista operazioni di conversione:\n")
                for sw in self.ed_data[w].closest_words:
                    f.write(f"{self.ed_data[w].closest_words[sw][0]}\t" +
                            f"- operazioni per conversione '{w.word} -> {self.ed_data[w].closest_words[sw][0]}':\n "
                            f"\t\t\t{self.ed_data[w].closest_op_seq[sw]}\n")
                f.write(f"\n- tempo utilizzando solo edit-distance: {self.ed_only_time[w]}" +
                        f"\n- trovate parole piu' vicine con edit-distance = {self.ed_only_data[w].cost} e lista operazioni di conversione:\n")
                for sw in self.ed_only_data[w].closest_words:
                    f.write(f"{self.ed_only_data[w].closest_words[sw][0]}\t" +
                            f"- operazioni per conversione '{w.word} -> {self.ed_only_data[w].closest_words[sw][0]}':\n "
                            f"\t\t\t{self.ed_only_data[w].closest_op_seq[sw]}\n")
                f.write("\n\n\n")
        f.close()
