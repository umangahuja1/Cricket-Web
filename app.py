from flask import Flask, render_template
from schedule import Schedule

app = Flask('__name__')


@app.route('/')
def index():
    match = Schedule()
    return render_template('index.html', match=match)


if __name__ == '__main__':
    app.run(debug=True)
