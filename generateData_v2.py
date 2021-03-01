import os
import pandas as pd
from operator import itemgetter
from collections import OrderedDict

# みんなのドリアン <３
#--------------------------------------------------------------------------------------------------------------------------------------------
mouseList = ['2131','2132']

#-------------------------下の内容を触るな！------Don't touch anything below this pls------------------------------------------------------------
directoryName = 'D:\FMON_Project\data\goodmice';
def GetFilePaths():
    experimentTypes = ['trainer2', '100-0', '90-10', '80-20', '60-40']; totalTrials = []; filePaths = []; #if more experiments are added, just make sure it is an entry in experimentTypes
    for mouse in mouseList: #directory information
        subDirectory = 'Mouse_'+mouse;
        for experimentType in experimentTypes:
            experimentPath = os.path.join(subDirectory, experimentType);
            if os.path.isdir(experimentPath):
                for session in os.listdir(experimentPath):
                    path = os.path.join(experimentPath,session,'notes.txt');
                    if os.path.isfile(path):
                        filePaths.append(path);
    for path in filePaths: #parses through notes.txt
        f = open(path); array = f.read().split('\n'); i = 0;
        if array[3][0] == 'I': #the line where weight should be
            weightSplit = array[3].split(': '); weight = weightSplit[1];
        else: #if notes.txt does not contain weight
            weight = 'NaN';
        if weight == 'NaN': #if the notes.txt file doesn't have a line for weight, then everything will be shifted one line down
            odor = array[7].split(': '); concentration = array[8].split(': ');
            smell = str(odor[1]) + ' ' +str(concentration[1]);
        else: #there is a weight on line 9 in notes.txt
            odor = array[8].split(': '); concentration = array[9].split(': ');
            smell = str(odor[1]) + ' ' + str(concentration[1]);
        while array[i] != 'PERFORMANCE': #performance statistics
            i = i + 1;
        i = i + 1;
        rawData = [];
        while array[i] != '':
            rawData.append(array[i]);
            i = i + 1;
        for total in rawData:  # This cleans up parsed performance statistics data
            endStrip = total.strip('. '); elseStrip = endStrip.split('.  ');
            temp = elseStrip[0].split(": "); elseStrip[0] = temp[1];
            directorySplit = path.split('/'); mouse = directorySplit[0].split('_'); experiment = directorySplit[1]; trialNumber = int(directorySplit[2]);
            mouseNumber = mouse[1];
            tempData = []; actualData = [];
            for entry in elseStrip:
                tempSplit = entry.split('/');
                for item in tempSplit:
                    tempData.append(item);
            if experiment == 'trainer2': #if you want data for sessions other than the three listed below, just add it in its own elif statement - assuming it is in experimentTypes (see above).
                actualData.extend([mouseNumber,weight,experiment,smell,trialNumber,tempData[2],tempData[3],tempData[6],tempData[7]]);
            elif experiment == '100-0':
                actualData.extend([mouseNumber,weight,experiment,smell,trialNumber,tempData[2],tempData[3],tempData[6],tempData[7]]);
            elif experiment == '90-10':
                actualData.extend([mouseNumber,weight,experiment,smell,trialNumber,tempData[2],tempData[3],tempData[6],tempData[7]]);
        totalTrials.append(actualData);
    dataframe = pd.DataFrame(
        totalTrials,
        columns=['ID', 'initalWeight', 'experimentType', 'odorant','session', 'totalCorrect',
                 'totalAttempts', 'controlCorrect', 'controlAttempts'
                 ]);
    dataframe.to_csv('Amanda_theGoodSpreadsheet.csv', index=False);

GetFilePaths()
