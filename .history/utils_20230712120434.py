import re

class Utils:
  def isEmail(email):
    # Email format validation using regular expressions
    if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
      return False

    return True