from mastodon import Mastodon, StreamListener
from pure import Pure

# ISO 639-2 Language Codes' corresponding language name    
lang_dict = {'ab': 'Abkhaz',
        'aa': 'Afar',
         'af': 'Afrikaans',
         'ak': 'Akan',
         'sq': 'Albanian',
         'am': 'Amharic',
         'ar': 'Arabic',
         'an': 'Aragonese',
         'hy': 'Armenian',
         'as': 'Assamese',
         'av': 'Avaric',
         'ae': 'Avestan',
         'ay': 'Aymara',
         'az': 'Azerbaijani',
         'bm': 'Bambara',
         'ba': 'Bashkir',
         'eu': 'Basque',
         'be': 'Belarusian',
         'bn': 'Bengali',
         'bh': 'Bihari',
         'bi': 'Bislama',
         'bs': 'Bosnian',
         'br': 'Breton',
         'bg': 'Bulgarian',
         'my': 'Burmese',
         'ca': 'Catalan; Valencian',
         'ch': 'Chamorro',
         'ce': 'Chechen',
         'ny': 'Chichewa; Chewa; Nyanja',
         'zh': 'Chinese',
         'cv': 'Chuvash',
         'kw': 'Cornish',
         'co': 'Corsican',
         'cr': 'Cree',
         'hr': 'Croatian',
         'cs': 'Czech',
         'da': 'Danish',
         'dv': 'Divehi; Maldivian;',
         'nl': 'Dutch',
         'dz': 'Dzongkha',
         'en': 'English',
         'eo': 'Esperanto',
         'et': 'Estonian',
         'ee': 'Ewe',
         'fo': 'Faroese',
         'fj': 'Fijian',
         'fi': 'Finnish',
         'fr': 'French',
         'ff': 'Fula',
         'gl': 'Galician',
         'ka': 'Georgian',
         'de': 'German',
         'el': 'Greek, Modern',
         'gn': 'Guaraní',
         'gu': 'Gujarati',
         'ht': 'Haitian',
         'ha': 'Hausa',
         'he': 'Hebrew (modern)',
         'hz': 'Herero',
         'hi': 'Hindi',
         'ho': 'Hiri Motu',
         'hu': 'Hungarian',
         'ia': 'Interlingua',
         'id': 'Indonesian',
         'ie': 'Interlingue',
         'ga': 'Irish',
         'ig': 'Igbo',
         'ik': 'Inupiaq',
         'io': 'Ido',
         'is': 'Icelandic',
         'it': 'Italian',
         'iu': 'Inuktitut',
         'ja': 'Japanese',
         'jv': 'Javanese',
         'kl': 'Kalaallisut',
         'kn': 'Kannada',
         'kr': 'Kanuri',
         'ks': 'Kashmiri',
         'kk': 'Kazakh',
         'km': 'Khmer',
         'ki': 'Kikuyu, Gikuyu',
         'rw': 'Kinyarwanda',
         'ky': 'Kirghiz, Kyrgyz',
         'kv': 'Komi',
         'kg': 'Kongo',
         'ko': 'Korean',
         'ku': 'Kurdish',
         'kj': 'Kwanyama, Kuanyama',
         'la': 'Latin',
         'lb': 'Luxembourgish',
         'lg': 'Luganda',
         'li': 'Limburgish',
         'ln': 'Lingala',
         'lo': 'Lao',
         'lt': 'Lithuanian',
         'lu': 'Luba-Katanga',
         'lv': 'Latvian',
         'gv': 'Manx',
         'mk': 'Macedonian',
         'mg': 'Malagasy',
         'ms': 'Malay',
         'ml': 'Malayalam',
         'mt': 'Maltese',
         'mi': 'Māori',
         'mr': 'Marathi (Marāṭhī)',
         'mh': 'Marshallese',
         'mn': 'Mongolian',
         'na': 'Nauru',
         'nv': 'Navajo, Navaho',
         'nb': 'Norwegian Bokmål',
         'nd': 'North Ndebele',
         'ne': 'Nepali',
         'ng': 'Ndonga',
         'nn': 'Norwegian Nynorsk',
         'no': 'Norwegian',
         'ii': 'Nuosu',
         'nr': 'South Ndebele',
         'oc': 'Occitan',
         'oj': 'Ojibwe, Ojibwa',
         'cu': 'Old Church Slavonic',
         'om': 'Oromo',
         'or': 'Oriya',
         'os': 'Ossetian, Ossetic',
         'pa': 'Panjabi, Punjabi',
         'pi': 'Pāli',
         'fa': 'Persian',
         'pl': 'Polish',
         'ps': 'Pashto, Pushto',
         'pt': 'Portuguese',
         'qu': 'Quechua',
         'rm': 'Romansh',
         'rn': 'Kirundi',
         'ro': 'Romanian, Moldavan',
         'ru': 'Russian',
         'sa': 'Sanskrit (Saṁskṛta)',
         'sc': 'Sardinian',
         'sd': 'Sindhi',
         'se': 'Northern Sami',
         'sm': 'Samoan',
         'sg': 'Sango',
         'sr': 'Serbian',
         'gd': 'Scottish Gaelic',
         'sn': 'Shona',
         'si': 'Sinhala, Sinhalese',
         'sk': 'Slovak',
         'sl': 'Slovene',
         'so': 'Somali',
         'st': 'Southern Sotho',
         'es': 'Spanish; Castilian',
         'su': 'Sundanese',
         'sw': 'Swahili',
         'ss': 'Swati',
         'sv': 'Swedish',
         'ta': 'Tamil',
         'te': 'Telugu',
         'tg': 'Tajik',
         'th': 'Thai',
         'ti': 'Tigrinya',
         'bo': 'Tibetan',
         'tk': 'Turkmen',
         'tl': 'Tagalog',
         'tn': 'Tswana',
         'to': 'Tonga',
         'tr': 'Turkish',
         'ts': 'Tsonga',
         'tt': 'Tatar',
         'tw': 'Twi',
         'ty': 'Tahitian',
         'ug': 'Uighur, Uyghur',
         'uk': 'Ukrainian',
         'ur': 'Urdu',
         'uz': 'Uzbek',
         've': 'Venda',
         'vi': 'Vietnamese',
         'vo': 'Volapük',
         'wa': 'Walloon',
         'cy': 'Welsh',
         'wo': 'Wolof',
         'fy': 'Western Frisian',
         'xh': 'Xhosa',
         'yi': 'Yiddish',
         'yo': 'Yoruba',
         'za': 'Zhuang, Chuang',
         'zu': 'Zulu'}


