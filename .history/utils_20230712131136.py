import re

class Utils:
  def isEmail(email):
    # Email format validation using regular expressions
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email):
      return False

    return True

  def toNumber(number):
    # Use regular expression to remove non-digit characters
    number_string = re.sub(r"[^\d]+", "", number_string)