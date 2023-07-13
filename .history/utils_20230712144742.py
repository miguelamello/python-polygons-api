import re

class Utils:
  # Email format validation using regular expressions
  def isEmail(email):
    if len(email):
      if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", email):
        return False

    return True

  # Use regular expression to remove non-digit characters
  def toNumber(string):
    if len(string):
      return re.sub(r"[^\d]+", "", string)

  # Verify required fields
  # # Exit if any of the them are missing or empty
  def validateFields(data):
    pass