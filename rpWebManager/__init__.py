from flask import Flask, render_template, request, current_app
from .utils import get_instance_folder_path

def create_app():
    app = Flask(
        __name__,
        instance_path=get_instance_folder_path(),
        instance_relative_config=False,
        template_folder="templates"
    )
    
    @app.route("/")
    def home():
        return render_template('index.html')    


    @app.errorhandler(404)
    def page_not_found(error):
        current_app.logger.error("Page not found: %s", (request.path, error))
        return render_template("404.html"), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        current_app.logger.error("Server Error: %s", (error))
        return render_template("500.html"), 500


    @app.errorhandler(Exception)
    def unhandled_exception(error):
        current_app.logger.error("Unhandled Exception: %s", (error))
        return render_template("500.html"), 500    

    with app.app_context():

        from .monitoring.monitoring import monitoring_bp
        from .bios.bios import bios_bp

        app.register_blueprint(monitoring_bp, url_prefix="/monitoring")
        app.register_blueprint(bios_bp, url_prefix="/bios")    

        return app