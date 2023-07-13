import re

class Utils:
  def isEmail(email):
    # Email format validation using regular expressions
    if not re.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@([A-Za-z0-9])*[A-Za-z]\.[A-Za-z]', email):
      return False

    return True