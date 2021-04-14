import os
import uuid
import requests
from flask import Flask, request, send_file
from newspaper import Article
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.font import Font
from wand.image import Image

app = Flask(__name__)


@app.route('/api', methods=['POST', 'GET'])
def summarize_article():
    posted_data = request.get_json() or {'url': ""}
    url = posted_data['url']
    if(url == ""):
        return {'message': 'Invalid URL!'}
    article = Article(url)
    article.download()
    article.parse()

    LANGUAGE = "english"
    SENTENCES_COUNT = 10

    parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)

    # summarize text
    CAPTION = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        CAPTION = sentence._text
        if(len(CAPTION) < 150):
            break

    image_url = article.top_image
    image_blob = requests.get(image_url)

    dims = (1080, 1920)
    ideal_width = dims[0]
    ideal_height = dims[1]
    ideal_aspect = ideal_width / ideal_height

    with Image(blob=image_blob.content) as img:
        size = img.size

    width = size[0]
    height = size[1]
    aspect = width/height

    if aspect > ideal_aspect:
        # crop the left and right edges:
        new_width = int(ideal_aspect * height)
        offset = (width - new_width) / 2
        resize = (int(offset), 0, int(width - offset), int(height))
    else:
        # crop the top and bottom edges:
        new_height = int(width / ideal_aspect)
        offset = (height - new_height) / 2
        resize = (0, int(offset), int(width), int(height - offset))

    print(len(CAPTION))
    print(CAPTION)
    with Image(blob=image_blob.content) as canvas:
        print(canvas.width)
        canvas.crop(*resize)
        print(canvas.width)
        canvas.font = Font("DelaGothicOne-Regular.ttf",
                           size=12,
                           color=Color('white'))
        caption_width = int(canvas.width/1.2)
        margin_left = int((canvas.width-caption_width)/2)
        margin_top = int(canvas.height/2)
        canvas.caption(CAPTION, gravity="center",
                       width=caption_width, left=margin_left,
                       top=margin_top)
        canvas.format = "jpg"
        unique_name = str(uuid.uuid4())
        canvas.save(filename=f'{unique_name}.jpg')

    return {'imageId': unique_name}


@app.route('/api/get-image/<id>', methods=['POST', 'GET'])
def get_image(id):
    return send_file(f'{id}.jpg', mimetype='image/gif')


@app.route('/api/remove-image/<id>', methods=['GET', 'POST'])
def remove_img(id):
    os.remove(f'{id}.jpg')
    return {'deleted-file': id}


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
