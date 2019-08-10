#! /usr/bin/env python3
import os
import itertools
import math
import pickle
import hashlib
from scipy import stats
from operator import itemgetter
from urllib.parse import urlparse
import matplotlib.pyplot as plt

def find_files(file_list):

    temp_list = []
    word_list = ['Trump']
    files_selected = []
    files_desired = 10
    collected_files = 0
    total_file_with_word = 0

    for each in file_list:
        with open('response_boiler/'+each,'r') as f:
            temp_list = f.read().split()
            temp_list = remove_stop_words(temp_list)
            if temp_list.count(word_list[0]) > 0:
                total_file_with_word += 1
                if collected_files < 10:
                    word_count = temp_list.count(word_list[0])
                    files_selected.append([each,word_count,len(temp_list)])
                    collected_files += 1

    return files_selected, len(file_list), total_file_with_word

def remove_stop_words(word_list):

    for i in range(len(word_list)):
        if len(word_list[i]) < 4:
            word_list[i] = '9'

    for i in range(word_list.count('9')):
        word_list.remove('9')

    return word_list

def calc_TF(word_count, total_word_count):
    return word_count / total_word_count

def calc_IDF(corpus_count, docs_with_term):
    return math.log2(corpus_count / docs_with_term)

def calc_TFIDF(TF_score, IDF_score):
    return TF_score * IDF_score

def calc_Tau_T1_T2(tfidf_scores, rank_scores):

    for i in range(len(rank_scores)):
        rank_scores[i] = float(rank_scores[i])
    tau,p_value = stats.kendalltau(tfidf_scores,rank_scores)
    print('Tau score: ', tau)
    print('p-value: ', p_value)

def gen_table(files, file_corpus, total_files_with_word, uri_lookup_dict):

    columns = ("TFIDF","TF","IDF","URI")
    Table_text = []
    TFIDF_values = []
    for each in files:
        TF_score = round(calc_TF(each[1], each[2]),3)
        IDF_score = round(calc_IDF(file_corpus, total_files_with_word),3)
        TFIDF_score = round(calc_TFIDF(TF_score, IDF_score),3)
        TFIDF_values.append(TFIDF_score)
        uri = urlparse(uri_lookup_dict[each[0]])
        #print(uri.netloc)
        Table_text.append([str(TFIDF_score), str(TF_score), str(IDF_score), uri.netloc])
    Table_text = sorted(Table_text,key=itemgetter(0), reverse=True)
    fig,ax = plt.subplots()

    fig.patch.set_visible(False)

    ax.axis('off')
    plt.title('TFIDF Rank by Word "Trump"')

    Table = ax.table(cellText=Table_text,colLabels = columns, loc='center')
    plt.savefig('TFIDF_table.png')
    
    return TFIDF_values

def gen_table_page_rank(files, uri_lookup_dict):

    columns = ("PageRank","URI")
    Table_text = []
    page_rank = [str(6/10),str(5/10),str(3/10),str(10/10),str(8/10),str(8/10),str(8/10),str(8/10),str(8/10),str(7/10)]
    for i in range(10):
        uri = urlparse(uri_lookup_dict[files[i][0]])
        Table_text.append([page_rank[i], uri.netloc])
    Table_text = sorted(Table_text,key=itemgetter(0), reverse=True)
    fig,ax = plt.subplots()

    fig.patch.set_visible(False)

    ax.axis('off')
    plt.title('Page Rank for Domains')
    Table = ax.table(cellText=Table_text,colLabels = columns, loc='center')

    plt.savefig('page_rank_table.png')

    return page_rank

def validate_matching_files():

    root, dirs, html_count = os.walk('response_html').__next__()
    root1, dirs1, boiler_count = os.walk('response_boiler').__next__()

    for each in html_count:
        boiler_match = each.split('_')
        if boiler_match[0] + '_boiler' not in boiler_count:
            os.system(f'rm response_html/{each}')

    return boiler_count

def gen_dict_uri(file):
    uri_dict = {}
    with open(file,'rb') as f:
        temp_list = pickle.load(f)

    for each in temp_list:
        temp_key = hashlib.md5(each.encode('utf-8')).hexdigest() + '_boiler'

        temp_value = each
        uri_dict[temp_key] = temp_value

    return uri_dict

def main():

    lookup_dict = gen_dict_uri('links.txt')
    boiler_files = validate_matching_files()
    files, file_count, files_with_word = find_files(boiler_files)
    TFIDF_values = gen_table(files, file_count, files_with_word, lookup_dict)
    page_rank = gen_table_page_rank(files, lookup_dict)
    calc_Tau_T1_T2(TFIDF_values, page_rank)

main()
