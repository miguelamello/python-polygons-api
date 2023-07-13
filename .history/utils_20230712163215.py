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
        if data['name'] == None:
            return {'error': 'Name is required'}, 400

        if data['email'] == None:
            return {'error': 'Email is required'}, 400

        if data['phone'] == None:
            return {'error': 'Phone is required'}, 400

        if len(data['name'].strip()) == 0:
            return {'error': 'Name can not be empty'}, 400

        if len(data['email'].strip()) == 0:
            return {'error': 'Email can not be empty'}, 400

        if len(data['phone'].strip()) == 0:
            return {'error': 'Phone can not be empty'}, 400

        return True

    # Format provider payload data to expected syntax
    def formatProviderPayload(data):
        if data['name']:
            data['name'] = data['name'].strip().title()

        if data['email']:
            data['email'] = data['email'].strip().lower()

        if data['price']:
            data['phone'] = Utils.toNumber(data['price'].strip())

        if data.get('language'):
            data['language'] = data.get('language').strip().title()

        if data.get('currency'):
            data['currency'] = data.get('currency').strip().upper()

        return data

    # Verify required service area fields in payload data
    def validateServiceAreaFields(data):
        if data['name'] == None:
            return {'error': 'Name is required'}, 400

        if data['price'] == None:
            return {'error': 'Price is required'}, 400

        if data['gespos'] == None:
            return {'error': 'Geoposition is required'}, 400

        if len(data['name'].strip()) == 0:
            return {'error': 'Name can not be empty'}, 400

        if len(data['price'].strip()) == 0:
            return {'error': 'Price can not be empty'}, 400

        if len(data['geopos'].strip()) == 0:
            return {'error': 'Geoposition can not be empty'}, 400

        return True

    # Format service area payload data to expected syntax
    def formatServiceAreaPayload(data):
        if data['name']:
            data['name'] = data['name'].title()

        if data['price']:
            data['price'] = Utils.toNumber(data['price'])
            data['price'] = int(data['price']) / 100
            data['price'] = "{:.2f}".format(data['price'])

        return data