import unittest

from switcore.ui.info_card import InfoCard
from switcore.ui.item import Item
from switcore.ui.text_paragraph import TextParagraph


class InfoCardTest(unittest.TestCase):

    def test_valid(self):
        text = TextParagraph(
            element_id='test_text_id',
            content="test content"
        )

        item = Item(
            label='test',
            text=text
        )

        info_card = InfoCard(
            element_id='text_info_card_id',
            action_id='test_action_id',
            draggable=True,
            items=[item])

        expected = {
            'element_id': 'text_info_card_id',
            'type': 'info_card',
            'action_id': 'test_action_id',
            'draggable': True,
            'items': [
                {
                    'label': 'test',
                    'text': {
                        'element_id': 'test_text_id',
                        'content': 'test content',
                        'markdown': False,
                        'type': 'text'
                    }
                }
            ]
        }

        self.assertEqual(expected, info_card.dict(exclude_none=True))
