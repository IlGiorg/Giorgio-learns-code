from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///filaments.db'
app.config['SECRET_KEY'] = 'supersecretkey'  # required for sessions
db = SQLAlchemy(app)

# Database model
class Filament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    ftype = db.Column(db.String(50), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Filament {self.color}>"

@app.before_request
def create_tables():
    db.create_all()

# Homepage - read-only or with graphs
@app.route('/')
def index():
    filaments = Filament.query.all()

    # Data for graphs
    type_counts = {}
    type_weights = {}
    for f in filaments:
        type_counts[f.ftype] = type_counts.get(f.ftype, 0) + 1
        type_weights[f.ftype] = type_weights.get(f.ftype, 0) + f.weight

    return render_template('index.html', filaments=filaments,
                           type_counts=type_counts, type_weights=type_weights,
                           authenticated=session.get('authenticated', False))

# Login for modification
@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == 'pass':
        session['authenticated'] = True
    return redirect(url_for('index'))

# Logout
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

# Add new filament
@app.route('/add', methods=['POST'])
def add():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    color = request.form['color']
    weight = float(request.form['weight'])
    ftype = request.form['ftype']
    manufacturer = request.form['manufacturer']
    new_filament = Filament(color=color, weight=weight, ftype=ftype, manufacturer=manufacturer)
    db.session.add(new_filament)
    db.session.commit()
    return redirect(url_for('index'))

# Delete filament
@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    filament = Filament.query.get_or_404(id)
    db.session.delete(filament)
    db.session.commit()
    return redirect(url_for('index'))

# Edit filament
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    filament = Filament.query.get_or_404(id)
    if request.method == 'POST':
        filament.color = request.form['color']
        filament.ftype = request.form['ftype']
        filament.manufacturer = request.form['manufacturer']

        # Remove weight if requested
        remove_weight = request.form.get('remove_weight')
        if remove_weight:
            filament.weight = max(filament.weight - float(remove_weight), 0)

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', filament=filament)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
