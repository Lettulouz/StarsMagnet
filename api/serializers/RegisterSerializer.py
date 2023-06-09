from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from api.models import Companies

User = get_user_model()


def unique_username(value):
    """
    Validator to check if username is unique,
    raise error if not.
    :param value: username
    """
    if User.objects.filter(username=value).exists() or Companies.objects.filter(username=value).exists():
        raise serializers.ValidationError("This field must be unique.")


def unique_email(value):
    """
    Validator to check if email is unique,
    raise error if not.
    :param value: email
    """
    if User.objects.filter(email=value).exists() or Companies.objects.filter(email=value).exists():
        raise serializers.ValidationError('This field must be unique.')


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for register a new user.
    """
    email = serializers.EmailField(
        required=True,
        validators=[unique_email]
    )

    username = serializers.CharField(
        required=True,
        validators=[unique_username]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """
        Metadata for RegisterSerializer.
        Contains used model, fields and extra params.
        """
        model = User
        fields = ('username', 'password', 'confirm_password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attr):
        """
        Method for additional validations, check if passwords are the same.
        :param attr: pre-cleaned data.
        :return: cleaned data
        """
        if attr['password'] != attr['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords must be the same"})
        return attr

    def save(self):
        """
        Method to save new user in database.
        :return: user object.
        """

        user = User.objects.create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )

        user.set_password(self.validated_data['password'])
        user.save()
        return user
