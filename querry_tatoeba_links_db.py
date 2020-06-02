"""
tatoeba_links.db was genarated using data from https://tatoeba.org/ published under various Creative Commons licenses
"""

import sqlite3


def querry(kanji):
    """
    This funtion will return a dictionary, containing requested kanji/kango examples with translations
    """
    with sqlite3.connect("tatoeba_links.db") as con:
        cur = con.cursor()
        cur.execute(
            'SELECT meaning_id, sentence FROM jpn_indices WHERE sentence LIKE "%' + kanji + '%";')

        jpn = [i for i in cur.fetchall()]
        eng_indices = ", ".join([f"'{i[0]}'" for i in jpn])
        res_dict = {
            num: sent for num, sent in jpn
        }

        q = 'SELECT sentence_id, sentence FROM eng_sentences WHERE sentence_id in (' + \
            eng_indices + ');'
        cur.execute(q)
        eng = cur.fetchall()
        jpn_eng_dict = dict()
        for sent in eng:
            jpn_eng_dict[res_dict[sent[0]]] = sent[1]
            #res_dict[sent[0]] = {res_dict[sent[0]]: sent[1]}

        return jpn_eng_dict
        # return list(res_dict.values())


if __name__ == "__main__":
    # Test call
    print(querry("すばらしい"))
