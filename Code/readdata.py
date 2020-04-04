# encoding: UTF-8
import numpy as np
import re
import os
import pickle
import jieba

def save(content,path):
    '''
    把content用pickle方式存到path里
    '''
    f=open(path,'wb')
    pickle.dump(content,f)
    f.close()
    print("file has been saved")

def clean_str(string):
    '''
    接收string，返回去除各种符号的string
    '''
    string=re.sub("[^\u4e00-\u9fff]"," ",string)
    string = re.sub(r"\s{2,}", " ", string)
    return string

def split_str(string):
    '''
    接收string，返回各个词间用空格隔开的string
    '''
    return " ".join([word for word in jieba.cut(string,HMM=True)])

def get_cleaned_list(file_path):
    '''
    接收文件全路径，返回次txt文件的分词好的列表
    '''
    print("read txt now..............")
    f=open(file_path,'r',encoding="utf8")
    lines=list(f.readlines())
    lines=[clean_str(split_str(line)) for line in lines]
    f.close()
    print("read txt finished")
    return lines

def padding_sentences(no_padding_lists, padding_token='<PADDING>',padding_sentence_length = None):
    '''
    接收句子列表，将所有句子填充为一样长
    '''
    print("padding sentences now..............")
    all_sample_lists=[sentence.split(' ') for sentence in no_padding_lists]
    if padding_sentence_length != None:
        max_sentence_length=padding_sentence_length
    else:
        max_sentence_length=max([len(sentence) for sentence in all_sample_lists])
    for i,sentence in enumerate(all_sample_lists):
        if len(sentence) > max_sentence_length:
            all_sample_lists[i]=sentence[:max_sentence_length]
        else:
            sentence.extend([padding_token] * (max_sentence_length - len(sentence)))
    print("padding sentences finished")
    return (all_sample_lists,max_sentence_length)

def get_all_data_from_file(positive_file_path,negative_file_path,force_len=None):
    '''
    positive_file_path:正评价txt全路径
    negative_file_path:负评价txt全路径
    '''
    positive_sample_lists=get_cleaned_list(positive_file_path)
    negative_sample_lists=get_cleaned_list(negative_file_path)
    positive_label_lists=[[0,1] for _ in positive_sample_lists]
    negative_label_lists=[[1,0] for _ in negative_sample_lists]
    all_sample_lists = positive_sample_lists + negative_sample_lists #样本为list类型！！
    if force_len == None:
        all_sample_lists, max_sentences_length = padding_sentences(all_sample_lists)  #样本为list类型！！
    else:
        all_sample_lists, max_sentences_length = padding_sentences(all_sample_lists,padding_token='<PADDING>',padding_sentence_length = force_len)  # 样本为list类型！！
    all_label_arrays=np.concatenate([positive_label_lists,negative_label_lists], 0)  #标签为array类型
    return (all_sample_lists,all_label_arrays,max_sentences_length)

def batch_iter(data, batch_size, num_epochs, shuffle=False):
    '''
    生成batches迭代对象
    '''
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((data_size - 1) / batch_size) + 1
    for epoch in range(num_epochs):
        if shuffle:
            #顺序打乱
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_idx : end_idx]

def batch_iter_test(data, batch_size, num_epochs, shuffle=False):
    '''
    生成batches迭代对象
    '''
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((data_size - 1) / batch_size) + 1
    for epoch in range(num_epochs):
        if shuffle:
            #顺序打乱
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_idx = batch_num * batch_size
            end_idx = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_idx : end_idx]

def loadDict(train_data_path):
    f=open(train_data_path,'rb')
    params=pickle.load(f)