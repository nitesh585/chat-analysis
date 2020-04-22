import os
import collections
import numpy as np
import pandas as pd
import seaborn as sb
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from wordcloud import WordCloud, STOPWORDS


def Contacts_greater_than_5(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    os.remove(os.path.join('csvs', filename))
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
    fig  = plt.GridSpec(13,4,wspace=0.4,hspace=0.5)
    plt.figure(figsize=(16, 50))

    # title
    ax1 = plt.subplot(fig[0, :])
    ax1.text(0.2, 0.4, 'CHAT ANALYSIS', weight='bold',
            color='#470070', fontsize="60")
    #sb.despine(left=True, bottom=True, ax=ax1)
    plt.xticks([], [])
    plt.yticks([], [])


    # 1st Row----------------------------
    ax2 = plt.subplot(fig[1, 0])
    msgs = df.shape[0]
    ax2.text(0.5, 0.4, msgs, horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax2.text(0.5, 0.1, 'Total Messages', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax2, left=True)
    plt.xticks([], [])
    plt.yticks([], [])

    ax3 = plt.subplot(fig[1, 1])
    members = np.unique(df['Contacts']).shape[0]
    ax3.text(0.5, 0.4, members, horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax3.text(0.5, 0.1, 'Members', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax3, left=True)
    plt.xticks([], [])
    plt.yticks([], [])

    ax4 = plt.subplot(fig[1, 2])
    sDate = df['Date'][0]
    ax4.text(0.5, 0.4, sDate, horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax4.text(0.5, 0.1, 'Start Date', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax4, left=True)
    plt.xticks([], [])
    plt.yticks([], [])

    ax5 = plt.subplot(fig[1, 3])
    eDate = df['Date'][df.shape[0]-1]
    ax5.text(0.5, 0.4, eDate, horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax5.text(0.5, 0.1, 'End Date', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax5, left=True)
    plt.xticks([], [])
    plt.yticks([], [])

    # 2nd Row-----------------------------
    ax6 = plt.subplot(fig[2, 0])
    i = 0
    for msg in df['Messages']:
        i += (len(str(msg).split(' ')))

    avgMsg = str(i/df.shape[0])
    ax6.text(0.5, 0.4, avgMsg[:4]+' words', horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax6.text(0.5, 0.1, 'Average msg length', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax6, left=True)
    plt.xticks([], [])
    plt.yticks([], [])

    ax7 = plt.subplot(fig[2, 1])
    length = 0
    name = ""
    for msg in df['Messages']:
        if(length < len(str(msg).split(' '))):
            length = len(str(msg).split(' '))
            name = df[df['Messages'] == msg]['Contacts'].values[0]

    ax7.text(0.5, 0.4, str(length)+' words', horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax7.text(0.5, 0.1, 'Maximum msg length', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax7, left=True)
    plt.xticks([], [])
    plt.yticks([], [])

    ax8 = plt.subplot(fig[2, 2])
    week = {0: "Monday", 1: "Tuesday", 2: "Wednesday",
            3: "Thursday", 4: "Friday", 5: 'Saturday', 6: 'Sunday'}
    busy_day = week[Counter(pd.to_datetime(
        df['Date']).dt.weekday).most_common(1)[0][0]]
    ax8.text(0.5, 0.4, busy_day, horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax8.text(0.5, 0.1, 'Most Busy WeekDay', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax8, left=True)
    plt.xticks([], [])
    plt.yticks([], [])


    ax9 = plt.subplot(fig[2, 3])
    month = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
            8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    busy_month = month[Counter(pd.to_datetime(
        df['Date']).dt.month).most_common(1)[0][0]]
    ax9.text(0.5, 0.4, busy_month, horizontalalignment='center',
            color='#9f21de', fontsize="30")
    ax9.text(0.5, 0.1, '    Most Busy Month    ', horizontalalignment='center',
            color='#8f8da6', fontsize="20")
    sb.despine(ax=ax9, left=True)
    plt.xticks([], [])
    plt.yticks([], [])


    # 3rd Row-----------------------------
    ax10 = plt.subplot(fig[3, :])
    ax10.set_facecolor('#9f21de')
    ax10.text(0.5, 0.4, name, weight='bold',
            horizontalalignment='center', color='white', fontsize="30")
    ax10.text(0.5, 0.1, 'Maximum Length Message Send By',
            horizontalalignment='center', color='#e9ddf0', fontsize="20")
    sb.despine(ax=ax10, left=True)
    plt.xticks([], [])
    plt.yticks([], [])


    # pie chart---------------------------
    pie_plot = plt.subplot(fig[4:6, :2])
    i=1
    df['Shift'] = pd.Series()
    for t in df['Time'] :
        if(str(t).endswith('am')):
            df['Shift'].loc[i] = 'am' 
        else :
            df['Shift'].loc[i] = 'pm'
        i+=1

    recipe = list( df.groupby('Shift').count()['Time'].index )
    data = list(df.groupby('Shift').count()['Time'].values)
    lable = list([str(recipe[0] + '\n'+str(data[0])+' msgs') ,str(recipe[1] + '\n'+str(data[1])+' msgs')])

    pie_plot.pie(data, textprops=dict( fontsize=18,
        color="black"), wedgeprops=dict(width=0.45), startangle=20 ,labels=lable)

    pie_plot.set_title("Messages in respective Meridian", fontsize=20)
    sb.despine(ax=pie_plot, left=True, bottom=True)

    # top active bar chart----------------
    top_active = plt.subplot(fig[4:8, 2:])
    sorted_active = df.groupby('Contacts').count()['Time'].sort_values()
    if(df.groupby('Contacts').count().shape[0] > 10):
        sb.barplot(sorted_active[-10:].values,
                sorted_active[-10:].index,
                ax=top_active,
                palette='spring'
                )
        j = -10
        for i, v in enumerate(sorted_active.values[-10:]):
            top_active.text(
                0, i + 0.2, str(sorted_active.index[j]), color='black', fontsize=20)
            j += 1
    else:
        sb.barplot(sorted_active.values,
                sorted_active.index,
                ax=top_active,
                palette='spring'
                )
        j = -1*len(sorted_active.values)
        for i, v in enumerate(sorted_active.values):
            top_active.text(
                0, i + 0.2, str(sorted_active.index[j]), color='black', fontsize=20)
            j += 1
    top_active.set_title("Most Active Memebers", fontsize=20)
    top_active.set_yticks([], [])
    top_active.set_ylabel("")
    sb.despine(ax=top_active, left=True)


    # least active data------------------
    least_active = plt.subplot(fig[6:8, :2])
    sorted_active = df.groupby('Contacts').count()['Time'].sort_values()
    if(df.groupby('Contacts').count().shape[0] > 5):
        sb.barplot(sorted_active[:5].values,
                sorted_active[:5].index,
                ax=least_active,
                palette='spring'
                )
        j = 0
        for i, v in enumerate(sorted_active.values[:5]):
            least_active.text(
                0, i + 0.2, str(sorted_active.index[j]), color='black', fontsize=20)
            j += 1
    else:
        sb.barplot(sorted_active.values,
                sorted_active.index,
                ax=least_active,
                palette='spring'
                )
        j = 0
        for i, v in enumerate(sorted_active.values):
            least_active.text(
                0, i + 0.2, str(sorted_active.index[j]), color='black', fontsize=20)
            j += 1
    least_active.set_title("Least Active Memebers", fontsize=20)
    least_active.set_yticks([], [])
    least_active.set_ylabel("")
    sb.despine(ax=least_active, left=True)


    # weekday wise msgs------------------
    week_plot = plt.subplot(fig[8:10, :])
    weekday = Counter(pd.to_datetime(df['Date']).dt.weekday)
    od = collections.OrderedDict(sorted(weekday.items()))
    values = []
    for value in od.values():
        values.append(value)
    keys = []
    for key in od.keys():
        keys.append(key)
    week = ["Monday", 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday', 'Sunday']

    x = []
    for k in keys:
        x.append(week[k])

    sb.barplot(x, values, palette='plasma', ax=week_plot)
    week_plot.set_xticklabels(x, fontsize=16)
    week_plot.set_title("WeekDay-wise Messages", fontsize=20)
    sb.despine(ax=week_plot)


    # WordCloud---------------------------
    word_Cloud = plt.subplot(fig[10:, :])
    new_stop = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
                'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
                "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
                'that', "that'll",'nan','media','omitted','media omitted'
                'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by',
                'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
                'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just',
                'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
                'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
                'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
                "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '0', '.', ',', '/', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '-'
                ]

    for stop in new_stop:
        STOPWORDS.add(stop)

    i = 0

    comment_words = ' '
    stopwords = set(STOPWORDS)

    # iterate through the csv file
    for val in df['Messages']:

        # typecaste each val to string
        val = str(val)

        if "media omitted" in val:
            i += 1
        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        for words in tokens:
            comment_words = comment_words + words + ' '


    wordcloud = WordCloud(width=1400, height=800,
                        background_color='white',
                        stopwords=stopwords,
                        min_font_size=15,
                        max_font_size=100,
                        colormap='plasma').generate(comment_words)

    word_Cloud.set_title("WORD CLOUD", fontsize=40)
    word_Cloud.imshow(wordcloud)
    word_Cloud.axis("off")

    plt.savefig(os.path.join('static/images/dashboard',filename+'.png'), bbox_inches='tight')
    return