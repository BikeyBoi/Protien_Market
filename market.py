from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    barcode = db.Column(db.String(12), nullable=False)  # Remove unique=True
    description = db.Column(db.String(1024), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()

    return render_template('market.html', items=items)

# Create and add items to the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # Create a list of item instances 
        items = [
            Item(name="Protein Bar", price=2.0, barcode="321345", description="A healthy protein bar."),
            Item(name="Protein Shake", price=50.0, barcode="98893548", description="A nutritious protein shake."),
            Item(name="Protein Pancake", price=10.0, barcode="3554897624", description="Delicious protein pancakes.")
        ]
        # if items are already in the db we don't need to add them again that's why db.session.add_all() and db.session.commit() have been commented out
        # Add the list of items to the database session
        #db.session.add_all(items)

        # Commit the changes to the database
        #db.session.commit()

    app.run()