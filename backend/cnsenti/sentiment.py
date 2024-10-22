import jieba
import numpy as np
import pickle
import pathlib
import re


class Sentiment(object):

    def __init__(self, merge=True, pos=None, neg=None, encoding='utf-8'):

        self.Poss = self.load_dict('pos.pkl')
        self.Negs = self.load_dict('neg.pkl')

        if pos:
            if merge:
                del self.Poss
                self.Poss = self.load_diydict(file=pos, encoding=encoding)+self.load_dict('pos.pkl')
                jieba.load_userdict(pos)

            else:
                del self.Poss
                self.Poss = self.load_diydict(file=pos, encoding=encoding)
                jieba.load_userdict(pos)


        if neg:
            if merge:
                del self.Negs
                self.Negs = self.load_diydict(file=neg, encoding=encoding)+self.load_dict('neg.pkl')
                jieba.load_userdict(neg)
            else:
                del self.Negs
                self.Negs = self.load_diydict(file=neg, encoding=encoding)
                jieba.load_userdict(neg)

        self.Denys = self.load_dict('deny.pkl')

        self.Extremes = self.load_dict('extreme.pkl')
        self.Verys = self.load_dict('very.pkl')
        self.Mores = self.load_dict('more.pkl')
        self.Ishs = self.load_dict('ish.pkl')

    def load_dict(self, file):

        pathchain = ['dictionary', 'hownet',file]
        mood_dict_filepath = pathlib.Path(__file__).parent.joinpath(*pathchain)
        dict_f = open(mood_dict_filepath, 'rb')
        words = pickle.load(dict_f)
        return words

    def load_diydict(self, file, encoding):

        text = open(file, encoding=encoding).read()
        words = text.split('\n')
        words = [w for w in words if w]
        return words


    def sentiment_count(self, text):

        length, sentences, pos, neg = 0, 0, 0, 0
        sentences = [s for s in re.split('[\.。！!？\?\n;；]+', text) if s]
        sentences = len(sentences)
        words = jieba.lcut(text)
        length = len(words)
        for w in words:
            if w in self.Poss:
                pos+=1
            elif w in self.Negs:
                neg+=1
            else:
                pass
        return {'words': length,  'sentences':sentences, 'pos':pos, 'neg':neg}



    def judgeodd(self, num):

        if (num % 2) == 0:
            return 'even'
        else:
            return 'odd'

    def sentiment_calculate(self, text):

        sentences = [s for s in re.split('[\.。！!？\?\n;；]+', text) if s]
        wordnum = len(jieba.lcut(text))
        count1 = []
        count2 = []
        for sen in sentences:
            segtmp = jieba.lcut(sen)
            i = 0  # 记录扫描到的词的位置
            a = 0  # 记录情感词的位置
            poscount = 0  # 积极词的第一次分值
            poscount2 = 0  # 积极词反转后的分值
            poscount3 = 0  # 积极词的最后分值（包括叹号的分值）
            negcount = 0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in self.Poss:  # 判断词语是否是情感词
                    poscount += 1
                    c = 0
                    for w in segtmp[a:i]:  # 扫描情感词前的程度词
                        if w in self.Extremes:
                            poscount *= 4.0
                        elif w in self.Verys:
                            poscount *= 3.0
                        elif w in self.Mores:
                            poscount *= 2.0
                        elif w in self.Ishs:
                            poscount *= 0.5
                        elif w in self.Denys:
                            c += 1
                    if self.judgeodd(c) == 'odd':  # 扫描情感词前的否定词数
                        poscount *= -1.0
                        poscount2 += poscount
                        poscount = 0
                        poscount3 = poscount + poscount2 + poscount3
                        poscount2 = 0
                    else:
                        poscount3 = poscount + poscount2 + poscount3
                        poscount = 0
                    a = i + 1  # 情感词的位置变化

                elif word in self.Negs:  # 消极情感的分析，与上面一致
                    negcount += 1
                    d = 0
                    for w in segtmp[a:i]:
                        if w in self.Extremes:
                            negcount *= 4.0
                        elif w in self.Verys:
                            negcount *= 3.0
                        elif w in self.Mores:
                            negcount *= 2.0
                        elif w in self.Ishs:
                            negcount *= 0.5
                        elif w in self.Denys:
                            d += 1
                    if self.judgeodd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1
                elif word == '！' or word == '!':  ##判断句子是否有感叹号
                    for w2 in segtmp[::-1]:  # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                        if w2 in self.Poss or self.Negs:
                            poscount3 += 2
                            negcount3 += 2
                            break
                i += 1  # 扫描词位置前移

                # 以下是防止出现负数的情况
                pos_count = 0
                neg_count = 0
                if poscount3 < 0 and negcount3 > 0:
                    neg_count += negcount3 - poscount3
                    pos_count = 0
                elif negcount3 < 0 and poscount3 > 0:
                    pos_count = poscount3 - negcount3
                    neg_count = 0
                elif poscount3 < 0 and negcount3 < 0:
                    neg_count = -poscount3
                    pos_count = -negcount3
                else:
                    pos_count = poscount3
                    neg_count = negcount3

                count1.append([pos_count, neg_count])
            count2.append(count1)
            count1 = []

        pos_result = []
        neg_result = []
        for sentence in count2:
            score_array = np.array(sentence)
            pos = np.sum(score_array[:, 0])
            neg = np.sum(score_array[:, 1])
            pos_result.append(pos)
            neg_result.append(neg)

        pos_score = np.sum(np.array(pos_result))
        neg_score = np.sum(np.array(neg_result))
        score = {'sentences': len(count2),
                 'words':wordnum,
                 'pos': pos_score,
                 'neg': neg_score}

        return score







