from unittest.mock import MagicMock

from lib.core.response import Response


def test_response():
    user = MagicMock()
    user.name = 'user_name'
    user.avatar_url = 'avatar'

    response = Response(
        title='TITLE',
        content='my content',
        user=user,
        colour=5051,
        footer_img='img',
        footer_text='footer',
        author_url='http://example.com/',
    )
    assert response.render().to_dict() == {
        'author': {'icon_url': 'avatar', 'name': 'user_name', 'url': 'http://example.com/'},
        'color': 5051,
        'description': 'my content',
        'footer': {'icon_url': 'img', 'text': 'footer'},
        'title': 'TITLE',
        'type': 'rich',
    }
