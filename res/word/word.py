def jaccard(cmp_w, x):          # calculate the jaccard coefficient
    intersection = []
    union = []
    [union.append(x.n_grams[i]) for i in range(len(x.n_grams))]
    for i in cmp_w.n_grams:
        if i in x.n_grams and i not in intersection:
            intersection.append(i)
        if i not in union:
            union.append(i)
    jac = len(intersection) / len(union)
    return jac


def find_close_words(cmp_word, words_list, j):
    j_dict = {}                              # word-key dict which contains any word of the list with greater jaccard
    for w in words_list:
        jac = round(jaccard(cmp_word, w), 3)
        if jac >= j:
            j_dict[w.word] = (w.word, jac)    # if the jaccard value is greater it stores the word (as a string) and the j value
    return j_dict


class NGramIndex:
    def __init__(self, word_to_cmp, words_list, j_val=0.5):

        self.close_words = {}           # this word-key dict associate the word and the jaccard value to the word-key
        self.ordered_j_words = []       # list of tuple (word, j) ordered by j
        self.words_list = words_list
        self.close_words = find_close_words(word_to_cmp, words_list, j_val)
        # self.ordered_j_words = self.inorder_j_words(self.close_words)

    def inorder_j_words(self, close_words):
        tmp_dict = {}
        for w in close_words:
            tmp_dict[w] = close_words[w]
        ordered_list = []
        while tmp_dict:
            best_j = 0
            best_w = ""
            for w in tmp_dict:
                if tmp_dict[w][1] > best_j:
                    best_w = tmp_dict[w][0]
                    best_j = tmp_dict[w][1]
            ordered_list.append(tmp_dict[best_w])
            del tmp_dict[best_w]
        return ordered_list

    # def inorder_j_words(self, close_words):
    #     close_words_list =

    #     while wj_dict:
    #         best_j = 0
    #         best_w = ""
    #         for cmp_w in wj_dict:
    #             if wj_dict[cmp_w] > best_j:
    #                 best_w = cmp_w
    #                 best_j = wj_dict[cmp_w]
    #         close_words_list.append((best_w, best_j))
    #         if best_w:
    #             del wj_dict[best_w]
    #         else:
    #             return []
    #     return close_words_list
    #

class Word:
    def __init__(self, word, ng_dim=2):
        self.word = word
        self.n_grams = self.n_gram_builder(self.word, ng_dim)

    def n_gram_builder(self, str_word, n):
        n_gram_list = []
        for x in range(-1, len(str_word) - n + 2):
            if x == -1:
                n_gram_list.append("_" + str_word[x + 1: x + n])
            elif x == len(str_word) - n + 1:
                n_gram_list.append(str_word[x: x + n - 1] + "_")
            else:
                n_gram_list.append(str_word[x: x + n])
        return n_gram_list


def main():
    w_list = [Word("pign"), Word("pigna"), Word("pigno"), Word("pigneto"), Word("paracetamolo")]
    ng_idx = NGramIndex(Word("pigne"), w_list, 0.5)
    print(ng_idx.close_words)
    ordered_words = ng_idx.inorder_j_words(ng_idx.close_words)
    print(ordered_words)
    # print(Word("pigne").n_grams)
    # print(Word("pigna").n_grams)
    # print(Word("pigno").n_grams)
    # print(Word("pigneto").n_grams)
    # print(Word("paracetamolo").n_grams)


if __name__ == "__main__":
    main()
