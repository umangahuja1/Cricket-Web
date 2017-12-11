from flask import Flask, render_template
from schedule import Schedule

app = Flask('__name__')

match = Schedule()


@app.route('/')
def index():
    return render_template('index.html', match=match)


if __name__ == '__main__':
    app.run(debug=True)
