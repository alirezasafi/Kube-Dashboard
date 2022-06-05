import magic
from django.template.defaultfilters import filesizeformat
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FileValidator(object):
    error_messages = {
        "max_size": "Ensure this file size is not greater than %(max_size)s. your file size is %(size)s.",
        "content_type": "Files of type %(content_type)s are not supported."
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                "max_size": filesizeformat(self.max_size),
                "size": filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['max_size'] % params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)
            if content_type not in self.content_types:
                params = {"content_type": content_type}
                raise ValidationError(self.error_messages['content_type'] % params)

    def __eq__(self, other):
        return (
            isinstance(other, FileValidator) and
            self.max_size == other.max_size and
            self.min_size == other.min_size and
            self.content_types == other.content_types
        )


class LoginSerializer(serializers.Serializer):
    token = serializers.CharField(allow_null=False, allow_blank=False)

    # config = serializers.FileField(max_length=200, allow_empty_file=True, allow_null=True, validators=[
    #     FileValidator(content_types=["application/x-yaml", "text/yaml", "text/plain"])
    # ])

    # def validate(self, attrs):
    #     if not attrs.get('token') and not attrs.get('config'):
    #         raise ValidationError("Must include at least one field")
    #     return super(LoginSerializer, self).validate(attrs)
