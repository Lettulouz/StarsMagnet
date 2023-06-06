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


class ResetTokenSerializer(serializers.ModelSerializer):

    def check_words(self, data):
        user = data.get("user", None)
        words = data.get("words", None)

        data_json = json.loads(words)

        queries = Q()
        for i, value in enumerate(data_json, start=1):
            query = "word" + str(i)
            queries &= Q(**{query: value})
            if i == 10:
                break

        matched_object = Safety_Words.objects.filter(queries).first()
        if not matched_object:
            return "duży błąd"

        if matched_object.user.email != user and matched_object.user.username != user:
            pass # tu błąd

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
