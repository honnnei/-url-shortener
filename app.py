from flask import (Flask, render_template, url_for, request, redirect)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
# 3 /// - relative path, 4 //// - absolute path:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_test.db'
db = SQLAlchemy(app)
# 'SQLALCHEMY_DATABASE_URI'

class YourUrl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(200), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # def __repr__(self):
    #     return '<YourUrl %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        link_long_url = request.form['long_url']
        link_short_url = request.form['short_url']
        new_url = YourUrl(long_url = link_long_url, short_url = link_short_url)
        try:
            db.session.add(new_url)
            db.session.commit()
            # return redirect('/')
            return "this was posted"
        except:
            return 'There was an issue adding your task'
    else:
        all_urls = YourUrl.query.order_by(YourUrl.date_created).all()
        return render_template('index.html', all_the_urls=all_urls)

        # all_urls=all_urls
@app.route('/link/<short>', methods=['GET']) 
def get_user_url(short):
    destination = YourUrl.query.filter_by(short_url=short).first()
    # url_destination = YourUrl.query.get_or_404(short_url)
    try:
        if 'www.' in destination.long_url:
             return redirect(f'https://{destination.long_url}/')
        else:
            return redirect(f'https://www.{destination.long_url}/')
    except:
        return 'There was a problem opening link that task'


# @app.route('/link/', methods=['GET']) 
# def get_user_url():
#     # url_destination = YourUrl.query.get_or_404(short_link)
#     # print(url_destination.long_url)
#     try:
#         return redirect('https://www.facebook.com/')
#     except:
#         return 'there was an issue'

@app.route('/delete/<int:id>')
def delete(id):
    url_to_delete = YourUrl.query.get_or_404(id)

    try:
        db.session.delete(url_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    url_to_update = YourUrl.query.get_or_404(id)
    if request.method == 'POST':
        url_to_update.short_url = request.form['short_url']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
            
    else:
        return render_template('update.html', url_link=url_to_update)


    try:
        db.session.put(url_to_update)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


if __name__ == "__main__":
    app.run(debug=True)
