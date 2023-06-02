from rest_framework import serializers
from api.models import Safety_Words


class SafeWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Safety_Words
        fields = ('word1',
                  'word2',
                  'word3',
                  'word4',
                  'word5',
                  'word6',
                  'word7',
                  'word8',
                  'word9',
                  'word10')

    def save(self):
        safe_word = Safety_Words.objects.create(
            user_id=self.context['id'],
            word1=self.validated_data['word1'],
            word2=self.validated_data['word2'],
            word3=self.validated_data['word3'],
            word4=self.validated_data['word4'],
            word5=self.validated_data['word5'],
            word6=self.validated_data['word6'],
            word7=self.validated_data['word7'],
            word8=self.validated_data['word8'],
            word9=self.validated_data['word9'],
            word10=self.validated_data['word10']
        )

        safe_word.save()
        return safe_word
