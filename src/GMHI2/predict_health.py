import pandas as pd
from joblib import load
import numpy as np
from . import utils
import os

def get_clean_matrix():
    df = pd.read_csv("abundance.txt", sep="\t", index_col=0).T
    df = df.reset_index(drop=True)
    df = df.rename_axis(None, axis = 1)


    clf = load(os.path.join(utils.DEFAULT_DB_FOLDER, "logreg.joblib"))
    names = [name[3:] for name in clf.feature_names_in_]

    set_diff = set(names) - set(df.columns)

    blank = pd.DataFrame(np.zeros((1, len(set_diff))), columns=set_diff, )
    concat = pd.concat([blank, df], axis=1)
    reindexed = concat[names]
    scaled = reindexed / reindexed.sum().sum()
    return scaled

def preprocess(cleaned):
    minmax = load(os.path.join(utils.DEFAULT_DB_FOLDER, "minmax.joblib"))
    c = 0.00001
    transformed = minmax.transform(np.log(cleaned + c))
    return transformed

def get_score():
    cleaned = get_clean_matrix()
    preprocessed = preprocess(cleaned)
    clf = load(os.path.join(utils.DEFAULT_DB_FOLDER, "logreg.joblib"))
    gmhi_score = clf.decision_function(preprocessed)
    return gmhi_score