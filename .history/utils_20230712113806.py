import re

class Utils:
  def isEmail():
    # Email format validation using regular expressions
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$', email):
      return {'error': 'Invalid email format'}, 400

    if not re.match(r'^[\w.-]+@([\w\.-]+\.)*[a-zA-Z]+\.[a-zA-Z]+$', email):
      return {'error2': 'Invalid email format'}, 400