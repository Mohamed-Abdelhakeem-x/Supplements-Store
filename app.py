import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from Prime_Supplements import app, init_db

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=3000)