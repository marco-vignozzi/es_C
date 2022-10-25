from res.edit_distance import edit_distance
from res.word import word
from timeit import default_timer as timer


class Test:
    def __init__(self, t_name, word_to_cmp, cmp_dict, ng_dim=2, j_val=0.5, ed_dist=3, t_type="edit_charts"):

        self.name = t_name
        self.word_to_compare = word.Word(word_to_cmp, ng_dim)
        self.compared_dict = cmp_dict
        self.j = j_val
        self.ng_dim = ng_dim
        self.ed_dist = ed_dist

        with open(f"res/words_lists/{cmp_dict}.txt", encoding="utf8") as f:
            lines = f.readlines()
            f.close()

        self.ng_creation_time = 0
        self.words_list = []

        start = timer()
        [self.words_list.append(wordim).Word(line.strip(), ng_d) for line in lines]
        end = timer()

        self.ng_creation_time = end - start

        self.ed_time = 0
        self.ng_time = 0

        start = timer()
        self.n_grams = word.NGramIndex(self.word_to_compare, self.words_list, j_val)
        self.ng_closest = self.n_grams.closest_data
        end = timer()
        self.ng_time = end - start

        start = timer()
        self.ed_data = edit_distance.EditDistanceData(self.word_to_compare, self.words_list, ed_dist)
        self.ed_closest = self.ed_data.closest_word
        if self.ed_closest:
            self.ed_op_closest = list()
            self.ed_data.get_op_sequence(self.ed_op_closest, self.ed_data.ed_schedule[self.ed_closest[0]][1], len(word_to_cmp),
                                                              self.ed_data.ed_schedule[self.ed_closest[0]][2])
        end = timer()
        self.ed_time = end - start

        # print(self.n_grams.close_j_words)
        # print(self.edited_list.close_words_schedule)
        # print(self.n_grams.close_words_schedule)

    def create_docs(self):
        with open(f"docs/{self.name}.txt", "w") as f:
            f.write(f"Test per trovare la parola piu' vicina a '{self.word_to_compare.word}' nella lista '{self.compared_dict}':\n\n" +
                    f"- risultati con l'utilizzo di N-GRAM:\n"
                    f"  dimensione n-gram: {self.ng_dim}\n  parola piu' vicina trovata: {self.ng_closest[0]}\n  coefficiente di jaccard (J): {self.ng_closest[1]}\n" +
                    f"  n-grams corrispondenti: {self.ng_closest[2]}\n  tempo creazione n-grams: {self.ng_creation_time}\n"
                    f"  tempo ricerca parola: {self.ng_time}\n\n  lista parole trovate con coefficiente J >= {self.j}:\n {self.n_grams.close_j_words}\n\n")

            if self.ed_closest:
                f.write(f"- risultati con l'utilizzo di EDIT-DISTANCE:\n"
                        f"  distanza massima di editing considerata: {self.ed_dist}\n  parola piu' vicina trovata: {self.ed_closest[0]}\n" +
                        f"  lista operazioni: {self.ed_op_closest}\n" +
                        f"  distanza di editing dalla parola cercata: {self.ed_closest[1]}\n  tempo con edit distance: {self.ed_time}\n\n" +
                        f"  lista parole trovate con distanza di editing <= {self.ed_dist}:\n {self.ed_data.close_words}\n\n")
            else:
                f.write(f"- risultati con l'utilizzo di EDIT-DISTANCE:\n"
                        f"  distanza massima di editing considerata: {self.ed_dist}\n\n  ***NESSUNA PAROLA TROVATA CON QUESTA DISTANZA***"
                        f"  \n\n  tempo con edit distance: {self.ed_time}\n")
            f.close()


