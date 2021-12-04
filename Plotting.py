import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import re
from os.path import isdir,join
from os import mkdir

FILENAME = "Results2/Result_BBRoad_Robustness_{}_del.csv"
FILELIST = [
    "Results2/Result_BBRoad_Robustness_DFBC_del.csv",
    "Results2/Result_BBRoad_Robustness_DFBC_in.csv",
#    "Results2/Result_BBRoad_Robustness_1C_CM_del.csv",
#    "Results2/Result_BBRoad_Robustness_1C_CM_in.csv"
]
columns = pd.read_csv(FILENAME.format("BC"),header=0).columns

for measure in columns[1:]:
    for method in ["BC", "CM", "DFBC"]:
        delfile = FILENAME.format(method)
        infile = delfile.replace("_del", "_in")
        del_df = pd.read_csv(delfile,header=0)
        in_df = df = pd.read_csv(infile,header=0)
        df = pd.concat([del_df, in_df], sort=False, ignore_index=True)
        
        #postfix = "_".join(re.split('_|\.',delfile)[-3:-1])
        #postfix = "_".join(re.split('_|\.',filename)[-4:-1])
        #dirname = f"plots/{postfix}"
        dirname = f"plots/1Call"

        if not isdir(dirname):
            mkdir(dirname)

        plt.plot(df.index, df[measure], label=method)

    plt.xlabel("Steps")
    plt.ylabel(measure.replace("_", " ").capitalize())
    plt.legend()
    plt.savefig(join(dirname, f"{measure}.png"))
    plt.close()
    aa= 0 
aa = 0 

