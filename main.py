from flask import Flask, render_template
from flask_login import current_user
from data.db_session import global_init, create_session

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home_page.html', current_user=current_user)


if __name__ == '__main__':
    global_init("db/project.sqlite")
    app.run()
