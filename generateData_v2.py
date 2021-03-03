import os;import os.path, time;import pandas as pd;import datetime;
#Dorian Yeh <3

mouseList = ['2149','2148','2151','2152']
#-------------------------------Don't touch anything below this pls--------------------------------------------------------------------------
directoryName = 'D:\FMON_Project\data\goodmice';
def GetFilePaths():
    experimentTypes = ['100-0', '90-10', '80-20', '60-40']; totalTrials = []; filePaths = []; #if more experiments are added, just make sure it is an entry in experimentTypes
    for mouse in mouseList: #directory information
        subDirectory = directoryName+'\Mouse_'+mouse;
        for experimentType in experimentTypes:
            experimentPath = os.path.join(subDirectory, experimentType);
            if os.path.isdir(experimentPath):
                for session in os.listdir(experimentPath):
                    path = os.path.join(experimentPath,session,'notes.txt');
                    if os.path.isfile(path):
                        filePaths.append(path);
    for path in filePaths: #opens/parses through notes.txt
        f = open(path); array = f.read().split('\n'); i = 0;
        date = time.ctime(os.path.getctime(path)); date_split = date.split(' '); #this pulls date/time created info from notes.txt
        while '' in date_split:
            date_split.remove('');
        month = date_split[1]; datetime_object = datetime.datetime.strptime(month, "%b");month_number = datetime_object.month;
        Numerized_Date = str(month_number) + '.'+ str(date_split[2])+'.'+str(date_split[4])+' '+str(date_split[3]);
        if array[5][0] == 'I': #array[x][y], x = the line where weight should be in notes.txt, y = the 'y'th character of array[x]
            weightSplit = array[5].split(': '); weight = weightSplit[1];
        else: #if notes.txt does not contain weight
            weight = 'NaN';
        if weight == 'NaN': #if the notes.txt file doesn't have a line for weight, then everything will be shifted one line
            odor = array[11].split(': ');concentration = array[12].split(': ');smell = str(odor[1]) + ' ' +str(concentration[1]);
        else: #there is a weight on line 9 in notes.txt
            odor = array[11].split(': '); concentration = array[12].split(': ');
            smell = str(odor[1]) + ' ' + str(concentration[1]);
        while array[i] != 'PERFORMANCE': #performance statistics
            i = i + 1;
        i = i + 1; rawData = [];
        while array[i] != '':
            rawData.append(array[i]);
            i = i + 1;
        for total in rawData:  # This cleans up parsed performance statistics data
            endStrip = total.strip('. ');elseStrip = endStrip.split('.  ');temp = elseStrip[0].split(": ");elseStrip[0] = temp[1];
            directorySplit = path.split('\\'); mouse = directorySplit[4].split('_'); experiment = directorySplit[5]; trialNumber = int(directorySplit[6]);
            mouseNumber = mouse[1]; tempData = []; actualData = [];
            for entry in elseStrip:
                tempSplit = entry.split('/');
                for item in tempSplit:
                    tempData.append(item);
            if experiment == '100-0': #if you want data for sessions other than the ones listed below, just add it in its own elif statement - assuming it is in experimentTypes (see above).
                actualData.extend([mouseNumber,weight,experiment,smell,trialNumber,tempData[0],tempData[1],tempData[8],tempData[9],Numerized_Date]);
            elif experiment == '90-10':
                actualData.extend([mouseNumber,weight,experiment,smell,trialNumber,tempData[2],tempData[3],tempData[6],tempData[7],Numerized_Date]);
        totalTrials.append(actualData);
    dataframe = pd.DataFrame(
        totalTrials,
        columns=['ID', 'initalWeight', 'experimentType', 'odorant+concentration','trial', 'totalCorrect',
                 'totalAttempts', 'controlCorrect', 'controlAttempts','datetime'
                 ]);
    dataframe.to_csv('Amanda_theGoodSpreadsheet.csv', index=False);
    print('CSV Generated!')
GetFilePaths()
