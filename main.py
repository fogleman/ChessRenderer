from flask import Flask, request, Response
from renderer import Renderer
import StringIO

app = Flask(__name__)

renderer = Renderer()

@app.route('/index.png')
def index():
    fen = request.args.get('fen')
    fen = fen or 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    response = StringIO.StringIO()
    surface = renderer.render(fen)
    surface.write_to_png(response)
    return Response(response=response.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
