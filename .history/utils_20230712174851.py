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

        if data['phone']:
            data['phone'] = Utils.toNumber(data['phone'].strip())

        if data['language']:
            data['language'] = data['language'].strip().title()

        if data['currency']:
            data['currency'] = data['currency'].strip().upper()

        return data

    # Verify required service area fields in payload data
    def validateServiceAreaFields(data):
        if data.get('name') == None:
            return {'error': 'Name is required'}, 400

        if data.get('price') == None:
            return {'error': 'Price is required'}, 400

        if data.get('geopos') == None:
            return {'error': 'Geoposition is required'}, 400

        if data.get('geopos', {}).get('type') != None:
            if data.get('geopos', {}).get('type') != 'Point':
              return {'error': 'Geoposition Type should be Point'}, 400

        if data.get('geopos', {}).get('coordinates') == None:
            return {'error': 'Geoposition Coordinates is required'}, 400

        if data.get('provider') == None:
            return {'error': 'Provider ID is required'}, 400

        if len(data['name'].strip()) == 0:
            return {'error': 'Name can not be empty'}, 400

        if len(str(data['price']).strip()) == 0:
            return {'error': 'Price can not be empty'}, 400

        if len(data['geopos']) == 0:
            return {'error': 'Geoposition can not be empty'}, 400

        if len(data['geopos']['coordinates']) != 2:
            return {'error': 'Geoposition Coordinates should be latitude and longitude'}, 400

        if len(data['provider'].strip()) != 24:
            return {'error': 'Provider should be an ID of 24 characters of size'}, 400

        return True

    # Format service area payload data to expected syntax
    def formatServiceAreaPayload(data):
        if data['name']:
            data['name'] = data['name'].title()

        if data['price']:
            data['price'] = Utils.toNumber(str(data['price']))
            data['price'] = float(data['price']) / 100
            data['price'] = "{:.2f}".format(data['price'])

        return data
