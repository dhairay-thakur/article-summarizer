import requests
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

url = "https://arstechnica.com/science/2021/04/finland-may-beat-japan-in-the-wooden-satellite-space-race/"
article = Article(url)
article.download()
article.parse()

print(article.images)

image_url = "https://cdn.arstechnica.net/wp-content/uploads/2021/04/wisawoodsat_rendering_upsidedown-760x380.jpg"
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
    # Then crop the left and right edges:
    new_width = int(ideal_aspect * height)
    offset = (width - new_width)
    resize = (
        (0, 0, int(new_width), int(height)),
        (int(offset), 0, int(width), int(height))
    )
else:
    # ... crop the top and bottom:
    new_height = int(width / ideal_aspect)
    offset = (height - new_height)
    resize = (
        (0, 0, int(width), int(new_height)),
        (0, int(offset), int(width), int(height))
    )

with Image(blob=image_blob.content) as img:
    img.crop(*resize[0])
    img.save(filename='cropped_1.jpg')

with Image(blob=image_blob.content) as img:
    img.crop(*resize[1])
    img.save(filename='cropped_2.jpg')


LANGUAGE = "english"
SENTENCES_COUNT = 10

parser = PlaintextParser.from_string(article.text, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)
summarizer = Summarizer(stemmer)


# summarize text
CAPTION = []
for sentence in summarizer(parser.document, SENTENCES_COUNT):
    CAPTION.append(sentence._text)


with Image(blob=image_blob.content) as canvas:
    print(canvas.width)
    canvas.crop(*resize[0])
    print(canvas.width)
    canvas.font = Font("DelaGothicOne-Regular.ttf",
                       size=12,
                       color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(canvas.height/2)
    canvas.caption(CAPTION[0], gravity="center",
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='text_overlayed_1.jpg')

with Image(blob=image_blob.content) as canvas:
    canvas.crop(*resize[1])
    canvas.font = Font("DelaGothicOne-Regular.ttf",
                       size=12,
                       color=Color('white'))
    caption_width = int(canvas.width/1.2)
    margin_left = int((canvas.width-caption_width)/2)
    margin_top = int(canvas.height/2)
    canvas.caption(CAPTION[1], gravity='center',
                   width=caption_width, left=margin_left,
                   top=margin_top)
    canvas.format = "jpg"
    canvas.save(filename='text_overlayed_2.jpg')
