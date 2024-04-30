import pandas as pd

def GMAInputSelection():
    gmaInputSelected = input("Select GMA Input to Baseline:  ")
    baselineData = pd.read_csv(f'baselineCapture/baselineCSV/{gmaInputSelected}.csv')
    return baselineData
    #print(baselineData.to_string(index=False))    

def GMAOutputSelection(baselineData):
    gmaOutSelected = [int(x) for x in input("List up to 8 GMA Outputs to Analyze:  ").split()]
    gmaOutputDict = dict()
    for output in gmaOutSelected:
        gmaOutputDict[output] = (float(baselineData.at[output-1,"Min"]),float(baselineData.at[output-1,"Max"]))
    return gmaOutputDict

def ADC_Channels(gmaOutputDict):
    ADC_channels = dict()
    for output in gmaOutputDict.keys():
        ADC_channels[int(input('GMA Output {} plugged into which FTM Channel? '.format(output)))] = output
    return ADC_channels
    