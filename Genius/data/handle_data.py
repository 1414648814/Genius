# from pymongo import MongoClient
# from pandas import DataFrame, Series
# from Genius.settings import SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT, SINGLE_MONGODB_DB
# from numpy.random import randn
#
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
#
# # class Graph(object):
# #     def __init__(self):
# #         self.client = MongoClient(SINGLE_MONGODB_SERVER, SINGLE_MONGODB_PORT)
# #         self.db = self.client[SINGLE_MONGODB_DB]
# #
# #     def getData(self):
# #         cursor = self.db['users'].find({'name':'王磊'})
# #         dataframe = DataFrame(list(cursor))
# #         print(dataframe)
# #
# # graph = Graph()
# # graph.getData()
#
# fig = plt.figure()
# ax1 = fig.add_subplot(2, 2, 1)
# fig.show()
# fig.suptitle('halle')
#
# #
# # plt.plot(randn(50).cumsum(), 'k--')