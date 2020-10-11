import os
import collections
import numpy as np
import pandas as pd
import seaborn as sb
from collections import Counter
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

#return the number of messages in the csv file
def number_of_msgs(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    return df.shape[0]

#return the number of unique members of the group
def number_of_unique_members(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    return np.unique(df['Contacts']).shape[0]

# return the starting date of the group
def start_date(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    return df['Date'][0]

# return the end date of the group
def end_date(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    return df['Date'][df.shape[0]-1]


def average_length_msg(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    #average length of message
    i = 0
    for msg in df['Messages']:
        i+=(len(str(msg).split(' ')))
    return str(i/df.shape[0])


def max_length_msg(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    i = 0
    name=""
    for msg in df['Messages']:
        if(i < len(str(msg).split(' '))):
            if(df[df['Messages']==msg]['Contacts'].shape[0]>0):
                i = len(str(msg).split(' '))
                name = df[df['Messages']==msg]['Contacts'].values[0]
    return (i,name)



def weekday_busy(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    week = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:'Saturday',6:'Sunday'}
    return week[Counter(pd.to_datetime(df['Date']).dt.weekday).most_common(1)[0][0]]

def month_busy(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    month = {1:"January" , 2:"February" ,3:"March", 4:"April", 5:"May" , 6:"June", 7:"July",
             8:"August",9:"September", 10:"October", 11:"November", 12:"December"}
    return month[Counter(pd.to_datetime(df['Date']).dt.month).most_common(1)[0][0]]



def most(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    plt.figure(figsize=(8,12))
    sorted_active = df.groupby('Contacts').count()['Time'].sort_values()  
    if(df.groupby('Contacts').count().shape[0]>10):
        sb.barplot(sorted_active[-10:].values,
                   sorted_active[-10:].index,
                   palette='spring'
                  )
        j=-10
        for i, v in enumerate(sorted_active.values[-10:]):
            plt.text(0, i + 0.2, str(sorted_active.index[j]), color='black',fontsize=20)
            j+=1
    else:
        sb.barplot(sorted_active.values,
                   sorted_active.index,
                   palette='spring'
                  )
        j=-1*len(sorted_active.values)
        for i, v in enumerate(sorted_active.values):
            plt.text(0, i + 0.2, str(sorted_active.index[j]), color='black',fontsize=20)
            j+=1
    plt.title("Most Active Memebers",fontsize=20)
    plt.yticks([],[])
    plt.xticks(fontsize=16)
    plt.ylabel("")
    sb.despine(left=True)
    plt.savefig(os.path.join('static/images/dashboard',filename+'mactive.png') ,bbox_inches='tight')


def least(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    plt.figure(figsize=(6,6))
    sorted_active = df.groupby('Contacts').count()['Time'].sort_values()  
    if(df.groupby('Contacts').count().shape[0]>5):
        sb.barplot(sorted_active[:5].values,
                   sorted_active[:5].index, 
                   palette='spring'
                  )
        j=0
        for i, v in enumerate(sorted_active.values[:5]):
            plt.text(0, i + 0.2, str(sorted_active.index[j]), color='black',fontsize=20)
            j+=1
    else:
        sb.barplot(sorted_active.values,
                   sorted_active.index,
                   palette='spring'
                  )
        j=0
        for i, v in enumerate(sorted_active.values):
            plt.text(0, i + 0.2, str(sorted_active.index[j]), color='black',fontsize=20)
            j+=1
    plt.title("Least Active Memebers",fontsize=20)
    plt.yticks([],[])
    plt.xticks(fontsize=16)
    plt.ylabel("")
    sb.despine(left=True)
    plt.savefig(os.path.join('static/images/dashboard',filename+'lactive.png') ,bbox_inches='tight')


def week(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    plt.figure(figsize=(15,10))
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

    
    sb.barplot(x, values, palette='plasma')
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=18)
    
    plt.title("WeekDay-wise Messages", fontsize=20)
    sb.despine()
    plt.savefig(os.path.join('static/images/dashboard',filename+'week.png') ,bbox_inches='tight')
