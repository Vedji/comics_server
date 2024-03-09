
from flask import Flask
from flask_jwt_extended import JWTManager

import api_v1.init_site_gui_v1
import api_v2.init_site_gui_v2

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = 'Ponkratov-Comics-server-secret-key'
jwt = JWTManager(app)


api_v1.init_site_gui_v1.init(app, jwt)       # Init gui v1
# api_v2.init_site_gui_v2.init(app, jwt)     # Init gui v2


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

