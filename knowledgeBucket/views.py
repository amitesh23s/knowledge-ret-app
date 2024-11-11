import os
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .utils import Embeddings, Context, InvokeModel
from .constants import parameters
EMBEDDINGS_MODEL_ID = os.environ.get("EMBEDDINGS_MODEL_ID")
QA_MODEL_ID = os.environ.get("QA_MODEL_ID")

class AskAPrompt(View):
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        embeddings_object = Embeddings(EMBEDDINGS_MODEL_ID)

        embedding = embeddings_object.generate_embeddings(body["prompt_data"])

        context_object = Context()
        context = context_object.fetch_context(embedding)

        invoke_object = InvokeModel(QA_MODEL_ID)
        prompt_data = f"""Answer the question based only on the information provided between ## and give step by step guide.
        #
        {context}
        #
        Question: {body["prompt_data"]}
        Answer:"""
        answer = invoke_object(prompt_data, parameters)


class AddDocuments(View):
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        build_chunks_object = BuildChunks()
        chunks = build_chunks_object.build_chunks(file)

        embedding_object = Embeddings()
        for chunk in chunks:
            embedding_object.store_embeddings(chunk)

        return HttpResponse("Success", status=200)


# Create your views here.
