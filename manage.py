import os
from file_upload_endpoint import create_app

env = 'default'
if 'FLASK_ENV' in os.environ:
    env = os.getenv('FLASK_ENV')

app = create_app(env)

if 'PYCHARM_HOSTED' in os.environ:
    app.run(host='0.0.0.0', port=9001, debug=True, use_debugger=False, use_reloader=False)
