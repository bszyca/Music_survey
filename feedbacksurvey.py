#from re import A
from flask import Flask,render_template, request
from flask_mysqldb import MySQL
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'music_survey'

#global lang = 0

mysql = MySQL(app)

questions = [
  "1. Płeć",
  "2. Wiek",
  "3. Wykształcenie",
  "4. Wybierz stwierdzenie, które najlepiej Cię opisuje:sytuacja zawodowa ",
  "5. Wybierz stwierdzenie, które najlepiej Cię opisuje: odnosnie muzyki",
  "6. Kraj pochodzenia",
  "7. Wielkość miejsca zamieszkania",
  "8. Czy twój nastrój wpływa na wybór słuchanych utworów?",
  "9. Czy grasz na jakimś instrumencie? Jeśli tak, to jakim?" ,
  "10. Jakich gatunków najczęściej słuchasz?",
  "11. Jak długo słuchasz muzyki w sposób aktywny (słuchanie muzyki jest dominującą czynnością, nie tłem) dziennie?",
  "12. Jak długo słuchasz muzyki w pasywny (muzyka jest dodatkiem, tłem dla innych czynności) dziennie?",
  "13. Czy zdarza Ci się słuchać muzyki w celu odcięcia się od otoczenia?",
  "14. Czy spotkaniom towarzyskim, na które uczęszczasz, towarzyszy muzyka?",
  "15. Jaki jest Twój preferowany sposób słuchania muzyki?",
  "16. Czy korzystasz z platformy streamingowej dpo słuchania muzyki? Jeśli tak, to z jakiej?",
  "17. Czy korzystasz z radia internetowego? Jeśli tak to z jakiej stacji? - pytanie dot. mieszkańców Polski",
  "18. Czy korzystasz z radia FM? Jeśli tak to z jakiej stacji? - pytanie dot. mieszkańców Polski",
  "19. Czy uważasz, że audycje radiowe przeplatane muzyką są atrakcyjne?",
  "20. Czy audycje poświęcone tylko muzyce są dla Ciebie atrakcyjne?",
  "21. W jaki sposób wybierasz odtwarzane utwory?",
  "22. Jaki jest stopień dopasowania playlist proponowanych do twojego gustu muzycznego?", 
  "23. Czy playlisty słuchasz w całości, czy też pomijasz niektóre utwory?"
]

answers_new =[]

@app.route('/')
def form():
    global lang
    lang = 'PL'
    return render_template('main.html')
 
@app.route('/save', methods = ['GET','POST'])
def save():
      if request.method == 'POST':
            #dodajemy appendem odpowiedzi do tablicy
            answers_new.append(request.form['answer1'])
            answers_new.append(request.form['answer2'])
            answers_new.append(request.form['answer3'])
            answers_new.append(request.form['answer4'])
            answers_new.append([','.join(request.form.getlist("answer5"))])
            answers_new.append(request.form['answer6'])
            answers_new.append(request.form['answer7'])
            answers_new.append(request.form['answer8'])
            answers_new.append(request.form['answer9'])
            answers_new.append([','.join(request.form.getlist("answer10"))])
            answers_new.append(request.form['answer11'])
            answers_new.append(request.form['answer12'])
            answers_new.append(request.form['answer13'])
            answers_new.append(request.form['answer14'])
            answers_new.append([','.join(request.form.getlist("answer15"))])
            answers_new.append([','.join(request.form.getlist("answer16"))])
            answers_new.append([','.join(request.form.getlist("answer17"))])
            answers_new.append([','.join(request.form.getlist("answer18"))])
            answers_new.append(request.form['answer19'])
            answers_new.append(request.form['answer20'])
            answers_new.append([','.join(request.form.getlist("answer21"))])
            answers_new.append(request.form['answer22'])
            answers_new.append(request.form['answer23'])
        
            cursor = mysql.connection.cursor()
            
            #pobranie user_id z db
            cursor.execute('''SELECT MAX(user_id) from feedback''')
            maxid = cursor.fetchone()

            #jesli nie ma rekordow w bazie zacznij od 0 
            if(maxid[0]==None):
                  maxid = return_max_id_value_if_none(maxid)

            #dodanie wartosci do nowej listy
            consecutive_params = []
            consecutive_params.append(maxid[0] + 1)
            for i in range(0,len(questions)):
                  consecutive_params.append(questions[i])
                  consecutive_params.append(answers_new[i])

            params_tuple = tuple(consecutive_params)
            length_of_tuple = len(params_tuple)

            #jakies gowno sqlowe
            sql_query = "INSERT INTO feedback VALUES(" + "%s,"*(length_of_tuple-1) + "%s)"
            cursor.execute(sql_query, params_tuple)
            mysql.connection.commit()
            cursor.close()
      if lang != 'PL':
            return render_template('thx.html')
      else:
            return render_template('dzieki.html')

@app.route('/eng')
def eng():
      global lang
      lang = 'ENG'
      return render_template('eng.html')
      
@app.route('/onas')
def onas():
    global lang
    lang = 0
    return render_template('onas.html')

@app.route('/about')
def about():
      global lang
      lang = 1
      return render_template('about.html')

@app.route('/dzieki')
def dzieki():
    return render_template('dzieki.html')

@app.route('/thx')
def thx():
    return render_template('thx.html')

def return_max_id_value_if_none(maxid):
      newlist = list(maxid)
      newlist[0] = -1
      return tuple(newlist)

app.run(host='localhost', port=5000)