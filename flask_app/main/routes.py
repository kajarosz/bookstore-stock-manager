from flask import jsonify, render_template

def configure_routes(app):

    @app.route('/random_songs/<int:number>', methods=['GET'])
    def random_songs(number):
        pass