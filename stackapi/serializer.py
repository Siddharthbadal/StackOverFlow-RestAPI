from rest_framework import serializers
from .models import Questions



class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('question', 'vote_count','views', 'tags')
