from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html') 
    
@app.route('/display', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        f = request.files['file']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f = open(app.config['UPLOAD_FOLDER']+filename,'r')
        a=f.read()
        a=a.lower();
        fmt="%I:%M:%p"
        totalmins=0;
        dele=a.find("time log:");
        if dele!=-1:
            a=a[dele+len("time log:"):]
            index=a.find('-')
            a1=a;
            while (index!=-1):
                if a1[index+1]==' ':
                    a1=a1[:index-1]+"&"+a1[index+2:];
                elif a1[index-1]==' ':
                    a1=a1[:index-2]+"&"+a1[index+1:]
                else:
                    a1=a1[:index-1]+"&"+a1[index+1:];
                index=a1.find("&",index-2,index+2);
                time1=a1.rfind(" ",0,index);
                time1=a1[time1+1:index];
                time2=a1.find("m",index,index+20);
                time2=a1[index+1:time2+1];
                time1=time1[:len(time1)-2]+":"+time1[len(time1)-2:]
                time2=time2[:len(time2)-2]+":"+time2[len(time2)-2:]
                try:
                    time1=datetime.strptime(time1,fmt)
                    time2=datetime.strptime(time2,fmt)
                    totalmins=totalmins+(time2-time1).seconds/60
                except:
                    index=a1.find('-')
                    continue;
                index=a1.find('-')
        output="Total Time is: "+str(int(totalmins//60))+" hrs "+str(int(totalmins%60))+" mins ";
        return render_template('index.html',result=output)
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)
