import os;import os.path, time;import pandas as pd;import datetime;from operator import itemgetter;from collections import OrderedDict;
from github import Github;from github import InputGitTreeElement;
#Dorian Yeh <3

mouseList = ['2139','2140','2141','2148','2150','2151','2152','2153','2154','2155']; #this script will output all session data into two spreadsheets

#---------------Lists below for outputting DAILY stats in a .txt file only-----------------------------------------------------------------------
trainer1Mice = ['2153','2154'] #trainer1 mice ***ONLY***
hundredMice = ['2151']; #100-0 mice
ninetyMice = ['2152']; #90-10 mice
interleavedMice = [] #90-10 interleaved mice
#-------------------------------Don't touch anything below this pls--------------------------------------------------------------------------
directoryName = 'D:\FMON_Project\data\goodmice';
def GetFilePaths():
    experimentTypes = ['100-0', '90-10', '90-10_interleaved']; totalTrials = []; filePaths = []; #if more experiments are added, just make sure it is an entry in experimentTypes
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
        print(path)
        f = open(path); array = f.read().split('\n'); i = 0;
        date = time.ctime(os.path.getctime(path)); date_split = date.split(' '); #this pulls date/time created info from notes.txt
        while '' in date_split:
            date_split.remove('');
        month = date_split[1]; datetime_object = datetime.datetime.strptime(month, "%b");month_number = datetime_object.month;
        Numerized_Date = str(month_number) + '.'+ str(date_split[2])+'.'+str(date_split[4])+' '+str(date_split[3]);
        if array[5][0] == 'I': #array[x][y], x = the line where weight should be in notes.txt, y = the 'y'th character of array[x]
            weightSplit = array[5].split(': '); weight = weightSplit[1];
            if weightSplit[1] == '':
                weight = 'NaN';
        else: #if notes.txt does not contain weight
            weight = 'NaN';
        if weight == 'NaN': #if the notes.txt file doesn't have a line for weight, then everything will be shifted one line
            odor = array[11].split(': ');concentration = array[12].split(': ');smell = str(odor[1]) + ' ' +str(concentration[1]);
        else: #there is a weight on line 9 in notes.txt
            if array[10][5] == 'T':
                odor = array[10].split(': ');concentration = array[11].split(': ');
            else:
                odor = array[11].split(': '); concentration = array[12].split(': ');
            smell = str(odor[1]) + ' ' + str(concentration[1]);
        while array[i] != 'PERFORMANCE': #performance statistics
            i = i + 1;
        i = i + 1; rawData = [];
        while array[i] != '':
            rawData.append(array[i]);
            i = i + 1;
        endStrip = rawData[0].strip('. ');elseStrip = endStrip.split('.  ');temp = elseStrip[0].split(": "); elseStrip[0] = temp[1];
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
        columns=[
            'ID','initalWeight','experimentType','odorant+concentration','trial',
            'totalCorrect','totalAttempts','controlCorrect','controlAttempts','datetime'
        ]);
    dataframe.to_csv('FMON_performanceData.csv', index=False);print('goodmice CSV Generated!');

def trainer1_GetFilePaths():
    totalTrials = []; filePaths = []; #if more experiments are added, just make sure it is an entry in experimentTypes
    for mouse in mouseList: #directory information
        subDirectory = directoryName+'\Mouse_'+mouse;
        experimentPath = os.path.join(subDirectory, 'trainer1');
        if os.path.isdir(experimentPath):
            for session in os.listdir(experimentPath):
                #subpath = os.path.join(experimentPath,session);
                path = os.path.join(experimentPath,session,'notes.txt');
                if os.path.isfile(path):
                    filePaths.append(path);
    for path in filePaths: #opens/parses through notes.txt
        print(path)
        f = open(path); array = f.read().split('\n'); i = 0;
        date = time.ctime(os.path.getctime(path)); date_split = date.split(' '); #this pulls date/time created info from notes.txt
        while '' in date_split:
            date_split.remove('');
        month = date_split[1]; datetime_object = datetime.datetime.strptime(month, "%b");month_number = datetime_object.month;
        Numerized_Date = str(month_number) + '.'+ str(date_split[2])+'.'+str(date_split[4])+' '+str(date_split[3]);
        if array[5][0] == 'I': #array[x][y], x = the line where weight should be in notes.txt, y = the 'y'th character of array[x]
            weightSplit = array[5].split(': '); weight = weightSplit[1];
            if weight == '':
                weight = 'NaN';
        else: #if notes.txt does not contain weight
            weight = 'NaN';
        while array[i] != 'PERFORMANCE': #performance statistics
            i = i + 1;
        i = i + 1; rawData = [];
        while array[i] != '':
            rawData.append(array[i]);
            i = i + 1;
        periodSplit = rawData[0].split('. '); runningTotal = 0;
        for item in periodSplit:
            split = item.split(': '); runningTotal += int(split[1]);
        directorySplit = path.split('\\'); mouse = directorySplit[4].split('_'); experiment = directorySplit[5]; trialNumber = int(directorySplit[6]);
        mouseNumber = mouse[1]; tempData = []; actualData = [];
        actualData.extend([mouseNumber,weight,experiment,trialNumber,runningTotal,Numerized_Date]);
        totalTrials.append(actualData);
    dataframe = pd.DataFrame(
        totalTrials,
        columns=[
            'ID','initalWeight','experimentType','trial',
            'totalPokes','datetime'
        ]);
    dataframe.to_csv('T1_FMON_performanceData.csv', index=False);print('CSV Generated!');print('T1_CSV Generated!');

