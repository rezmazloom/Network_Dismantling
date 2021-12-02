import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
from os.path import isdir,join
from os import mkdir


FILELIST = [
    "Results2/Result_BBRoad_Robustness_BC_del.csv",
    "Results2/Result_BBRoad_Robustness_BC_in.csv",
    "Results2/Result_BBRoad_Robustness_CM_del.csv",
    "Results2/Result_BBRoad_Robustness_CM_in.csv"
]

for filename in FILELIST:
    df = pd.read_csv(filename,header=0)
    columns = df.columns
    postfix = "_".join(re.split('_|\.',filename)[-3:-1])
    dirname = f"plots/{postfix}"

    if not isdir(dirname):
        mkdir(dirname)

    for idx, col in enumerate(columns[1:]):
        plt.plot(df.index, df[col])

        plt.savefig(join(dirname, f"{col}.png"))
        plt.close()
aa = 0 

