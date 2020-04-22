import os
import collections
import numpy as np
import pandas as pd
import seaborn as sb
from collections import Counter
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS


def number_of_msgs(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    return df.shape[0]


def number_of_unique_members(filename):
    df = pd.read_csv(os.path.join('csvs/',filename))
    return np.unique(df['Contacts']).shape[0]


def start_date(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    return df['Date'][0]


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



def pie(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    plt.figure(figsize=(6,6))
    recipe = list( df.groupby('Shift').count()['Time'].index )
    data = list(df.groupby('Shift').count()['Time'].values)
    lable = list([str(recipe[0] + '\n'+str(data[0])+' msgs') ,str(recipe[1] + '\n'+str(data[1])+' msgs')])

    plt.pie(data, textprops=dict( fontsize=15,
        color="black"), wedgeprops=dict(width=0.45), startangle=20 ,labels=lable)

    plt.title("Messages in respective Meridian", fontsize=20)
    sb.despine( left=True, bottom=True)
    plt.savefig(os.path.join('static/images/dashboard',filename+'pie.png') ,bbox_inches='tight')


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



def word(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    plt.figure(figsize=(20,15))
    new_stop = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
                'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
                "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 
                'that', "that'll", 
                'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 
                'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 
                'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 
                'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 
                'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 
                'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 
                'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
                'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn',
                "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't",'1','2','3','4','5','6','7',
                '8','9','0','.',',','/','!','@','#','$','%','^','&','*','(',')','+','-','media','omitted','media omitted','nan','message deleted'
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
            i+=1
        # split the value 
        tokens = val.split() 

        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower() 

        for words in tokens: 
            comment_words = comment_words + words + ' '


    wordcloud = WordCloud(width = 1400, height = 800,
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10,
                    max_font_size = 150,      
                    colormap= 'plasma').generate(comment_words) 

    plt.title("WORD CLOUD",fontsize=40)
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.savefig(os.path.join('static/images/dashboard',filename+'word.png') ,bbox_inches='tight')
