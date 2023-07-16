import re
from bson import ObjectId

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

        if len(str(data['name']).strip()) == 0:
            return {'error': 'Name can not be empty'}, 400

        if len(str(data['email']).strip()) == 0:
            return {'error': 'Email can not be empty'}, 400

        if len(str(data['phone']).strip()) == 0:
            return {'error': 'Phone can not be empty'}, 400

        return True

    # Format provider payload data to expected syntax
    def formatProviderPayload(data):
        if data['name']:
            data['name'] = str(data['name']).strip().title()

        if data['email']:
            data['email'] = str(data['email']).strip().lower()

        if data['phone']:
            data['phone'] = Utils.toNumber(str(data['phone']).strip())

        if data['language']:
            data['language'] = str(data['language']).strip().title()

        if data['currency']:
            data['currency'] = str(data['currency']).strip().upper()

        return data

    # Verify required service area fields in payload data
    def validateServiceAreaFields(data):
        if data['name'] == None:
            return {'error': 'Name is required'}, 400

        if data['price'] == None:
            return {'error': 'Price is required'}, 400

        if data['vertices'] == None:
            return {'error': 'Vertices is required'}, 400

        if data['vertices']['type'] == None:
            data['vertices']['type'] = 'Polygon'
        else:
            if data['vertices']['type'] != 'Polygon':
              return {'error': 'Vertices should be of type Polygon'}, 400
          

        if data['vertices']['coordinates'] == None:
            return {'error': 'Geo coordinates are required'}, 400
        else:
            if len(data['vertices']['coordinates'][0]) < 3:
                return {'error': 'At least 3 geo coordinates are required'}, 400

        if data['provider'] == None:
            return {'error': 'Provider ID is required'}, 400

        if len(str(data['name']).strip()) == 0:
            return {'error': 'Name can not be empty'}, 400

        if len(str(data['price']).strip()) == 0:
            return {'error': 'Price can not be empty'}, 400

        # Verify if price is a valid float number. Ex: 10.57
        # Only a dot is allowed as decimal separator
        try:
          if float(data['price']):
              pass
        except ValueError:
            return {'error': 'Price should be a valid float number'}, 400

        if len(data['vertices']) == 0:
            return {'error': 'Vertices can not be empty'}, 400

        if len(str(data['provider']).strip()) != 24:
            return {'error': 'Provider should be an ID of 24 characters in length'}, 400

        return True

    # Format service area payload data to expected syntax
    def formatServiceAreaPayload(data):
        # Capitalize name
        if data['name']:
            data['name'] = data['name'].title()

        # Take only 2 decimal digits from price
        if data['price']:
            data['price'] = float(str(data['price'])[:5])
            
        # Insert missing Geoposition Type 
        if data['vertices']['type'] == None:
            data['vertices']['type'] = "Polygon"
            
        # Format coordinates to 4 decimal digits 
        # Return an erro if coordinates are not valid
        for i in range(len(data['vertices']['coordinates'][0])):
            coordinate = data['vertices']['coordinates'][0][i]

            try: 
                lng = str(coordinate[0])
                lng = lng[:lng.index('.') + 5]
                data['vertices']['coordinates'][0][i][0] = float(lng)
            except:
                return None, 'Longitude must be a valid geo coordinate: Ex: -73.9889'

            try:
                lat = str(coordinate[1])
                lat = lat[:lat.index('.') + 5]
                data['vertices']['coordinates'][0][i][1] = float(lat)
            except:
                return None, 'Latitude must be a valid geo coordinate: Ex: 40.7306'

        # Ensure the first and last points are the same to close the polygon
        if data['vertices']['coordinates']:
            first_point = data['vertices']['coordinates'][0][0]
            last_point = data['vertices']['coordinates'][0][-1]
            if first_point != last_point:
                data['vertices']['coordinates'][0].append(first_point)
                
        # Format provider id to ObjectId
        if data['provider']:
            data['provider'] = ObjectId(data['provider'])

        return data, None
