from rpWebManager import create_app
from flask_debugtoolbar import DebugToolbarExtension
from rpWebManager.config import configure_app

app = create_app()

configure_app(app)
toolbar = DebugToolbarExtension(app)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8888, debug=True)