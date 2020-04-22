import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template,url_for
from analysis import analysis
#from visualization import build_dashboard
from builddash import *

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html') 


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSION']


@app.route('/upload' , methods=['GET','POST'])
def upload():
    if request.method=='POST' :
        
        if 'file' not in request.files :
            return "file not found !!"
        
        file = request.files['file']

        if file.filename == "":
            return "No file passed"
        
        if file and allowed_file(file.filename): 

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename) 
            file.save(filepath)
            return analyze(filepath, filename)
             
        else :
            return "<h2>Extension not allowed !!</h2>"

    return render_template('index.html')


@app.route('/analyze',methods=['GET'])
def analyze(filepath,filename):
    analysis(os.path.join(app.config['UPLOAD_FOLDER'],filename),filename)
    
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
    avg = average_length_msg(filename)[:4]
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


@app.route('/about',methods=['GET'])
def about():
    return redirect('https://niteshrocks.github.io/ ')


if __name__=="__main__":
    app.run(debug=True)
