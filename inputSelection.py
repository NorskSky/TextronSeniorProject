import pandas as pd

def GMAInputSelection():
    gmaInputSelected = input("Select GMA Input to Baseline:  ")
    baselineData = pd.read_csv(f'baselineCapture/baselineCSV/{inputSelected}.csv')
	gmaOutSelected = [int(x) for x in input("List GMA Outputs to Analyze:  ").split()]
	
	print(baselineData.to_string(index=False))
