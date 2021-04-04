import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def importData(): #note, clean up the notes.txt files
    rawFMON_data = 'https://raw.githubusercontent.com/civond/FMON_DataManagement/main/FMON_performanceData.csv';
    df = pd.read_csv(rawFMON_data);
    df['trialPercentage'] = df['totalCorrect'] / df['totalAttempts'];
    df[['odorant', 'concentration']] = df.odorantConc.str.split(' ', expand=True)

    df.drop(df.columns.difference([
        'ID',
        'experimentType',
        'odorant',
        'concentration',
        'trial',
        'trialPercentage',
    ]),
        1, inplace=True);
    df['odorant'] = df['odorant'].replace(['pinene(7)'], 'pinene');
    df['odorant'] = df['odorant'].replace(['2-pe','2-PE'], '2pe');
    df['odorant'] = df['odorant'].replace(['vanillin(7)','Vanillin'], 'vanillin');
    df['odorant'] = df['odorant'].replace(['Benzaldehyde'], 'benzaldehyde');
    fig, ax = plt.subplots()

    df100 = df[df['experimentType'] == '100-0'];
    #df100_pinene = df100[df100['odorant'] == 'pinene'];
    #df100_pinene.groupby('ID').plot(x='trial', y='trialPercentage', ax=ax, legend=False);

    #df100_2pe = df100[df100['odorant'] == '2pe'];
    #df100_2pe.groupby('ID').plot(x='trial', y='trialPercentage', ax=ax, legend=False);

    #df100_vanillin = df100[df100['odorant'] == 'vanillin'];
    #df100_vanillin.groupby('ID').plot(x='trial', y='trialPercentage', ax=ax, legend=False);

    df100.groupby('ID').plot(x='trial', y='trialPercentage', ax=ax, legend=False);


    #plt.legend(['ID'])
    plt.xlabel("Session")
    plt.ylabel("Percentage Correct")
    plt.title("100-0 Overall Performance")
    #ax.set_xlim(right=35)

    plt.show()

importData()
