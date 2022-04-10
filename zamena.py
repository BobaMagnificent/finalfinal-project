import gensim
import logging
import urllib.request
import pandas as pd
from nltk import sent_tokenize, word_tokenize


from pymorphy2 import MorphAnalyzer

with open('Борис.txt', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('\n', ' ')
t= sent_tokenize(text)


def word_changer(sentence):
    m = 'ruscorpora_mean_hs.model.bin' #этот файл нужно скачивать отдельно(он слишком большой для репозитория)
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True, )
    morph = MorphAnalyzer()
    s = [w.lower() for w in word_tokenize(sentence)]
    for i in range(len(s)):
        a = morph.parse(s[i])[0]
        value_dict = {}
        value_dict[i] = [a.tag.POS, a.tag.tense, a.tag.case, a.tag.number, a.tag.gender]
        try:
            if value_dict[i][0] == 'NOUN':
                similar = model.most_similar(a.normal_form + '_S')[0][0]
                similar = similar.split('_')[0]
                s[i] = morph.parse(similar)[0].inflect({value_dict[i][2], value_dict[i][3]}).word
        except Exception:
            continue
    s = ' '.join(s)
    s = s.replace(' ,', ',').replace(' .', '.').replace(' !', '!').replace(' ?', '?')
    return s


df = pd.DataFrame()
df['stolbec'] = t

df1 = df.head(350)


df2 = df.tail(351)
df2 = df2['stolbec'].apply(word_changer).to_frame()


df1['stolbec'].to_csv(r"./orig.txt", index=True, sep=",")
df2['stolbec'].to_csv(r"./izm.txt", index=True, sep=",")

#я убрал цифры в начале каждой строки с помощью регулярно выражения ([0-9]+)?\,