# Main object listens to the stream
class Listener(StreamListener):
    def __init__(self,bot,pure):
        # self.bot for handling content
        self.bot = bot
        #self.pure for taking actions on the server with given credentials
        self.pure = pure
    def on_notification(self, ntf):
        # Follows back whoever follows the logged in user
        if ntf['type'] == 'follow':
            print("You have a new follower !",ntf['account']['username'])
            self.pure.account_follow(ntf['account']['id'])
            print("You followed back {}.".format(ntf['account']['username']))
        #print(ntf)
        # Replies mentions with 'Dont disturb'
        elif ntf['type'] == 'mention':
            print('Someone mentioned you !',ntf['account']['username'])
            self.pure.status_post('Dont disturb me 😡.',in_reply_to_id=ntf['status']['id'])
    def on_update(self, status):
        """A new status has appeared! 'status' is the parsed JSON dictionary
        describing the status."""
        # Detects language of the status and does a sentiment analysis with transformers pipeline
        toot_id = status['id']
        lang = self.bot.toot_language(status)
        label_score = self.bot.toot_sentiment(status)
        string = "This status' sentiment analysis is classified as {}, with confidence of {}. Model provided from transformers 🤗 (https://github.com/huggingface/transformers)".format(label_score[0]['label'],label_score[0]['score'])
        pure.status_post(string,in_reply_to_id=toot_id)
        context = self.bot.context(status)
        print('Context: ', context)
        print('Detected language: ', lang)
        #print(status)
    def handle_heartbeat(self):
        """The server has sent us a keep-alive message. This callback may be
        useful to carry out periodic housekeeping tasks, or just to confirm
        that the connection is still open."""

        print('Bot script is working...')



# bot features
class MastodonBot():
    def __init__(self):
        pass
    def cleanhtml(self,raw_html):
        import re
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    def toot_language(self,status):
        from textblob.sentiments import NaiveBayesAnalyzer
        from textblob import TextBlob
        global lang_dict
        toot_context = self.cleanhtml(status['content'])
        blob = TextBlob(toot_context,analyzer=NaiveBayesAnalyzer())
        detected_language = blob.detect_language()
        detected_language_name = lang_dict[detected_language]
        return detected_language_name
    def toot_sentiment(self,status):
        from transformers import pipeline
        classifier = pipeline('sentiment-analysis')

        label_score = classifier(self.cleanhtml(status['content']))
        return label_score

    # def toot_translate(self,status):
    #     toot_context = cleanhtml(status['content'])
    #     blob = TextBlob(toot_context,analyzer=NaiveBayesAnalyzer())
    #     try:
    #         blob.translate(to='tr')
    #     except NotTranslated:
    #         toot()
    #     pass
    def context(self,status):
        toot_context = self.cleanhtml(status['content'])
        return toot_context


if __name__ == '__main__':
    bot = MastodonBot()
    pure = Pure(access_token='./secrets/pure_user.secret',api_base_url='https://mastodon.social')
    listener = Listener(bot,pure)
    pure.stream_local(listener)