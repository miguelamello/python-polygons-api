import re

class Utils:
  def isEmail(email):
    # Email format validation using regular expressions
    if not re.match(r'^[\w.-]+@[\w\.-]+\.)*[a-zA-Z]+\.[a-zA-Z]+$', email):
      return False

    if not re.match(r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]+$', email):
      return False

    return True