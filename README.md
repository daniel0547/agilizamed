# agilizamed

## Installation

Install with pip:

`$ pip install -r requirements.txt`

set your openai api-key in app/settings.py


## Run flask for production

** Run with gunicorn **

`$ gunicorn -w 4 -b 127.0.0.1:5000 run:app`

-w : number of worker
-b : Socket to bind

