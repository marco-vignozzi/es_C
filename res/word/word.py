# def jaccard1(ng_used, x, cmp_w):
#     ng_count = 0
#     for i in cmp_w.n_grams:
#         if i not in ng_used[cmp_w.word]:
#             ng_count += 1
#     for j in x.n_grams:
#         if j not in ng_used[cmp_w.word]:
#             ng_count += 1
#     ng_count += len(ng_used[cmp_w.word])
#     jac = len(ng_used[cmp_w.word]) / ng_count
#     return jac
#

def jaccard(cmp_w, x):          # calculate the jaccard
    intersection = []
    union = x.n_grams
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
        jac = jaccard(cmp_word, w)
        if jac >= j:
            j_dict[w] = (w, jac)              # if the jaccard value is greater it stores the word and the j value
    return j_dict
#
# def find_closest(ng_close_index, ng_used, word):
#     closest_word = ""
#     j_dict = {}
#     best_j = 0
#     for w in ng_close_index:
#         j = jaccard1(ng_used, word, w)
#         j_dict[w.word] = j
#         if j > best_j:
#             best_j = j
#             closest_word = w
#     return closest_word.word, best_j, ng_used[closest_word.word], ng_close_index[closest_word], ng_close_index, j_dict


class NGramIndex:
    def __init__(self, word_to_cmp, words_list, j_val=0.5):
        #self.n_gram_index = {}              # this dictionary associate to every n-gram-key any word that contains it
        #self.n_gram_schedule = {}           # this dictionary associate to every word-key its n-grams
        #self.close_j_words = []

        self.close_words = []           # this word-key dict associate the word and the jaccard value to the word-key
        self.words_list = words_list
        self.close_words = find_close_words(word_to_cmp, words_list, j_val)

        #for word in words_list:     # add to the words-key dict the n-grams of every word
        #    self.n_gram_schedule[word] = word.n_grams

        #for w in self.n_gram_schedule:
        #    for ng in self.n_gram_schedule[w]:
        #        if ng in self.n_gram_index:         # add to the n-grams-key dict any word that contains it
        #            self.n_gram_index[ng].append(w)
        #        else:
        #            self.n_gram_index[ng] = []
        #            self.n_gram_index[ng].append(w)
        #self.closest_data = self.get_closest_word(word_to_cmp)    # ritorna dati parola più vicina e parole più vicine
        #self.closest_word = self.closest_data[0]
        #close_j_words = self.find_j_words(self.closest_data[5], j_val)
        #self.close_j_words = self.inorder_j_words(close_j_words)

    # def inorder_j_words(self, wj_dict):
    #     close_words_list = []
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
    # def find_j_words(self, j_dict, j_val):    # crea lista di parole con j >= j_val
    #     close_words = {}
    #     for word in j_dict:
    #         if j_dict[word] >= j_val:
    #             close_words[word] = j_dict[word]
    #     return close_words
    #
    # def get_closest_word(self, word):
    #     n_gram_close_index = {}
    #     n_gram_used = {}
    #     for ng in word.n_grams:
    #         if ng in self.n_gram_index:
    #             for w in self.n_gram_index[ng]:
    #                 if w in n_gram_close_index and ng not in n_gram_used[w.word]:
    #                     n_gram_close_index[w] += 1
    #                     n_gram_used[w.word].append(ng)
    #                 elif w.word not in n_gram_used:
    #                     n_gram_close_index[w] = 0
    #                     n_gram_close_index[w] += 1
    #                     n_gram_used[w.word] = []
    #                     n_gram_used[w.word].append(ng)
    #     return find_closest(n_gram_close_index, n_gram_used, word)
    #

class Word:
    def __init__(self, word, ng_dim=3):
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
    w_list = [Word("pigna"), Word("pigno"), Word("pigneto"), Word("paracetamolo")]
    ng_idx = NGramIndex(Word("pigne"), w_list, 0)
    print(ng_idx.close_j_words)



if __name__ == "__main__":
    main()
