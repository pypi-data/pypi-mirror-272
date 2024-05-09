import unittest

from switcore.ui.collection_entry import CollectionEntry, TextSection
from switcore.ui.image import Image
from switcore.ui.text_paragraph import TextParagraph


class CollectionEntryTest(unittest.TestCase):

    def test_valid_collection_entry01(self):
        collection_entry: CollectionEntry = CollectionEntry(
            text_sections=[
                TextSection(
                    text=TextParagraph(
                        content="test content"
                    ),
                    metadata_items=[
                        Image(image_url="./assets/builder_logo.png")
                    ])
            ]
        )
        expected: dict = {
            'type': 'collection_entry',
            'draggable': False,
            'text_sections': [
                {
                    'metadata_items': [
                        {
                            'image_url': './assets/builder_logo.png',
                            'type': 'image'
                        }
                    ],
                    'text': {
                        'content': 'test content',
                        'markdown': False,
                        'type': 'text'}
                }
            ],
            'vertical_alignment': 'top'
        }

        # print(json.dumps(expected, indent=4))
        self.assertEqual(expected, collection_entry.dict(exclude_none=True))

    def test_valid_collection_entry02(self):
        collection_entry: CollectionEntry = CollectionEntry(
            start_section=Image(
                image_url="./assets/builder_logo.png",
            ),
            text_sections=[
                TextSection(
                    text=TextParagraph(
                        content="test content"
                    ),
                )
            ]
        )
        expected: dict = {
            'type': 'collection_entry',
            'start_section': {
                'image_url': './assets/builder_logo.png',
                'type': 'image'
            },
            'draggable': False,
            'text_sections': [
                {
                    'text': {
                        'content': 'test content',
                        'markdown': False,
                        'type': 'text'}
                }
            ],
            'vertical_alignment': 'top'
        }

        # print(json.dumps(expected, indent=4))
        self.assertEqual(expected, collection_entry.dict(exclude_none=True))