def outputStatsFile():
    elsemice = open('FMON_performanceData.csv');t1_mice = open('T1_FMON_performanceData.csv');
    hundredDict = {};ninetyDict = {};hundredList = [];ninetyList = [];interleavedDict = {};interleavedList = [];t1List=[];t1Dict={};
    for line in elsemice:
        if line == '\n': continue;
        mouse, initialWeight,experimentType,odorantconcentration,trial,totalCorrect,totalAttempts,controlCorrect,controlAttempts,datetime = line.strip('\n').split(',');
        if mouse == 'mouse': continue;
        if mouse in hundredMice:  #refer to the top
            if mouse == mouse and experimentType == '100-0':
                if mouse not in hundredDict:
                    hundredDict.update({mouse: [totalCorrect + '/' + totalAttempts]});hundredList.append(mouse);
                else:
                    hundredDict[mouse].append(totalCorrect + '/' + totalAttempts);
        if mouse in ninetyMice:  # if the mouse in in the top list
            if mouse == mouse and experimentType == '90-10':
                if mouse not in ninetyDict:
                    ninetyDict.update({mouse: [totalCorrect + '/' + totalAttempts]});ninetyList.append(mouse);
                else:
                    ninetyDict[mouse].append(totalCorrect + '/' + totalAttempts);
        if mouse in interleavedMice:
            if mouse == mouse and experimentType == '90-10_interleaved':
                if mouse not in interleavedDict:
                    interleavedDict.update({mouse: [totalCorrect + '/' + totalAttempts]});interleavedList.append(mouse);
                else:
                    interleavedDict[mouse].append(totalCorrect + '/' + totalAttempts);
    for line in t1_mice:
        if line == '\n': continue;
        mouse, initalWeight, experimentType, trial, totalPokes, datetime = line.strip('\n').split(',');
        if mouse == 'mouse': continue;
        if mouse in trainer1Mice:  # refer to the top
            if mouse == mouse and experimentType == 'trainer1':
                if mouse not in t1Dict:
                    t1Dict.update({mouse: [totalPokes]});
                    t1List.append(mouse);
                else:
                    t1Dict[mouse].append(totalPokes);
    dict3 = OrderedDict(sorted(hundredDict.items()));dict4 = OrderedDict(sorted(ninetyDict.items()));dict5 = OrderedDict(sorted(interleavedDict.items()));t1Dict=OrderedDict(sorted(t1Dict.items()));
    entries3 = [];entries4 = [];entries5 = [];t1entries = [];
    for dictionary in dict3,dict4,dict5,t1Dict:
        for entry in dictionary:
            result = dictionary[entry][len(dictionary[entry]) - 1];
            if entry in hundredList:
                temp = str(entry) + '(*100-0* #' + str(len(dictionary[entry])) + ') - ' + str(result);entries3.append(temp);
            elif entry in ninetyList:
                temp = str(entry) + '(*90-10* #' + str(len(dictionary[entry])) + ') - ' + str(result);entries4.append(temp);
            elif entry in interleavedList:
                temp = str(entry) + '(*90-10 interleaved* #' + str(len(dictionary[entry])) + ') - ' + str(result);entries5.append(temp);
            elif entry in t1List:
                temp = str(entry) + '(*trainer1* #' + str(len(dictionary[entry])) + ') - ' + str(result);t1entries.append(temp);
    textFile = open(r"stats.txt", "w+"); #generates .txt file
    for stats in entries3, entries4,entries5,t1entries:
        for item in stats:
            textFile.writelines('%s\n' % item);
        if len(stats) > 0:
            textFile.write('\n');
    textFile.close();print('Daily Stats Generated!');

GetFilePaths()
trainer1_GetFilePaths()
outputStatsFile()
from githubPush import *;
