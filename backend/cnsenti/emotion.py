import jieba
import pickle
import pathlib
import re

class Emotion(object):


    def __init__(self):
        self.Haos = self.read_dict('好.pkl')
        self.Les = self.read_dict('乐.pkl')
        self.Ais = self.read_dict('哀.pkl')
        self.Nus = self.read_dict('怒.pkl')
        self.Jus = self.read_dict('惧.pkl')
        self.Wus = self.read_dict('恶.pkl')
        self.Jings = self.read_dict('惊.pkl')

    def read_dict(self, file):
        pathchain = ['dictionary', 'dutir',file]
        mood_dict_filepath = pathlib.Path(__file__).parent.joinpath(*pathchain)
        dict_f = open(mood_dict_filepath, 'rb')
        words = pickle.load(dict_f)
        return words

    def emotion_count(self, text):

        wordnum, sentences, hao, le, ai, nu, ju, wu, jing =0, 0, 0, 0, 0, 0, 0, 0, 0
        sentences = len(re.split('[\.。！!？\?\n;；]+', text))
        words = jieba.lcut(text)
        wordnum = len(words)
        for w in words:
            if w in self.Haos:
                hao += 1
            elif w in self.Les:
                le += 1
            elif w in self.Ais:
                ai += 1
            elif w in self.Nus:
                nu += 1
            elif w in self.Jus:
                ju += 1
            elif w in self.Wus:
                wu += 1
            elif w in self.Jings:
                jing += 1
            else:
                pass
        result = {'words':wordnum, 'sentences':sentences, '好':hao, '乐':le, '哀':ai, '怒':nu, '惧':ju, '恶': wu, '惊':jing}
        return result



