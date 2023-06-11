from rest_framework import serializers
from api.models import Safety_Words
from django.db.models import Q
from ..utils.generate_token import generate_token
from ..utils.generate_safe_words import generate_safe_words
from ..utils.generate_safe_words import make_dictio
from .SafeWordsSerializer import SafeWordsSerializer


class ResetTokenSerializer(serializers.Serializer):
    """
    Serializer to reset token
    """

    class Meta:
        """
        Metadata for ResetTokenSerializer.
        Contains fields
        """
        fields = ('words', 'user')

    def check_words(self, data):
        """
        Method to reset the company's token if given safe words in the correct order
        :param data: input data
        :return: new token, secure words and token reset process information
        """
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
            raise serializers.ValidationError({"data": "Invalid data. Error code A01"})

        if matched_object.user.email != user and matched_object.user.username != user:
            raise serializers.ValidationError({"data": "Invalid data. Error code A02"})

        token = generate_token()

        json_response = generate_safe_words()

        words = make_dictio(json_response)

        serializer = SafeWordsSerializer(data=words, context={'user_id': matched_object.id})

        if serializer.is_valid():
            serializer.save()
        else:
            raise serializers.ValidationError({"data": "An error has occurred, no data has been changed"})

        if matched_object:
            return {'responseWords': json_response, 'token': token,
                    'response': "Your token and secure words was successfully changed" }

        raise serializers.ValidationError({"data": "Invalid data. Error code A03"})

