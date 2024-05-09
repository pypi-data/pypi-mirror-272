import pandas as pd
import numpy as np
from rapidfuzz import fuzz as fz
from joblib import Parallel, delayed

def nameMatch(in_path="", out_path="", miles_sheet_name="Miles Names", icra_sheet_name="ICRA Names"):

    milesSheet = pd.read_excel(in_path, sheet_name=miles_sheet_name).dropna()
    icraSheet = pd.read_excel(in_path, sheet_name=icraSheet).dropna()

    # Define the fuzzy metric (uncomment any one of the metric)
    metric = fz.ratio
    # Define Threshold for Metric
    thresh = 40
    ca = np.array(icraSheet[["All ICRA Names"]])
    cb = np.array(milesSheet[["sch_name"]])

    #Parallel Code
    def parallel_fuzzy_match(idxa,idxb):
        return [ca[idxa][0],cb[idxb][0],metric(ca[idxa][0],cb[idxb][0])]  

    results = Parallel(n_jobs=-1,verbose=1)(delayed(parallel_fuzzy_match)(idx1, idx2) for idx1 in range(len(ca)) for idx2 in range(len(cb)) \
                    if(metric(ca[idx1][0],cb[idx2][0]) > thresh))
    results = pd.DataFrame(results,columns = ["ICRA fund name","Miles fund name","Score"])
    idx = results.groupby(['ICRA fund name'])['Score'].transform(max) == results['Score']
    asd = results[idx]

    writer = pd.ExcelWriter(out_path, engine = 'openpyxl')
    icraSheet.to_excel(writer, sheet_name = 'ICRA')
    milesSheet.to_excel(writer, sheet_name = 'Miles')
    asd.to_excel(writer, sheet_name = 'Result')
    writer.close()