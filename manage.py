import os, unittest
from file_upload_endpoint import create_app

app = create_app(os.getenv('FLASK_ENV') or 'default')

if 'PYCHARM_HOSTED' in os.environ:
    app.run(host='0.0.0.0', port=9001, debug=True, use_debugger=False, use_reloader=False)

@app.cli.command()
def test():
    """Run integration tests."""
    tests = unittest.TestLoader().discover(os.path.join(os.path.dirname(__file__), 'tests'))
    unittest.TextTestRunner(verbosity=2).run(tests)
