import os
import numpy as np
import pandas as pd
from contacts_less_than_5 import Contacts_less_than_5
from contacts_Greater_than_5 import Contacts_greater_than_5
from builddash import *
from flask import render_template


def build_dashboard(filename):
    df = pd.read_csv(os.path.join('csvs',filename))
    contacts = np.unique(df['Contacts']).shape[0]
    pie(filename)
    most(filename)
    word(filename)
    week(filename)
    msgs = number_of_msgs(filename)
    member = number_of_unique_members(filename)
    sdate = start_date(filename)
    edate = end_date(filename)
    avg = average_length_msg(filename)
    maxl , name = max_length_msg(filename)
    month = month_busy(filename)
    day =  weekday_busy(filename)

    if( np.unique(df['Contacts']).shape[0]>5):
        least(filename)
        return render_template("dash2.html" ,filename = filename, msgs=msgs, member=member,
        sdate=sdate, edate=edate, day=day,avg=avg,maxl=maxl,name=name, month=month)
    else:
        return render_template("dash1.html" ,filename = filename, msgs=msgs, member=member,
        sdate=sdate, edate=edate, day=day,avg=avg,maxl=maxl,name=name, month=month)
    