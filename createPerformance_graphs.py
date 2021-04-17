import pandas as pd
import matplotlib.pyplot as plt;import matplotlib.ticker as ticker;
import matplotlib;from matplotlib.lines import Line2D

def importData(): #note, clean up the notes.txt files
    rawFMON_data = 'https://raw.githubusercontent.com/civond/FMON_DataManagement/main/FMON_performanceData.csv';
    df = pd.read_csv(rawFMON_data);
    df['trialPercentage'] = df['totalCorrect'] / df['totalAttempts'];
    df.drop(df.columns.difference([
        'ID',
        'experimentType',
        'odor',
        'concentration',
        'trial',
        'trialPercentage',
        'totalAttempts'
    ]),1,
        inplace=True);

    fig, ax = plt.subplots()
    df100 = df[df['experimentType'] == '100-0'];
    df90 = df[df['experimentType'] == '90-10'];
    df90int = df[df['experimentType'] == '90-10_interleaved'];

    plot1 = plt.subplot2grid((2,2),(0,0));
    plot2 = plt.subplot2grid((2,2),(0,1));
    plot3 = plt.subplot2grid((2,2),(1,0));
    plot4 = plt.subplot2grid((2,2),(1,1));

    for mouseID in df100.ID.unique():
        df100_mouseSplit = df100[df100['ID'] == mouseID]
        fileTitle = 'figures/' + str(mouseID)+'_100Performance.png'
        for odor in df100_mouseSplit.odor.unique():
            odorSplit = df100_mouseSplit[df100_mouseSplit['odor'] == odor]
            x = odorSplit['trial'];y = odorSplit['trialPercentage'];attempts = odorSplit['totalAttempts']
            plot4.plot(x, attempts, color='cyan', linestyle='-');  # total pokes
            if odor == '2pe':
                plot1.plot(x,y,ms=4,marker='o', color='purple',linestyle='-');
            elif odor == 'pinene':
                plot1.plot(x,y,ms=4,marker='s', color='green',linestyle='-');
            elif odor == 'vanillin':
                plot1.plot(x,y,ms=4,marker='D', color='magenta',linestyle='-');
            elif odor == 'benzaldehyde':
                plot1.plot(x,y,ms=4,marker='p', color='red',linestyle='-');

        df90_mouseSplit = df90[df90['ID'] == mouseID]
        for odor in df90_mouseSplit.odor.unique():
            odorSplit = df90_mouseSplit[df90_mouseSplit['odor'] == odor]
            x = odorSplit['trial'];y = odorSplit['trialPercentage'];attempts = odorSplit['totalAttempts']
            plot4.plot(x,attempts,color='gray',linestyle='-.'); #total pokes
            if odor == '2pe':
                plot2.plot(x,y,ms=4,marker='o', color='purple',linestyle='--');
            elif odor == 'pinene':
                plot2.plot(x,y,ms=4,marker='s', color='green',linestyle='--');
            elif odor == 'vanillin':
                plot2.plot(x,y,ms=4,marker='D', color='magenta',linestyle='--');
            elif odor == 'benzaldehyde':
                plot2.plot(x,y,ms=4,marker='p', color='red',linestyle='--');

        df90int_mouseSplit = df90int[df90int['ID'] == mouseID]
        for odor in df90int_mouseSplit.odor.unique():
            odorSplit = df90int_mouseSplit[df90_mouseSplit['odor'] == odor]
            x = odorSplit['trial'];y = odorSplit['trialPercentage'];attempts = odorSplit['totalAttempts']
            plot4.plot(x,attempts,color='gray',linestyle='-.'); #total pokes
            if odor == '2pe':
                plot3.plot(x,y,ms=4,marker='o', color='purple',linestyle='.-');
            elif odor == 'pinene':
                plot3.plot(x,y,ms=4,marker='s', color='green',linestyle='.-');
            elif odor == 'vanillin':
                plot3.plot(x,y,ms=4,marker='D', color='magenta',linestyle='.-');
            elif odor == 'benzaldehyde':
                plot3.plot(x,y,ms=4,marker='p', color='red',linestyle='.-');

        for plot in plot1,plot2,plot3:
            plot.set_ylim([0.4,1])
        for axis in [ax.xaxis]:
            axis.set_major_locator(ticker.MaxNLocator(integer=True))
        plot1.title.set_text('{} 100-0 Performance'.format(mouseID))
        plot2.title.set_text('{} 90-10 Performance'.format(mouseID))
        plot3.title.set_text('{} Interleaved Performance'.format(mouseID))
        plot4.title.set_text('{} Total Trials Performed'.format(mouseID))

        #Labels
        for plot in plot1,plot2,plot3:
            plot.set_xlabel('Session', fontsize=7)
            plot.set_ylabel('% Correct', fontsize=7)

        plot4.set_xlabel('Session', fontsize=7);
        plot4.set_ylabel('Total Pokes', fontsize=7);

        plt.subplots_adjust(left=0.1,
                            bottom=0.1,
                            right=0.9,
                            top=0.9,
                            wspace=0.4,
                            hspace=0.4)
        #Legend
        plot1.legend(df100_mouseSplit.odor.unique(),shadow=True,fancybox=True,loc="best",fontsize='8')
        plot2.legend(df90_mouseSplit.odor.unique(),shadow=True,fancybox=True,loc="best",fontsize='8')
        plot3.legend(df90int_mouseSplit.odor.unique(),shadow=True,fancybox=True,loc="best",fontsize='8')
        #plot4.legend(df.experimentType.unique(),shadow=True,fancybox=True,loc="best")
        #plot4.legend([(color='gray',linestyle='-.'),][df100_mouseSplit.experimentType.unique(),df90_mouseSplit.experimentType.unique()])
        custom_lines = [Line2D([0],[0], color='cyan',linestyle='-'),
                        Line2D([0],[0], color='gray',linestyle='-.'),
                        Line2D([0],[0], color='pink',linestyle='--')]
        plot4.legend(custom_lines, ['100-0','90-10','90-10 Int'],shadow=True,fancybox=True,loc="best",fontsize='8')

        font = {'family': 'sans-serif',
                'weight': 'normal',
                'size': 9}
        matplotlib.rc('font', **font)

        plt.savefig(fileTitle);
        plot1.cla();plot2.cla();plot3.cla();plot4.cla()


importData()
