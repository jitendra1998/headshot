import numpy as np
from builtins import float
from gensim.models.word2vec import Word2Vec
import json
from sklearn.cluster import KMeans
import redis as rd


red = rd.StrictRedis('localhost',db=10)

class Sentence(object):

    def __init__(self):
        self.data = json.loads(red.get('questions').decode('utf-8'))
        self.limit = None

    def data_tokenizer(self):
        for key in self.data:
            line = self.data[key].split()
            self.data[key] = line
            yield line
        # return self.data

    def train_model(self):
        data = list(self.data_tokenizer())
        self.model = Word2Vec(data, size=100, min_count=0, workers=12,window=3, sample=1e-3, sg=0, hs=1,negative=5, iter=5)

    def map_score(self):
        self.score = dict()
        for key in self.data:
            if len(self.data[key])!=1:
                for word in range(len(self.data[key])):
                    if self.data[key][word] not in self.model.wv.vocab:
                        self.data[key][word] = np.zeros(100)
                    else:
                        self.data[key][word] = self.model[self.data[key][word]]

            self.score[key] = str(np.sum([abs(np.subtract(self.data[key][word],self.data[key][word+1])) for word in range(len(self.data[key])-2)]))
        red.set('scores', json.dumps(self.score))


    def score_categories_making(self):
        self.cat = json.loads(red.get('cat').decode('utf-8'))
        limits = {}
        for ele in self.cat:
            limits[ele] = self.keans_cluster(self.cat[ele])
        red.set('limits', json.dumps(limits))
        pass

    def keans_cluster(self, lis):
        self.score = json.loads(red.get('scores').decode('utf-8'))
        score = []
        mini = 99999999.0
        maxi = 0.0

        for ele in lis:
            k = []
            k.append((self.score[str(ele)]))
            if float(self.score[str(ele)]) < (mini):
                mini = float(self.score[str(ele)])
            elif float(self.score[str(ele)]) > maxi:
                maxi = float(self.score[str(ele)])
            score.append(k)
        kmeans = KMeans(n_clusters=4, random_state=0).fit(score)
        centers = (kmeans.cluster_centers_)
        a = []
        for key in centers:
            a.extend(key)
        a.sort()
        range = []
        range.append(mini)
        range.extend(a)
        range.append(maxi)
        return range
        pass

    def band_creation(self):
        master= {}
        cat = json.loads(red.get('cat').decode('utf-8'))
        limits = json.loads(red.get('limits').decode('utf-8'))
        score = json.loads(red.get('scores').decode('utf-8'))
        for ele in cat:
            master[ele] = {}
            for ele1 in limits:
                if ele == ele1:
                    for num in range(len(limits[ele1])-1):
                        master[ele][num] = []
                        for ids in cat[ele]:
                            if float(score[str(ids)]) > limits[ele1][num] and float(score[str(ids)]) < limits[ele1][num+1]:
                                master[ele][num].append(ids)
        red.set('master', json.dumps(master))


        pass

    def run(self):
        print('Training model')
        self.train_model()
        self.map_score()
        print('Score Cat Mapping')
        self.score_categories_making()
        self.band_creation()
        pass

if __name__=='__main__':
    corpus = Sentence()
    corpus.train_model()
    corpus.map_score()
    corpus.score_categories_making()
    corpus.band_creation()