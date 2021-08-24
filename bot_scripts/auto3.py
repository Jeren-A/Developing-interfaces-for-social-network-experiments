import PyPDF2
import numpy as np
import time 
from mastodon import Mastodon
pdfFileObj = open('book.pdf', 'rb')
 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

mastodon = Mastodon(access_token = 'onurva.secret', api_base_url = 'https://dogukankefeli.tech')
while True:
    try:
        pageObj = pdfReader.getPage(np.random.randint(0,670))
        text = pageObj.extractText().split('\n')
        index = np.random.randint(len(text))
        text2 = text[index-3:index]
        text3 = " ".join(text2)
        print(len(text3))
        #print(text3)
        if len(text3)>500:
            text3=text3[:498]
        print(text3)
        mastodon.toot(text3)
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print (message)
        
    time.sleep(30)
