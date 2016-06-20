from flask import Flask, render_template,request,redirect,url_for
#---------------------------------- connect database lowcarb
import mongoengine
from mongoengine import Document, StringField

app = Flask(__name__,static_url_path='')

host = "ds025973.mlab.com"
port = 25973
db_name = "data_kcal"
user_name = "huong"
password = "123456"
mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

class Carb_recipes(Document):
    title = StringField()
    img = StringField()
    link = StringField()
    summary = StringField()
#------------------------- code bmi bmr


@app.route('/BMI_request<bmr>,<BMI>,<calo>,<calorie_to_eat>,<calorie_to_burn>,<bmi2>,<print_bmi>')
def BMI_request(bmr, BMI, calo,calorie_to_eat,calorie_to_burn, bmi2,print_bmi):
    return render_template('BMI_request.html', bmr=bmr, BMI=BMI, calo=calo,calorie_to_eat=calorie_to_eat,calorie_to_burn=calorie_to_burn,bmi2=bmi2,print_bmi=print_bmi)


class Person:
    def __init__(self, A, H, W, G, goal, activis, W2, month):
        self.A = request.form['age']
        self.W = request.form['weight']
        self.H = request.form['height']
        self.G = request.form['gender']
        self.goal = request.form['target']
        self.activis = request.form['activities']
        self.month = request.form['month']
        self.W2 = request.form['target weight']

    def BMR(self):
        if self.G == "Female":
            bmr = 665.09 + (9.56 * int(self.W)) + (1.84 * int(self.H)) - (4.67 * int(self.A))
            return bmr
        elif self.G == "Male":
            bmr = 66.47 + (13.75 * int(self.W)) + (5.0 * int(self.H)) - (6.75 * int(self.A))
            return bmr
        return 0

    def BMI(self):
        BMI = int(self.W) / (int(self.H) / 100) ** 2
        return BMI

    def print_bmi(self):
        if self.BMI() < 18.5:
            return "You are underweight. You should gain weight"
        elif self.BMI() >= 18.5 and self.BMI() <= 24.9:
            return " Healthy Weight"
        elif self.BMI() >= 25 and self.BMI() <= 29.9:
            return "You are overweight. You should lose weight"
        elif self.BMI() >= 30 and self.BMI() <= 34.9:
            return "You are Obese. You should lose weight"
        elif self.BMI() >= 35 and self.BMI() <= 39.9:
            return "You are Severely Obese. You should lose weight immediately"
        elif self.BMI() >= 40:
            return "You are Morbidly Obese. See your doctor soon"
        else:
            return 0


    def calo(self):
        if self.activis == "Little or no excercise":
            calo = self.BMR() * 1.2
            return calo
        elif self.activis == "Light exercise (1-3 times/week)":
            calo = self.BMR() * 1.35
            return calo
        elif self.activis == "Moderate exercise (3-5 days/week)":
            calo = self.BMR() * 1.55
            return calo
        elif self.activis == "Heavy exercise (6-7 days/week)":
            calo = self.BMR() * 1.75
            return calo
        elif self.activis == "Very heavy exercise (physical job or exercise twice a day)":
            calo = self.BMR() * 1.95
            return calo
        return 0

    def BMI_new(self):
        bmi_new = int(self.W2) / (int(self.H) / 100) ** 2
        return bmi_new

    def calorie_eat(self):
        if self.goal == "Lose weight":
            if self.BMI_new() < 18.5:
                weight_lose_per_day = (int(self.W) - int(self.W2)) * 7716.18 / (self.month * 4 * 7)
                calorie_to_eat = self.calo() - weight_lose_per_day
                return calorie_to_eat
            else:
                return 0
        elif self.goal == "Gain weight":
            if self.G == "male":
                calorie_to_eat = self.calo() + 250
                return calorie_to_eat
            elif self.G == "female":
                calorie_to_eat = self.calo() + 125
                return calorie_to_eat
            else:
                return 0
    def calorie_burn(self):
        if self.goal == "Lose weight":
            if self.BMI_new() > 18.5:
                calorie_to_burn = self.BMR() - self.calorie_eat()
                return calorie_to_burn
            else:
                return 0
        else:
            return 0

@app.route('/BMI', methods=['GET', 'POST'])
def bmi():
    if request.method == 'POST':
        # get bmr, bmi, .... from form
        A = int(request.form['age'])
        W = int(request.form['weight'])
        H = int(request.form['height'])
        G = str(request.form['gender'])
        goal = str(request.form['target'])
        activis = str(request.form['activities'])
        month = int(request.form['month'])
        W2 = int(request.form['target weight'])
        p = Person(A,W,H,G,goal,activis,month,W2)

        return redirect(url_for('BMI_request', bmr=p.BMR(), BMI=p.BMI(), calo=p.calo(),calorie_to_eat=p.calorie_eat(),calorie_to_burn=p.calorie_burn(),bmi2=p.BMI_new(),print_bmi=p.print_bmi()))
    return render_template("BMI.html")

# #---------------------------------- connect database shop
# import mongoengine
# from mongoengine import Document, StringField
# host = "ds025973.mlab.com"
# port = 25973
# db_name = "data_kcal"
# user_name = "huong"
# password = "123456"
# mongoengine.connect(db_name, host=host, port=port, username=user_name, password=password)

class Shop_das(Document):
    title = StringField()
    link = StringField()
    image = StringField()
#-------------------------

#----------------------- search
import pymongo
db_uri = "mongodb://huong:123456@ds025973.mlab.com:25973/data_kcal"
db = pymongo.MongoClient(db_uri).get_default_database()
kcal_collection = db['kcal']

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        def collect_choice(x):
            data_find = kcal_collection.find({'NAME': x})
            for i in data_find:
                short_descript=i['SHORT_DESCRIPT']
                traffic_light=i['TRAFFIC_LIGHT']
                carb=i['CARB']
                kcal= i['KCAL']
            return [short_descript,traffic_light,carb,kcal]
        n = str(request.form['name_search']).upper()
        [short_descript, traffic_light, carb, kcal] = collect_choice(n)
        return redirect(url_for('search',short_descript=short_descript,traffic_light=traffic_light,carb=carb,kcal=kcal))
    return render_template("index.html")

@app.route('/search<short_descript>,<traffic_light>,<carb>,<kcal>')
def search(short_descript,traffic_light,carb,kcal):
    return render_template("search.html",short_descript = short_descript ,traffic_light = traffic_light,carb = carb ,kcal =kcal)

@app.route('/index')
def index_return():
    return render_template("index.html")
# -------------------------------------------------
@app.route('/lowcarb')
def lowcarb():
    return render_template("lowcarb.html",data = Carb_recipes.objects)

@app.route('/shop')
def shop():
    return render_template("shop.html",data_shop = Shop_das.objects)




#--------------------------------------------------------------------
@app.route('/About Us')
def about_us():
    return render_template("About Us.html")

@app.route('/register')
def register():
    return render_template("register.html")

# @app.route('/login',methods=['GET','POST'])#vut thuoc tinh vao day
# def login():
#     if request.method == 'POST':
#         return redirect('/')
#     return render_template("login.html")

if __name__ == '__main__':
    app.run()
