import bz2
import os
import pickle

# location of this file is required to load resource urls
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


# some Wikipedia articles
def dewiki_sample():
    graph_path = os.path.join(__location__, 'resources', 'dewiki_sample.pickle.bz2')
    with bz2.open(graph_path, 'rb') as file:
        return pickle.load(file)
