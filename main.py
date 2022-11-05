from res import test

words_to_compare = [' mugolo']
compared_dict = "60000_parole_italiane"

with open(f"res/words_lists/{compared_dict}.txt", encoding="utf8") as f:
    lines = f.readlines()
    f.close()

test1 = test.Test("panino-try", words_to_compare, compared_dict, ng_dim=2, j_val=0.5)

test1.create_docs()
