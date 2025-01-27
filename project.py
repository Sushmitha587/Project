import pyrebase 
from flask import Flask,render_template,request  #Flask is a method,render_template is a method  check the html  in  templates
app=Flask(__name__)  # app is object  __ is a special decorater
firebaseConfig = {

  "apiKey": "AIzaSyDwkbtB4flRwdL92HAfm3pV_rz6dBu2jLE",

  "authDomain": "mywebsite-95f0e.firebaseapp.com",

  "databaseURL": "https://mywebsite-95f0e-default-rtdb.firebaseio.com",

  "projectId": "mywebsite-95f0e",

  "storageBucket": "mywebsite-95f0e.appspot.com",

  "messagingSenderId": "336419066452",

  "appId": "1:336419066452:web:355a0db60b00f5d20893c1",

  "measurementId": "G-L667MMKES0"

};
firebase=pyrebase.initialize_app(firebaseConfig)
rdb=firebase.database()
sdb=firebase.storage()
count=0
@app.route("/",methods=["GET","POST"])  #/ path to the routing
def  hi():  #define the particular function
    global count
    if(request.form):
        click=request.form["btn"]
        if((click=="loginbtn") and (count==0)):
            return render_template("login.html")
        elif(click=="aboutbtn"):
            return render_template("jobpage3.html")
        elif(click=="aboutbtn"):
            return render_template("home.html")
        elif(click=="jobpagebtns"):
            return render_template("jobpage1.html")
        elif(click=="jobpagebtn"):
            return render_template("jobpage2.html")
        elif(click=="signupbtn"):
            return render_template("signup.html")
        elif(click=="registersbtn"):
            return render_template("home.html")
        elif(click=="signupsubmit"):
            uname=request.form["username"]
            pwd=request.form["password"]
            mail=request.form["email"]
            mobile=request.form["contect"]
            uname=uname.lower()
            details={"name":uname,
                     "password":pwd,
                     "mail":mail,
                     "number":mobile
                     }
            data=rdb.get().val()
            if(uname in data):
                return render_template("signup.html",msg="user exits")
            else:
                rdb.child(uname).update(details) #to store the multiple details we use a one child node ,upadte will .update a new details and , .set will delete the previous data and display the new data r updated date
                        
                return render_template("login.html")
        elif(click=="loginsubmit"):
            lname=request.form["luname"].lower()
            lpwd=request.form["lpassword"]
            dname=rdb.child(lname).child("name").get().val()
            dpwd=rdb.child(lname).child("password").get().val()
            if(lname==dname and lpwd==dpwd):
                sdb.child(lname).download(path="gs://"+firebaseConfig["storageBucket"]+"/",filename="static/"+lname+".png")
                return render_template("jobpage.html",msg="login sucessful")
            
            else:
                count+=1
                if(count<3):
                    return render_template("login.html" ,msg="wrong message" +str(3-count)+"attempts left")
                else:
                    return render_template("home.html", msg="blocked")
        elif(click=="registerbtn"):
            fname=request.form["first_name"]
            lname=request.form["last_name"]
            gend=request.form["gender"]
            fmail=request.form["femail"]
            img=request.files["resume"]
            fname=fname.lower()
            details={"sname":fname,
                     "yname":lname,
                     "gen":gend,
                     "smail":fmail
                     }
            rdb.child(fname).update(details)
            sdb.child(fname).put(img)
            
            
        
        
    return render_template("home.html",name="sk")
app.run(debug=True,port=5008)