import os

from flask import Flask

from util import json_response
from routes import routes

app = Flask(__name__)
routes(app)
port = os.getenv("PORT", 3002) # 端口



@app.errorhandler(Exception)
def error(e):
	r = {
		"err": "error happened",
		"err_type": type(e).__name__,
		"err_msg": e.args
	}
	return json_response(500, r)


if __name__ == '__main__':
	# Run the app, listening on all IPs with our chosen port number
	app.config['JSON_AS_ASCII'] = False
	app.run(debug=True ,port=port) # 调试用
	# app.run(host='0.0.0.0', port=port) # 实际部署请用这个