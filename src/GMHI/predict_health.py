import pandas as pd
from .GMHI import GMHI_model
from joblib import load
import numpy as np
from . import utils
import os

def get_score():
    df = pd.read_csv("abundance.txt", sep="\t", index_col=0).T
    df = df.reset_index(drop=True)
    df = df.rename_axis(None, axis = 1)

    clf = GMHI_model()
    names = list(clf.features)

    set_diff = set(names) - set(df.columns)

    blank = pd.DataFrame(np.zeros((1, len(set_diff))), columns=set_diff, )
    concat = pd.concat([blank, df], axis=1)
    reindexed = concat[names]
    scaled = reindexed / reindexed.sum().sum()
    gmhi_score = clf.decision_function(scaled)
    return gmhi_score[0]