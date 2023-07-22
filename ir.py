import os
import numpy as np
import pandas as pd
import math
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from natsort import natsorted

stop_words = stopwords.words('english')
stop_words.remove('where')
stop_words.remove('in')
stop_words.remove('to')

files_name = natsorted(os.listdir('files'))
documents = []
for files in files_name:
    with open(f'files/{files}', 'r') as f:
        document = f.read()
    tokenized_documents = word_tokenize(document)
    terms = []
    for word in tokenized_documents:
        if word not in stop_words:
            terms.append(word)
    documents.append(terms)
    print(tokenized_documents)
document_number = 1
positional_index = {}

for document in documents:

    for positional, term in enumerate(document):

        if term in positional_index:

            positional_index[term][0] = positional_index[term][0] + 1

            if document_number in positional_index[term][1]:
                positional_index[term][1][document_number].append(positional)
            else:
                positional_index[term][1][document_number] = [positional]

        else:
            positional_index[term] = []
            positional_index[term].append(1)
            positional_index[term].append({})
            positional_index[term][1][document_number] = [positional]

    document_number = document_number + 1
print(positional_index)
query = 'antony brutus'

final_list = [[] for i in range(10)]

for word in query.split():
    for key in positional_index[word][1].keys():

        if final_list[key - 1] != []:
            if final_list[key - 1][-1] == positional_index[word][1][key][0] - 1:
                final_list[key - 1].append(positional_index[word][1][key][0])
        else:
            final_list[key - 1].append(positional_index[word][1][key][0])

for position, list in enumerate(final_list, start=1):

    if len(list) == len(query.split()):
        print(position)
all_words = []
for doc in documents:
    for word in doc:
        all_words.append(word)


def get_freq_term(d):
    words_found = dict.fromkeys(all_words, 0)
    for w in d:
        words_found[w] += 1
    return words_found


term_freq = pd.DataFrame(get_freq_term(documents[0]).values(), index=get_freq_term(documents[0]).keys())
for i in range(1, len(documents)):
    term_freq[i] = get_freq_term(documents[i]).values()

print(term_freq)


def get_wighted_term_freq(x):
    if x > 0:
        return math.log(x) + 1
    return 0


tfd = pd.DataFrame(columns=['freq', 'idf'])
for i in range(len(term_freq)):
    frequency = term_freq.iloc[i].values.sum()
    tfd.loc[i, 'freq'] = frequency
    tfd.loc[i, 'idf'] = math.log(10 / (float(frequency)))
tfd.index = term_freq.index
term_freq_inve_doc_freq = term_freq.multiply(tfd['idf'], axis=0)

print(term_freq_inve_doc_freq)

document_lengths = pd.DataFrame()


def get_doc_length(col):
    return np.sqrt(term_freq_inve_doc_freq[col].apply(lambda x: x ** 2).sum())


for column in term_freq_inve_doc_freq.columns:
    document_lengths.loc[0, f'{column}_len'] = get_doc_length(column)

print(document_lengths)

normalize_term_freq_idf = pd.DataFrame()


def get_normalized(col, x):
    try:
        return x / document_lengths[f'{col}_len'].values[0]
    except:
        return 0


for column in term_freq_inve_doc_freq.columns:
    normalize_term_freq_idf[column] = term_freq_inve_doc_freq[column].apply(lambda x: get_normalized(column, x))

print(normalize_term_freq_idf)
