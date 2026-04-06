from datetime import datetime
from flask import Flask, flash, get_flashed_messages, g, jsonify,  render_template, request, redirect, session, url_for
from functools import wraps
import os
import sqlite3
from sqlite3 import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash



# Create Flask app; tell Flask where templates and static files live
# Compute the app directory relative to this file for portability
APP_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(APP_DIR, 'templates')
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=os.path.join(APP_DIR, 'static'))


app.config["SESSION_PERMANENT"] = False
app.config["SECRET_KEY"] = "dev-secret-key-change-later-jk"

if not app.config['SECRET_KEY']:
    raise ValueError("No SECRET_KEY set for Flask application. Check environment variables.")


# A shortcut to make changes to the databases
def get_db():
    db_path = os.path.join(APP_DIR, 'practice.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  
    return conn


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def validate_required(fields):

    errors = [f"must provide {name}" for name, value in fields.items() 
                  if not value or not value.strip()]
        
    for error in errors:
        flash(error)

    return errors


# Format practice time. ( ex: 65 minutes -> 1 hour 5 minutes) 
@app.template_filter("format_time")
def format_time(minutes):
    try:
        minutes = int(minutes)
    except(TypeError, ValueError):
        return "0 minutes"
    
    hours = minutes // 60
    remaining = minutes % 60

    time = []

    if hours == 1:
        time.append("1 hour")
    elif hours > 1:
        time.append(f"{hours} hours")

    if remaining == 1:
        time.append("1 minute")
    elif remaining > 1 or hours == 0:
        time.append(f"{remaining} minutes")

    return" ".join(time)




# Convert a timestamp string to a nicely formatted date.
@app.template_filter('format_datetime')
def format_datetime(value, fmt="%b %d, %Y – %H:%M"):
    
    if not value:
        return ""
    # value comes as a string like "2026-02-17 19:34:22"
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime(fmt)


@app.context_processor
def inject_current_user():
    """Make current_user available to all templates.

    Returns a dict with `current_user` set to the username string when logged in,
    or None otherwise.
    """
    user_id = session.get('user_id')
    if not user_id:
        return {'current_user': None}

    conn = get_db()
    try:
        cur = conn.cursor()
        row = cur.execute('SELECT username FROM users WHERE id = ?', (user_id,)).fetchone()
        if row:
            return {'current_user': row[0]}
        else:
            return {'current_user': None}
    finally:
        conn.close()


# Create a new account
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == "POST":
        username = " ".join(request.form.get("username", "").split())
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if (len(password) < 6):
            flash("password must be at least 6 characters")
            return redirect(request.referrer)


        hash = generate_password_hash(password)

        fields = {
           "username" : username,
           "password" : password,
           "password confirmation" : confirm
        }
        
        errors = validate_required(fields)
        if errors:
            return redirect('/register')
        

        
        with get_db() as conn:
            cur = conn.cursor()

            cur.execute("SELECT id FROM users WHERE username = ? COLLATE NOCASE", (username,))
            row = cur.fetchone()

            if row is not None:
                flash("username already taken")
                return redirect("/register")

            # Adds new username and password to the 'users' DB
            # Store hashed password in the `hash` column
            cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
            conn.commit()
            user_id = cur.lastrowid

            session["user_id"] = user_id
            return redirect("/")

    else:
        return render_template('register.html')
        
# Log in if user already has an existing account 
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""
    if request.method == 'POST':

        username = request.form.get("username").strip()
        password = request.form.get("password")
    

        fields = {
           "username" : username,
           "password" : password,
        }

        errors = validate_required(fields)
        if errors:
            flash("validate fields")
            return redirect("/login")
        
        with get_db() as conn:
        
            cur = conn.cursor()
            rows = cur.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,)).fetchall()

            if rows == None or len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
                flash("Invalid username or password")
                return redirect("/login")
            
            session["user_id"] = rows[0]["id"]
            return redirect("/")
        

    else:
        return render_template('login.html')
    


