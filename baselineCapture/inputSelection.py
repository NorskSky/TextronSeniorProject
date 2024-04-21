import pandas as pd

def inputSelection():
    inputSelected = input("Select Input to Baseline:  ")
    baselineData = pd.read_csv(f'baselineCapture/baselineCSV/{inputSelected}.csv')
    print(baselineData.to_string(index=False))
    
