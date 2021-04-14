import pandas as pd;
import matplotlib.pyplot as plt;


def importData():  # note, clean up the notes.txt files
    rawFMON_data = 'FMON_performanceData.csv';
    df = pd.read_csv(rawFMON_data);
    df['trialPercentage'] = df['totalCorrect'] / df['totalAttempts'];
    df.drop(df.columns.difference([
        'ID',
        'experimentType',
        'odor',
        'concentration',
        'trial',
        'trialPercentage',
    ]), 1, inplace=True);
    fig, ax = plt.subplots()
    df100 = df[df['experimentType'] == '100-0'];
    for mouseID in df100.ID.unique():
        df100_mouseSplit = df100[df100['ID'] == mouseID]
        fileTitle = 'figures/' + str(mouseID) + '_100Performance.png'
        for odor in df100_mouseSplit.odor.unique():
            odorSplit = df100_mouseSplit[df100_mouseSplit['odor'] == odor]
            if odor == '2pe':
                odorSplit.plot(x='trial', y='trialPercentage', ax=ax, legend=False, marker='o', color='purple');
            elif odor == 'pinene':
                odorSplit.plot(x='trial', y='trialPercentage', ax=ax, legend=False, marker='s', color='green');
            elif odor == 'vanillin':
                odorSplit.plot(x='trial', y='trialPercentage', ax=ax, legend=False, marker='D', color='magenta');
            elif odor == 'benzaldehyde':
                odorSplit.plot(x='trial', y='trialPercentage', ax=ax, legend=False, marker='p', color='red');
        # df100_mouseSplit.groupby('odor').plot(x='trial', y='trialPercentage', ax=ax, legend=False,marker='o');
        plt.title('{} 100-0 Performance'.format(mouseID));
        plt.xlabel('Session', fontsize=12);
        plt.ylabel('Percentage Correct', fontsize=12)
        plt.legend(df100_mouseSplit.odor.unique())
        plt.savefig(fileTitle);
        plt.cla();
        print(str(mouseID) + ' graph generated')
    # plt.show()


importData()