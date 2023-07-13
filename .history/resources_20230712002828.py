class ProviderResource(Resource):
    def get(self, provider_id):
        provider = Provider.objects.get(id=provider_id)
        return provider.to_json()

    def post(self):
        data = request.get_json()
        try:
            provider = Provider(**data)
            provider.save()
            return {'message': 'Provider created successfully', 'id': str(provider.id)}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def put(self, provider_id):
        data = request.get_json()
        try:
            Provider.objects(id=provider_id).update_one(**data)
            return {'message': 'Provider updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def delete(self, provider_id):
        Provider.objects(id=provider_id).delete()
        return {'message': 'Provider deleted successfully'}


class ServiceAreaResource(Resource):
    def get(self, service_area_id):
        service_area = ServiceArea.objects.get(id=service_area_id)
        return service_area.to_json()

    def post(self):
        data = request.get_json()
        try:
            service_area = ServiceArea(**data)
            service_area.save()
            return {'message': 'ServiceArea created successfully', 'id': str(service_area.id)}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def put(self, service_area_id):
        data = request.get_json()
        try:
            ServiceArea.objects(id=service_area_id).update_one(**data)
            return {'message': 'ServiceArea updated successfully'}
        except ValidationError as e:
            return {'error': str(e)}, 400

    def delete(self, service_area_id):
        ServiceArea.objects(id=service_area_id).delete()
        return {'message': 'ServiceArea deleted successfully'}


api.add_resource(ProviderResource, '/providers', '/providers/<string:provider_id>')
api.add_resource(ServiceAreaResource, '/service-areas', '/service-areas/<string:service_area_id>')
