"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,request,redirect,url_for
from DataProject1 import app,db,login_manager
from DataProject1.Datamodule1 import create_html_page_for_src1,create_html_page_for_src2,create_plot_for_compere,Get_Data_From_Qeruy
from DataProject1.Usermodule import user
from flask_login import login_required, logout_user, current_user, login_user
from flask_wtf import FlaskForm
from wtforms import DateTimeField,SubmitField,SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField


class Qury_(FlaskForm):
    datasource = SelectField(choices=[('Hacinert','הכנרת'), ('yamhamelach','ים המלח')],validators = [DataRequired('please select ')])
    date = DateField('select date',format='%Y-%m-%d',validators=[DataRequired('please select ')])


    submit = SubmitField("serach")


@login_manager.user_loader
def load_user(user_id):
    try:
        return user.query.get(user_id)
    except:
        return None



@app.route('/')
@app.route('/home')
def home():
    textbox1= "כשהכינרת מגיעה לקו העליון פותחים את סכר דגניה ומשחררים מים מהכינרת לים המלח לכן אני אראה את הנותונים על איך מפלס הכינרת משפיע על מפלס ים המלח"
    textbox = " איך מפלס הכינרת משפיע על מלס ים המלח"
    return render_template('index.html')

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST": # בודק עם התקבלה בקשת post
        uname = request.form["uname"] # מבקש מהבקשה שהתקבלה את המשתנה שמחזיק את השם משתמש
        passw = request.form["passw"]# מבקש מהבקשה שהתקבלה את המשתנה שמחזיק את הסיסמה
        
        login = user.query.filter_by(username=uname, password=passw).first() # בודק עם היוזר נמצע בדאטה בייס
        if login is not None: # עם קיים משתמש כזה
            login_user(login) #  תתחבר למשתמש
            return redirect(url_for("home")) # תעבור לדף  הבית
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        register = user(username = uname, email = mail, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")




@app.route('/DataPageMenu')
@login_required
def DataPageMenu():
    DataSorces = [("DataPage1","ים המלח"),("DataPage2","הכנרת"),("CompereData",'השוואה')]
    TextBlock = "המקור מידע מתייחס לכנרת"
    return render_template('DataPageMenu.html',DataSorces=DataSorces,TextBlock=TextBlock)


@app.route('/DataPage1') #ים המלח 
@login_required
def data_page1():
    Tables = create_html_page_for_src1()
    FildInfoTable = [["הסבר",'שדה'],["מפלס ים המלח במטרים",'מפלס'],['התאריך שבו התקבל המפלס','תאריך מדידה'],[None,'טבלת נתונים']]
    TextBlock = "המקור מידע מתייחס לים המלח"
    IMG1 = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Dead_sea_ecological_disaster_1960_-_2007.gif/200px-Dead_sea_ecological_disaster_1960_-_2007.gif"
    IMG2 = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/The_Dead_Sea_and_Surroundings_EL.png/250px-The_Dead_Sea_and_Surroundings_EL.png "
    return render_template('DataPage1.html',tables=[Tables],title="ים המלח",FildInfoTable=FildInfoTable,TextBlock=TextBlock,IMG1=IMG1,IMG2=IMG2)

@app.route('/DataPage2') #הכנרת
@login_required
def data_page2():
    
    Tables = create_html_page_for_src2()
    FildInfoTable = [["הסבר",'שדה'],["מפלס הכנרת במטרים",'מפלס'],['התאריך שבו התקבל המפלס','תאריך מדידה'],[None,'טבלת נתונים']]
    IMG1 = " https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Bathymetric_map_of_Sea_of_Galilee.jpg/250px-Bathymetric_map_of_Sea_of_Galilee.jpg"
    IMG2 = " https://kineret.org.il/wp-content/uploads/2018/01/Screen-Shot-2018-01-15-at-2.49.16-PM-1.png"
    return render_template('DataPage1.html',tables=[Tables],title="הכנרת",FildInfoTable=FildInfoTable,IMG1=IMG1,IMG2=IMG2)

@app.route('/CompereData')
def compere_data_page():
    plot,plot1 = create_plot_for_compere()
    Tables = [(create_html_page_for_src2(),"הכנרת"),(plot,"plot",plot1),(create_html_page_for_src1(),"ים המלח")]
    
    return render_template('CompreData.html',tables=Tables)

@app.route('/qurey',methods=['GET','POST'])
@login_required
def query():
    q_from = Qury_()

    table = None
    if q_from.validate():
        cooltime = q_from.date.data

        table = Get_Data_From_Qeruy(cooltime.year, cooltime.month,cooltime.day,q_from.datasource.data)


    return render_template('QueryPage.html',form=q_from,tables=[table])

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

