from res import test

words_to_compare = ['metitapo', 'panin', 'carucola', 'paveta', 'peresso', 'falstidio', 'perola', 'cosato', 'fra', 'polemta', 'ferilo']
compared_dict = "60000_parole_italiane"

with open(f"res/words_lists/{compared_dict}.txt", encoding="utf8") as f:
    lines = f.readlines()
    f.close()

test1 = test.Test("2gram03", words_to_compare, compared_dict, ng_dim=2, j_val=0.3)
test2 = test.Test("2gram04", words_to_compare, compared_dict, ng_dim=2, j_val=0.4)
test3 = test.Test("3gram025", words_to_compare, compared_dict, ng_dim=3, j_val=0.25)
test4 = test.Test("3gram035", words_to_compare, compared_dict, ng_dim=3, j_val=0.35)

test1.create_docs()
test2.create_docs()
test3.create_docs()
test4.create_docs()