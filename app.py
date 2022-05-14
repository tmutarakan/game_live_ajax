from flask import Flask, render_template, request
import json
from game_of_live import GameOfLife
from project.forms import ParameterForm
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['get', 'post'])
def index():
    GameOfLife()
    if request.method == 'POST':
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        GameOfLife(width=width, height=height)

    return render_template(
        'index.html',
        form=ParameterForm()
    )


@app.route('/live')
def live():
    game = GameOfLife()
    if game.counter:
        game.form_new_generation()
    game.counter += 1
    return render_template(
        'live.html',
        game=game
    )


@app.route('/next_gen')
def next_gen():
    """Отправляет данные в формате JSON-строки в ответ на запрос по url"""
    game = GameOfLife()
    if game.counter:
        game.form_new_generation()
    game.counter += 1
    return json.dumps(game.get_worlds_dict())


@app.route('/', methods=['get', 'post'])
def get_len():
    name = request.form.get('width')
    return json.dumps({'len', len(name)})


def create_app():
    return app


module = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
