import pandas as pd
from GMHI import GMHI
import warnings
from joblib import load
import numpy as np
from . import utils
import os

def get_clean_matrix():
    df = pd.read_csv("abundance.txt", sep="\t", index_col=0).T
    df = df.reset_index(drop=True)
    df = df.rename_axis(None, axis = 1)


    clf = load(os.path.join(utils.DEFAULT_DB_FOLDER, "gmhi1.joblib"))
    print(clf.health_abundant)
    print(clf.health_scarce)
    names = list(clf.feature_names_in_)

    set_diff = set(names) - set(df.columns)

    blank = pd.DataFrame(np.zeros((1, len(set_diff))), columns=set_diff, )
    concat = pd.concat([blank, df], axis=1)
    reindexed = concat[names]
    scaled = reindexed / reindexed.sum().sum()
    return scaled

def get_score():
    # df = get_clean_matrix()
    from GMHI import GMHI
    clf = load(os.path.join(utils.DEFAULT_DB_FOLDER, "gmhi1.joblib"))
    gmhi_score = clf.decision_function(df)
    return gmhi_score