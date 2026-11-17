import psycopg2
from flask import Flask, render_template

from config import Config
from routes.planes import bp as planes_bp
from routes.entrenadores import bp as entrenadores_bp
from routes.miembros import bp as miembros_bp
from routes.clases import bp as clases_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(planes_bp)
    app.register_blueprint(entrenadores_bp)
    app.register_blueprint(miembros_bp)
    app.register_blueprint(clases_bp)

    @app.route("/")
    def inicio():
        return render_template("index.html")

    @app.errorhandler(psycopg2.OperationalError)
    def error_conexion(exc):
        return render_template("error_db.html"), 500

    @app.errorhandler(404)
    def no_encontrado(exc):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