@app.route('/')
@login_required
def home():

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
        row = cur.fetchone()

        if row is None:
            session.clear()
            return redirect("/login")
        
        username = row["username"]
        
        # Select pieces the user is working on to display it on the home page.

        cur.execute("""SELECT pw.title, pw.composer, up.piece_id, up.id AS project_id
             FROM user_projects up 
             JOIN piano_works pw ON pw.id = up.piece_id 
             WHERE up.status == 'in-progress' AND up.user_id = ?""", (session["user_id"], ))
        
        projects = cur.fetchall()

        # Select and display user's past practice session data.

        cur.execute("""SELECT ps.*, pw.title, pw.composer   
                    FROM practice_sessions ps
                    JOIN user_projects up ON  ps.project_id = up.id
                    JOIN piano_works pw ON up.piece_id = pw.id
                    WHERE up.user_id = ?
                    ORDER BY ps.created_at DESC;""", (session["user_id"],) )
        
        sessions = cur.fetchall()

        cur.execute("""WITH user_sessions AS (
            SELECT ps.minutes, date(ps.created_at) AS day
            FROM practice_sessions ps
            JOIN user_projects up ON ps.project_id = up.id
            WHERE up.user_id = ?
        ),

        week_stats AS (
            SELECT
                SUM(minutes) AS weekly_minutes
            FROM user_sessions
            WHERE day >= date('now','weekday 0','-7 days')
        ),

        practice_days AS (
            SELECT DISTINCT day
            FROM user_sessions
        ),

        numbered_days AS (
            SELECT
                day,
                ROW_NUMBER() OVER (ORDER BY day DESC) AS rn
            FROM practice_days
        ),

       streak_calc AS (
            SELECT COUNT(*) AS streak
            FROM (
                SELECT
                    day,
                    ROW_NUMBER() OVER (ORDER BY day DESC) AS rn,
                    julianday(date('now')) - julianday(day) AS diff
                FROM practice_days
            )
            WHERE diff = rn - 1
        )

        SELECT
            week_stats.weekly_minutes,
            streak_calc.streak
        FROM week_stats, streak_calc;""",(session["user_id"],))
        
        stats = cur.fetchone()

        weekly_minutes = stats["weekly_minutes"] or 0
        streak = stats["streak"]

    if not projects:
        message = "Welcome"
    else:
        message = "Welcome back"

    return render_template('index.html', username=username,
                            projects=projects,
                            sessions=sessions, 
                            weekly_minutes=weekly_minutes,
                            streak=streak,
                            message=message)


@app.route("/projects")
@login_required
def index():
    if request.method == "GET":

        filter = request.args.get('filter', 'in-progress')

        with get_db() as conn:
            cur = conn.cursor()

            if filter == "all":
                cur.execute("""SELECT pw.title, pw.composer, up.status, up.piece_id, up.id AS project_id
             FROM user_projects up 
             JOIN piano_works pw ON pw.id = up.piece_id 
             WHERE up.user_id = ?""", (session["user_id"], ))

            
            else: 
                cur.execute("""SELECT pw.title, pw.composer, up.status, up.piece_id, up.id AS project_id
                FROM user_projects up 
                JOIN piano_works pw ON pw.id = up.piece_id  
                WHERE up.status = ? AND up.user_id = ?""", (filter, (session["user_id"]) ))
            
            pieces = cur.fetchall()
            

        return render_template('projects.html', pieces = pieces, filter = filter)

@app.route("/project/<int:project_id>", methods=['GET', 'POST'])
@login_required
def project(project_id):

    with get_db() as conn:
        cur = conn.cursor()

        # Fetch project info
        cur.execute("""
            SELECT pw.title,
                   pw.composer,
                   up.id AS project_id,
                   up.status
            FROM user_projects up
            JOIN piano_works pw ON pw.id = up.piece_id
            WHERE up.id = ? AND up.user_id = ?
        """, (project_id, session["user_id"]))

        project = cur.fetchone()
        if project is None:
            return redirect("/")

        # Fetch all practice sessions for this project
        cur.execute("""
            SELECT minutes, notes, created_at, id
            FROM practice_sessions
            WHERE project_id = ?
            ORDER BY created_at DESC
        """, (project_id,))
        practice_sessions = cur.fetchall()

        # Sum total minutes
        total_minutes = sum(s['minutes'] for s in practice_sessions)

    return render_template("project.html",
                           project=project,
                           practice_sessions=practice_sessions,
                           total_minutes=total_minutes)

@app.route("/project/<int:project_id>/log", methods =["POST"])
@login_required
def log_practice(project_id):
    
    minutes_raw = request.form.get("minutes", "").strip()
    notes = request.form.get("notes")

    if not minutes_raw.isdigit():
        flash("Minutes must be a positive number.")
        return redirect(request.referrer)

    minutes = int(minutes_raw)


    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO practice_sessions (project_id, minutes, notes) values (?, ?, ?)", 
                    (project_id, minutes, notes))
        
    return redirect(request.referrer)

@app.route("/project/<int:project_id>/delete", methods =["POST"])
@login_required
def delete_project(project_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM user_projects WHERE id = ? AND user_id = ?", (
            project_id, session["user_id"]))
        
    return redirect("/projects")

@app.route("/project/<int:project_id>/status", methods=["POST"])
@login_required
def complete(project_id):
     button_value = request.form['status']
     with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE user_projects SET status = ? WHERE id = ? AND user_id = ?",
                     (button_value, project_id, session["user_id"]))
        
        flash("Project status updated!", "success")
        return redirect(url_for("project", project_id=project_id))
     
