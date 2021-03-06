from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
  return render_template('home.html')

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
