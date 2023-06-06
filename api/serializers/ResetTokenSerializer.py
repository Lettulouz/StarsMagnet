from django.http import HttpResponse
from rest_framework import serializers
from api.models import Safety_Words
from api.models import Companies
from django.db.models import Q
import json
from ..utils.generate_token import generate_token
from ..utils.generate_safe_words import generate_safe_words
from ..utils.generate_safe_words import make_dictio
from .SafeWordsSerializer import SafeWordsSerializer


class ResetTokenSerializer(serializers.Serializer):

    class Meta:
        fields = ('words', 'user')

    def check_words(self, data):
        user = data.get("user", None)
        words_input = data.get("words", None)

        queries = Q()
        for i, value in enumerate(words_input, start=1):
            query = "word" + str(i)
            queries &= Q(**{query: value})
            if i == 10:
                break

        matched_object = Safety_Words.objects.filter(queries).first()
        if not matched_object:
            return "duży błąd"

        if matched_object.user.email != user and matched_object.user.username != user:
            return "mniejszy błąd"

        token = generate_token()

        json_response = generate_safe_words()

        words = make_dictio(json_response)

        serializer = SafeWordsSerializer(data=words, context={'user_id': matched_object.id})

        if serializer.is_valid():
            serializer.save()
        else:
            return "Wielbłąd"

        if matched_object:
            return {'words': json_response, 'token': token}

        return "No matching object found"

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass