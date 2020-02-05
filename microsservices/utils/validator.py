from rest_framework import status
from rest_framework.response import Response


class ValidatorData:
    def validated_data(self, validated_fields):
        data = self.request.data
        if len(data) == 0:
            return Response(
                {
                    "success": False,
                    "msg": "There is no fields"
                }, status=status.HTTP_400_BAD_REQUEST
            )

        validator = [f for f in validated_fields if f not in [key for key in data.keys()]]

        if len(validator) > 0:
            return Response(
                {
                    'success': False,
                    'msg': 'There is not fields',
                    'fields_required': validator
                }, status=status.HTTP_400_BAD_REQUEST
            )

        if 'slug' in data:
            return Response(
                {
                    "success": False,
                    "msg": "Slug field is not editable"
                }, status=status.HTTP_403_FORBIDDEN
            )

        empty_fields = [key for key, value in data.items() if key in validated_fields and value == '']

        if len(empty_fields) != 0:
            return Response(
                {
                    'success': False,
                    'msg': 'fields are empty',
                    'fields': empty_fields
                }, status=status.HTTP_400_BAD_REQUEST

            )

        return 1
