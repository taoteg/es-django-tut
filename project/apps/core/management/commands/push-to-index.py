# ADDED.
from elasticsearch.client import IndicesClient
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Student


class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        # TEST COMMAND WORKS.
        print('Populating elastic search index...')
        self.recreate_index()

    def recreate_index(self):
        indices_client = IndicesClient(client=settings.ES_CLIENT)

        index_name = Student._meta.es_index_name

        if indices_client.exists(index_name):
            indices_client.delete(index=index_name)

        indices_client.create(index=index_name)

        indices_client.put_mapping(
            doc_type=Student._meta.es_type_name,
            body=Student._meta.es_mapping,
            index=index_name
        )
