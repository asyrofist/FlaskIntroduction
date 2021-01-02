from flask import Flask, render_template, url_for, request, redirect # import library flask berisi render template, url_for, request dan redirect
from flask_sqlalchemy import SQLAlchemy  # import library flask sqlalchemy sebagai database
from datetime import datetime # import library datetime sebagai tanggal

app = Flask(__name__) # buat file app dari flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # buat sebuah konfigurasi dengan database bernama test.db
db = SQLAlchemy(app) # buat database berdasarkan sqlalchemy

class Todo(db.Model): # membuat kelas todo untuk membuat model database
    id = db.Column(db.Integer, primary_key=True) # buat kolom database id, dengan tipe integer bersifat primary key
    content = db.Column(db.String(200), nullable=False) # buat kolom content, dengan tipe string berjumlah 200
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # buat kolom date, dengan nilai default berdasarkan UTC

    def __repr__(self):
        return '<Task %r>' % self.id # kembalikan nilai ke file id


@app.route('/', methods=['POST', 'GET']) # buat route dengan '/' dengan metode POST dan GET
def index(): # buat fungsi index
    if request.method == 'POST': # apabila request yang dilakukan, dengan metode POST. Maka lakukan proses selanjutnya.
        task_content = request.form['content'] # buat task konten dengan form request berdsarkan content.
        new_task = Todo(content=task_content) # buat task baru dengan nilai konten berdasarkan task konten

        try: # apabila benar, maka masuk database
            db.session.add(new_task)   #buat sesi database
            db.session.commit() #buat sesi commit database
            return redirect('/') # kembalikan nilai ke awal route
        except: # apabila salah, maka muncul error issue
            return 'There was an issue adding your task'

    else: # apabila request bukan dengan metode POST, maka lakukan proses selanjutnya.
        tasks = Todo.query.order_by(Todo.date_created).all() # task yang dimuat berdasarkan urutan tanggal query yang dibuat,
        return render_template('index.html', tasks=tasks) #kembali ke index, dengan nilai task sama seperti sebelumnya.


@app.route('/delete/<int:id>') #buat rute delete berdasarkan id
def delete(id): # buat fungsi delete berdasarkan id
    task_to_delete = Todo.query.get_or_404(id) # lakukan proses delete, apabila tidak bisa muncul 404

    try: #apabila benar lakukan proses database
        db.session.delete(task_to_delete) # delete sesi database
        db.session.commit() # buat sesi commit
        return redirect('/') # kembali nilai ke awal route
    except: # apabil¡a salah, maka muncul error issue
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST']) #buat rute update berdasarkan id dengan metode GET dan POST
def update(id): # buat fungsi update berdasarkan id
    task = Todo.query.get_or_404(id) # lakukan proses task berdasarkan query, apabila tidak bisa muncul 404

    if request.method == 'POST': # apabila request yang dilakukan, dengan metode POST. Maka lakukan proses selanjutnya.
        task.content = request.form['content'] # buat task konten dengan form request berdsarkan content.

        try: # apabila benar lakukan proses 
            db.session.commit() # buat sesi commit
            return redirect('/') # kembalikan nilai ke awal route
        except: #apabila salah, maka muncul error issue
            return 'There was an issue updating your task'

    else: # apabila request yang dilakukan maka lakukan proses selanjutnya.
        return render_template('update.html', task=task) 


if __name__ == "__main__": # buat kondisi main
    app.run(debug=True) # lakukan proses debug route
