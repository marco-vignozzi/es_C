from res import test

word_to_compare = "frasconi"
compared_dict = "60000_parole_italiane"

test1 = test.Test("frasconi-60k-parole", word_to_compare, compared_dict, ng_dim=3, j_val=0.5, ed_dist=3)

test1.create_docs()
