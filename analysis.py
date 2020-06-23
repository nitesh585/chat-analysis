#Used to convert the raw text file into structured csv file
import os
import re
import pandas as pd
     
def analysis(filepath,filename):
    file  = open(filepath,"r")
    text = file.read()
    text = text.encode('ascii', 'ignore').decode('utf-8')
    i=0
    date = []
    time = []
    shift = []
    contact = []
    msgs = []

    split = text.split('\n')
    for s in split:
	  # regular expression to get the data, number and name in one go
        if(re.match('[0-9]+/[0-9]+/[0-9]+, [0-9]+:[0-9]+ [a-zA-Z]',s)):
            d = s.find(',')
            h = s.find('-')
            date.append( s[:d])
            time.append(s[d+1:h])
            shift.append(s[h-3:h])
            s = s[h+1:]
            start = s.find(':')
            contact.append(s[:start])
            msgs.append(s[start+2:])

    df = pd.DataFrame({"Date":date,
                   "Time" :time,
                   "Contacts" : contact,
                   "Messages" :msgs,
                   "Shift":shift})

    # Stopwords that should be removed from our text to make it clean
    stopwords = ['removed','left','added','lef','changed','was','joined','Messages','created',
                'were','group']
    
    for word in stopwords:
        df = df[~df['Contacts'].str.contains(word)]
    
    # remove extra space from front and back of the feature
    df['Date'] = df['Date'].str.strip()
    df['Time'] = df['Time'].str.strip()
    df['Contacts'] = df['Contacts'].str.strip()
    df['Messages'] = df['Messages'].str.strip()
    df['Shift'] = df['Shift'].str.strip()

    df['Date'] = pd.to_datetime(df['Date'])
    
    # change the format of date 
    df['Date'] = df['Date'].dt.strftime('%d/%m/%Y')
    
    df.index = [ i for i in range(1,len(df)+1)]
    # Save the file as csv on the server
    df.to_csv(os.path.join('csvs',filename),index=False)
    return 
