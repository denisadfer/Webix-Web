from flask import Flask, jsonify, session, render_template, request
from connectdb import Database

app = Flask(__name__)
app.secret_key = 'secret'

conn = Database('ksb-2022')

@app.route('/', methods=['GET'])
def index():
  session['login'] = False
  if session['login'] == True:
    return render_template('dashboard.html')
  else:
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
  username = request.form.get('username')
  password = request.form.get('password')
  if username == 'admin' and password == 'admin':
    session['login'] = 1
    return jsonify({'status': 'success'})
  else:
    return jsonify({'status': 'error'})

@app.route('/logout', methods=['GET'])
def logout():
  session.pop('login', None)
  return render_template('index.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
  if session['login'] == True:
    return render_template('dashboard.html')
  else:
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
  if session['login'] == True:
    result = conn.select("SELECT * FROM public.denis_672019245")
    return render_template('data.html', data=result)
  else:
    return render_template('index.html')

@app.route('/data/insert', methods=['GET'])
def insert():
  if session['login'] == True:
    return render_template('insert.html')
  else:
    return render_template('index.html')

@app.route('/insert_data', methods=['POST'])
def insert_data():
  if session['login'] == True:
    name = request.form.get('name')
    city = request.form.get('city')
    room = request.form.get('room')
    check_in = request.form.get('check_in')
    sql = "INSERT INTO denis_672019245 (name, city, room, check_in) VALUES (%s, %s, %s, %s)"
    val = name, city, str(room), str(check_in)
    conn.execute(sql,(val))
    return jsonify({'status': 'success'})
  else:
    return render_template('index.html')

@app.route('/data/delete/<id>', methods=['DELETE'])
def delete(id):
  if session['login'] == True:
    sql = "DELETE FROM denis_672019245 WHERE id = %s"
    conn.execute(sql,(id,))
    return jsonify({'status': 'success'})
  else:
    return render_template('index.html')

@app.route('/data/edit/<id>', methods=['GET'])
def edit(id):
  if session['login'] == True:
    result = conn.select("SELECT * FROM public.denis_672019245 WHERE id = "+id)
    return render_template('edit.html', data=result)
  else:
    return render_template('index.html')

@app.route('/edit_data', methods=['POST'])
def edit_data():
  if session['login'] == True:
    id = request.form.get('id')
    name = request.form.get('name')
    city = request.form.get('city')
    room = request.form.get('room')
    check_in = request.form.get('check_in')
    sql = "UPDATE denis_672019245 SET name = %s, city = %s, room = %s, check_in = %s WHERE id = %s"
    val = name, city, str(room), str(check_in), id
    conn.execute(sql,(val))
    return jsonify({'status': 'success'})
  else:
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host="localhost", port=8080 , debug=True)