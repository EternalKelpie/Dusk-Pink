from flask import Flask, jsonify, request, send_from_directory, render_template, session, flash, request, redirect, url_for
from Backend.DungeonGenerator import GenerateRooms
import json
from pathlib import Path
from flask_session import Session
import sqlite3, random

app = Flask(__name__, template_folder="Frontend")
app.secret_key = "some-secret-key"

sess = Session()

DATABASE = 'database.db'

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "map.json"
file_path_NPC = BASE_DIR / "NPC.json"
file_path_NPC_gen = BASE_DIR / "NpcTraitsForGen.json"

@app.route('/createDB', methods =['GET', 'POST'] )
def create_database():
    db = sqlite3.connect(DATABASE)
    db.execute('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE , password TEXT, admin INTEGER)')
    db.execute('CREATE TABLE npc (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, race TEXT, job TEXT, looks TEXT, trait TEXT ,user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id))',)
    db.execute("INSERT INTO users (username, password, admin) VALUES ('admin', 'admin', 1)")
    db.commit()
    db.close()
    return "created"

@app.route('/saveNpcToJson')
def saveNpcToJson():
      name = request.args.get("name", default ="Kira", type=str)
      race = request.args.get("race", default ="Elf", type=str)
      job = request.args.get("job", default ="jobless", type=str)
      looks = request.args.get("looks", default ="basic anime character", type=str)
      act = request.args.get("act", default ="eats nuts all the time", type=str)
      data={
                      "name" : name,
                      "race" : race,
                      "job"  : job,
                      "looks": looks,
                      "trait": act
          
              }
      with open(file_path_NPC, "w", encoding="utf-8") as file:
              json.dump(data, file, indent=4, ensure_ascii=False)
      
      return "saved successfully"

@app.route('/saveNpcToDB')
def saveNpcToDB():
      db= sqlite3.connect(DATABASE)
      cur = db.cursor()
      name = request.args.get("name", default ="Kira", type=str)
      race = request.args.get("race", default ="Elf", type=str)
      job = request.args.get("job", default ="jobless", type=str)
      looks = request.args.get("looks", default ="basic anime character", type=str)
      act = request.args.get("act", default ="eats nuts all the time", type=str)
      user_id = session.get('user_id')
      db.execute("INSERT INTO npc (name, race, job, looks,trait, user_id ) VALUES (?, ?, ?, ?, ?, ?)", (name,race, job, looks,act, user_id ))
      db.commit()
      db.close()
      return "saved successfully"
          

@app.route('/oldNpc', methods=['GET', 'POST'])
def oldNpc():
        db= sqlite3.connect(DATABASE)
        cur = db.cursor()
        cur.execute("SELECT name, race, job, looks, trait FROM npc")
        npc=cur.fetchall()
        print("NPC FROM DATABASE:", npc)
        db.close()
        return render_template('oldNpc.html', npc=npc)

@app.route('/loadUsersNpc')
def loadUsersNpc():
      db= sqlite3.connect(DATABASE)
      cur = db.cursor()
      user_id = session.get('user_id')
      cur.execute("SELECT id, name, race, job, looks, trait FROM npc WHERE user_id=?", (user_id,))
      npc=cur.fetchall()
      db.close()
      return render_template('UserNpc.html', npc=npc)

@app.route("/deleteNPC/<int:npc_id>", methods=['POST'])
def deleteNPC(npc_id):
    if 'user' not in session:
        return redirect(url_for('home'))
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE FROM npc WHERE id=?", (npc_id,))
    con.commit()
    con.close()
    return redirect(url_for('loadUsersNpc'))

@app.route('/')
def home():
    if 'user' in session:
         if session.get('admin', 0) == 1:
            return render_template("MapGenerator.html", user = 2)
         else:  
              return render_template("MapGenerator.html", user = 1)           
    return render_template("MapGenerator.html",  user = 0)

@app.route('/createNpc')
def createNpc():
    return render_template("createNpc.html")

@app.route('/generateNpc')
def generateNpc():
    with open(file_path_NPC_gen, "r", encoding="utf-8") as file:
         options = json.load(file)
         npc ={key: random.choice(values) for key, values in options.items()}
         return jsonify(npc)
    


@app.route("/")
def index():
    return send_from_directory("Frontend", "MapGenerator.html")

@app.route("/<path:filename>")
def frontend_file(filename):
    return send_from_directory("Frontend", filename)

@app.route('/load')
def load():
    if not file_path.exists():
        return jsonify({"error": "File does not exist"}), 404
    
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

        return jsonify(data)

@app.route('/loadNPC')
def loadNPC():
    if not file_path.exists():
        return jsonify({"error": "File does not exist"}), 404
    
    with open(file_path_NPC, "r", encoding="utf-8") as file:
        data = json.load(file)

        return jsonify(data)

@app.route('/generate')
def generate():
    roomCount = request.args.get("rooms", default =5, type=int)
    getIsLoot = request.args.get("isLoot", default ="true").lower() =="true"
    getIsEnc = request.args.get("isEnc", default ="true").lower() =="true"
    dungeon  = GenerateRooms(roomNumber = roomCount, isLoot=getIsLoot, isEnc= getIsEnc)

    data={
                "map" : dungeon
    
        }
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return jsonify(
        {
            "map" : dungeon

        }
    )
    
# tutaj do zmian, żeby to miało sens z tym cop aktualnie mam ______________________________________________________________________
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST": 
        login = request.form.get("login", "").strip()
        password = request.form.get("password", "")
        if not login or not password:
            return render_template(
                'login.html',
                error="Enter username and password"
            )
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT id, username, admin FROM users WHERE username=? AND password=?", (login, password))
        row = cur.fetchone()
        con.close()
        if row:
            session['user_id'] = row[0]
            session['user'] = row[1]
            session['admin'] = row[2]
            return redirect(url_for('home'))
        return render_template('login.html', error ="Wrong login or password")
    return render_template('login.html')


@app.route("/logout", methods=["POST"])
def logout():
        session.pop('user', None)
        session.pop('admin', None)
        return redirect(url_for('home'))




@app.route("/adminPanel", methods=['GET', 'POST'])
def adminPanel():
    if 'user' not in session:
        return redirect(url_for('home'))
    if session.get('admin') != 1:
         return redirect(url_for('home'))
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    if request.method=="POST":
         login = request.form['login']
         password = request.form['password']
         admin = 1 if "admin" in request.form else 0
         con.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", (login, password, admin))
         con.commit()
    cur.execute("SELECT id, username, password, admin FROM users")
    users = cur.fetchall()
    con.close()
    return render_template('adminPanel.html', users=users)

         
@app.route("/deleteUser/<int:user_id>", methods=['POST'])
def deleteUser(user_id):
    if 'user' not in session:
        return redirect(url_for('home'))
    if session.get('admin') != 1:
        return redirect(url_for('home'))
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT username FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    if row and row[0] != session['user']:
        cur.execute("DELETE FROM users WHERE id=?", (user_id,))
        con.commit()
    con.close()
    return redirect(url_for('adminPanel'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)