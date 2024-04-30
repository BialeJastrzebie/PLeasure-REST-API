"""
Serializers for the user API view
"""
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers

from friendship.serializers import UserFriendsSerializer


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user object"""
    relations = UserFriendsSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name',
                  'first_name', 'last_name', 'relations']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def _get_or_create_relations(self, relations, user):
        auth_user = self.context['request'].user
        for relation in relations:
            relation_obj, create = UserFriendsSerializer().get_or_create(
                user=auth_user,
                **relation,
            )
            user.relations.add(relation_obj)

    def create(self, validated_data):
        """create and return a user with encrypted password"""
        relations = validated_data.pop('relations', [])
        user = get_user_model().objects.create_user(**validated_data)
        self._get_or_create_relations(relations, user)

        return user

    def update(self, instance, validated_data):
        """updated and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """serializer for user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
