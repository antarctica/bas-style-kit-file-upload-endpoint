import os
from dotenv import load_dotenv

from file_upload_endpoint import create_app

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

env = 'default'
if 'FLASK_ENV' in os.environ:
    env = os.getenv('FLASK_ENV')

app = create_app(env)

if 'PYCHARM_HOSTED' in os.environ:
    app.run(host='0.0.0.0', port=9000, debug=True, use_debugger=False, use_reloader=False)
