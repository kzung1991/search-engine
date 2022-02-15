from flask import Flask, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from sqlalchemy import or_, and_ # for quering multiple columns
from sqlalchemy import desc # Order the datetime, default is ascending order

app = Flask(__name__)

db_name = 'database.db'
# Perform a connection to the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = '9RNZyYBmGv0uR6r4xhSC9XKUv5s6Z6nb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# Set a veriable for query purposes in SQLAlchemy
db = SQLAlchemy(app)

# Create a Class for the table 'vnexpress' in the database
# and identify all columns by name and datatype
class Vnexpress(db.Model):
    __tablename__ = 'vnexpress'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Text)
    title = db.Column(db.Text, unique=True)
    link = db.Column(db.Text)
    description = db.Column(db.Text)

class SearchForm(FlaskForm):
    search_field = StringField('Enter any word you like in English:', validators=[DataRequired()])
    submit = SubmitField('Search')

# Routes
@app.route("/", methods=['GET', 'POST'])
def index():
    form = SearchForm()
    table = Vnexpress.query

    if form.validate_on_submit():
        word = form.search_field.data.lower()
        table = table.filter(or_(Vnexpress.description.like('%' + word + '%'), \
        Vnexpress.title.like('%' + word + '%'))).order_by(desc(Vnexpress.date)).all()

    return render_template('index.html', table=table, form=form)

if __name__ == '__main__':
    app.run(debug=True)
