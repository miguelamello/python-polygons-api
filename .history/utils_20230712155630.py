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

    # Verify required provider fields in payload data
    def validateProviderFields(data):
        if data.get('name') == None:
            return {'error': 'Name is required'}, 400

        if data.get('email') == None:
            return {'error': 'Email is required'}, 400

        if data.get('phone') == None:
            return {'error': 'Phone is required'}, 400

        if len(data.get('name').strip()) == 0:
            return {'error': 'Name can not be empty'}, 400

        if len(data.get('email').strip()) == 0:
            return {'error': 'Email can not be empty'}, 400

        if len(data.get('phone').strip()) == 0:
            return {'error': 'Phone can not be empty'}, 400

        return True

    # Format provider payload data to expected syntax
    def formatProviderPayload(data):
        if data.get('name'):
            data['name'] = data.get('name').strip().title()
            name = data.get('name')

        if data.get('email'):
            data['email'] = data.get('email').strip().lower()
            email = data.get('email')

        if data.get('phone'):
            data['phone'] = Utils.toNumber(data.get('phone').strip())
            phone = data.get('phone')

        if data.get('language'):
            data['language'] = data.get('language').strip().title()

        if data.get('currency'):
            data['currency'] = data.get('currency').strip().upper()

        return data
