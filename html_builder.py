def process_editorjs_text(text_json):
    tags = {
        'paragraph': parse_paragraphs,
        'header': parse_headers,
        'list': parse_lists
    }
    html = ''
    for block in text_json:
        html += tags[block['type']](block) + '\n'
    return html


def parse_paragraphs(block):
    return '<p>' + block['data']['text'] + '</p>'


def parse_headers(block):
    level = block['data']['level']
    return f'<h{level}>' + block['data']['text'] + f'</h{level}>'


def parse_lists(block):
    list_types = {
        'ordered': 'ol',
        'unordered': 'ul'
    }
    list_type = list_types[block['data']['style']]
    return f'<{list_type}>\n'\
           + '\n'.join([f'  <li>{text}</li>' for text in block['data']['items']])\
           + f'\n</{list_type}>'
