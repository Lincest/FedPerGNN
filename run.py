#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from utils import *
from encrypt import *
from model import *
from preprocess import *
from expansion import *
from generator import *
from const import *
import numpy as np
import random
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
path_dataset = 'training_test_dataset.mat'


# In[ ]:


def train(model):
    for rounds in range(EPOCH): # 每一轮
        alluserembs = userembedding_layer.get_weights()[0]
        # 消息传递的过程 
        user_neighbor_emb = graph_embedding_expansion(
            Otraining, usernei, alluserembs)
        # 生成小批量 (多个batch)
        traingen = generate_batch_data_random(
            BATCH_SIZE, train_user_index, trainu, traini, usernei, trainlabel, user_neighbor_emb)
        cnt = 0
        batchloss = []
        for i in traingen:
            layer_weights = model.get_weights()
            loss = model.train_on_batch(i[0], i[1])
            batchloss.append(loss)
            now_weights = model.get_weights()

            sigma = np.std(now_weights[0]-layer_weights[0]) # 训练前后参数的标准差
            # noise of pseudo interacted items (伪交互采样)
            norm = np.random.normal(
                0, sigma/np.sqrt(PSEUDO*BATCH_SIZE/now_weights[0].shape[0]), size=now_weights[0].shape)
            now_weights[0] += norm  
            itemembedding_layer.set_weights([now_weights[0]])
            print(np.mean(batchloss))
            # ldp noise (local differential privacy, 局部差分隐私)
            for i in range(len(now_weights)):
                now_weights[i] += np.random.laplace(0, LR*2*CLIP/np.sqrt(
                    BATCH_SIZE)/EPS, size=now_weights[i].shape)
            model.set_weights(now_weights)
            cnt += 1
            if cnt % 10 == 0:
                print(cnt, loss)
            if cnt == len(train_user_index)//BATCH_SIZE:
                break
    return user_neighbor_emb


def test(model, user_neighbor_emb):
    # 生成测试数据
    testgen = generate_batch_data(
        BATCH_SIZE, testu, testi, usernei, testlabel, user_neighbor_emb)
    cr = model.predict_generator(testgen, steps=len(
        testlabel)//BATCH_SIZE+1, verbose=1)
    print('rmse:', np.sqrt(
        np.mean(np.square(cr.flatten()-testlabel/LABEL_SCALE)))*LABEL_SCALE)


# In[ ]:
if __name__ == "__main__":

    # load data 加载数据
    M = load_matlab_file(path_dataset, 'M')
    Otraining = load_matlab_file(path_dataset, 'Otraining')  # 训练集
    Otest = load_matlab_file(path_dataset, 'Otest')  # 测试聚
    print('There are %i interactions logs.' %
          np.sum(np.array(np.array(M, dtype='bool'), dtype='int32')))  # 打印交互信息

    # preprocess data 预处理
    usernei = generate_history(Otraining)  # user neiborhood
    trainu, traini, trainlabel, train_user_index = generate_training_data(
        Otraining, M)  # trainu: user, traini: item
    testu, testi, testlabel = generate_test_data(Otest, M)

    # generate public&private keys
    generate_key()

    # build model
    model, userembedding_layer, itemembedding_layer = get_model(
        Otraining)  # model, user 嵌入, item 嵌入

    # train
    user_neighbor_emb = train(model)

    # test
    test(model, user_neighbor_emb)
