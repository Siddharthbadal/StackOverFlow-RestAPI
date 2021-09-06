from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Questions
from .serializer import QuestionsSerializer
import requests
from bs4 import BeautifulSoup
import json

class QuestionAPI(viewsets.ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer



def scrapedQuestions(request):
    try:
        response = requests.get("https://stackoverflow.com/questions")
        # https://stackoverflow.com/questions?tab=newest&page=2

        soup = BeautifulSoup(response.text, "html.parser")

        questions = soup.select(".question-summary")
        for que in questions:
            q = que.select_one('.question-hyperlink').getText()
            vote_count = que.select_one('.vote-count-post').getText()
            views_on_post = que.select_one('.views').attrs['title']
            tags = [i.getText() for i in (que.select('.post-tag'))]

            question = Questions()
            question.question = q
            question.vote_count = vote_count
            question.views = views_on_post
            question.tags = tags

            question.save()
        return HttpResponse("Data fetched from StackOverFlow!")

    except Exception:
        return HttpResponse("Data not fetched!")



