import os
from file_upload_endpoint import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')

if 'PYCHARM_HOSTED' in os.environ:
    app.run(host='0.0.0.0', port=9001, debug=True, use_debugger=False, use_reloader=False)