@app.route("/session/<int:session_id>/edit", methods=["POST"])
@login_required
def edit_session(session_id):
    minutes = request.form.get("minutes")
    notes = request.form.get("notes")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE practice_sessions
            SET minutes = ?, notes = ?
            WHERE id = ?
        """, (minutes, notes, session_id))
        conn.commit()

    flash("Session updated.", "success")
    return redirect(request.referrer)

@app.route("/session/<int:session_id>/delete", methods=["POST"])
@login_required
def delete_session(session_id):

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM practice_sessions
            WHERE id = ?
        """, (session_id,))
        conn.commit()

    flash("Session deleted.", "success")
    return redirect(request.referrer)



@app.route("/search-pieces")
@login_required
def search_pieces():
    query = request.args.get("q","").strip().lower()
    terms = query.split()

    conditions =[]
    params = []

    for term in terms:
        conditions.append("(title LIKE ? or composer LIKE ?)")
        params.extend([f"%{term}%", f"%{term}%"])
        

    sql =f""" 
    SELECT * FROM piano_works WHERE {' AND '.join(conditions)}
    """


    conn = get_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql, params)

    results = [dict(row) for row in cur.fetchall()]

    
    conn.close()
    
    return jsonify(results)


@app.route('/add-piece/', methods=['GET', 'POST'])
@login_required
def add_piece():
    if request.method == "POST":

        #for existing pieces in piano_works
        if request.is_json:
            pieceId = request.get_json('piece_id')['piece_id']

        #for custom entries
        else:
            title = request.form.get("title")
            composer = request.form.get("composer") or ""

            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO piano_works (composer, title) VALUES (?, ?)", (composer, title))

                pieceId = cur.lastrowid
            
        try:
            with get_db() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO user_projects (user_id, piece_id) VALUES (?, ?)", (session["user_id"], pieceId))

                if request.is_json:
                    return jsonify({"success": True})
                else:
                    return redirect("/projects")

        except IntegrityError:
            if request.is_json:
                return jsonify({"success": False, "error": "duplicate"}), 409
            else:
                return redirect("/projects")
    else: 
        """Add a new piece to your repertoire """
        return render_template('add-piece.html')

@app.route('/remove-piece', methods=['POST'])
@login_required
def remove_piece():

    data = request.get_json()
    pieceId = data['piece_id']

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM user_projects WHERE user_id = ? AND piece_id = ?",
            (session["user_id"], pieceId)
        )

    return jsonify({"success": True})

@app.route('/account')
def account():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
        current_name = dict(cur.fetchone())["username"]

    return render_template("account.html", current_name=current_name)

@app.route('/change_username', methods =['POST'])
def change_username():
    if request.method=="POST":

        new = " ".join(request.form.get("username", "").split())
        if not new:
            flash("Must enter a username")
            return redirect(request.referrer)
        
    password = request.form.get("password")
    with get_db() as conn:
        cur = conn.cursor()
        
        cur.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],))
        hash = cur.fetchone()["hash"]
    
    
        if not password:
            flash("Missing Password")
            return redirect(request.referrer)
        if not check_password_hash(hash, password):

            flash("Incorrect Password")
            return redirect(request.referrer)
        cur.execute("UPDATE users SET username = ? WHERE id = ?", (new, session["user_id"]))
    return redirect("/")
    
@app.route('/change_password', methods =["POST"])
def change_password():
    
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],))
        hash = cur.fetchone()["hash"]
    

    current_password = request.form.get("current-password")
    new_password = request.form.get("new-password")
    confirmation = request.form.get("retype-password")

    if not current_password or not new_password or not confirmation:
        flash("Missing password field")
        return redirect(request.referrer)
    
    if not check_password_hash(hash, current_password):
        flash("Incorrect Password")
        return redirect(request.referrer)
    
    if check_password_hash(hash, new_password):
        flash("Password was not changed")
        return redirect(request.referrer)

    if confirmation != new_password:
        flash("New password does not match confirmation")
        return redirect(request.referrer)
    
    new_hash = generate_password_hash(new_password)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET hash = ? WHERE id = ?", (new_hash, session["user_id"]))

    return redirect("/")

        
        

@app.route('/delete-account', methods=["POST"])
def delete_account():

    password = request.form.get("password")
    with get_db() as conn:
        cur = conn.cursor()        
        cur.execute("SELECT hash FROM users WHERE id = ?", (session["user_id"],))
        hash = cur.fetchone()["hash"]
    
        print(password)
        if not password:
            flash("no password bug???")
            return redirect(request.referrer)
        if not check_password_hash(hash, password):

            flash("Incorrect Password")
            return redirect(request.referrer)
        cur.execute("DELETE FROM users WHERE id = ?", (session["user_id"],))
        session.clear()
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/dev/reset-db')
def dev_reset_db():
    """Dangerous: re-run init_db.py to recreate schema. Protected by a simple secret param for dev use only."""
    secret = request.args.get('secret')
    if secret != 'reset-now-please':
        return ('Forbidden', 403)

    init_script = os.path.join(APP_DIR, 'init_db.py')
    os.system(f'python "{init_script}"')
    return ('DB reset', 200)


if __name__ == '__main__':
    # Use debug=True for auto-reload during development
    app.run(debug=True)