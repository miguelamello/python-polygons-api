import re

class Utils:
  def isEmail(email):
    # Email format validation using regular expressions
    #if len(email):
      if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email):
        return False

    return True

  def toNumber(string):
    # Use regular expression to remove non-digit characters
    if len(string):
      return re.sub(r"[^\d]+", "", string)