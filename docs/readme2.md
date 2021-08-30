# Dashboard and API


## Install dependencies
To install all dependencies please run `requirements.txt`  file first:  

    pip install -r requirements.txt

## Preview the project
To view dashboard on your local host run:  

    streamlit run main.py


# Components: 

## Steamlit
Streamlit is an open-source app framework used to create a Dashboard with Python.  
`main.py` is the main frontend source file to run the project.

## Pure.py  
 - serves as a `server communicator` between Mastadon and Dashboard  
 Built on top of the Mastodon.py python wrapper. Further information:  
 
 [Mastodon.py](https://github.com/halcy/Mastodon.py)


## Creating an actual Mastodon API instance:
By creating a `Pure` object you create an actual Mastodon API instance.  It has an API that allows you to interact with any given Mastodon server's every aspect.  
Generate your own secret files with provided methods and substitute your secret files to the Pure object.

### Register
Register your app! This only needs to be done once. Uncomment the code and substitute in your information:
 
```python
from pure import Pure

'''
Pure.create_app(
     'PURE',
     api_base_url = 'https://mastodon.social',
     to_file = 'app_cred.secret'
)
'''
```
### Login
Then login. This can be done every time, or you can use the persisted information:

```python
from pure import Pure

pure = Pure(
    client_id = 'app_cred.secret',
    api_base_url = 'https://mastodon.social'
)
pure.log_in(
    'my_login_email@example.com',
    'incrediblygoodpassword',
    to_file = 'user_cred.secret'
)
```
To post, create an actual API instance:

```python
from pure import Pure

pure = Pure(
    access_token = 'user_cred.secret',
    api_base_url = 'https://mastodon.social'
)
pure.toot('Tooting from python !')

```




#### *Pure* object's functionality :



* Get a title and a description from the server  - when conducting research on other mastodon servers your dashboard will automatically update its title
* Get a timeline of specific logged in user
* Create a dataframe which includes `{user_ids, usernames, toot_ids, toot_time, favourites_count, toot_content}`
* Get *user_id* from a provided *username*
* Provide *user_toots* from a given *user_id*
* Create a **Followings Network** of 400 users starting from given a *user_id*
* Create detailed *.html* file that includes **account_information** from a provided *username*
* Get clean content of last 400 toots from a provided  *user_id* which is implemented to create a **Word Cloud**
 




## Main.py
Main.py functionality:  
* Implement a *Pure* object  
* Display *Options Menu : User Toots, User Profile, Diffusion Netwok, Word Cloud*
* If user selects **User Toots**:

    - Takes username as input and calls `get_user_id` to communicate with Mastodon API and calls `get_user_toots` method of Pure object
    - Plots a graph of toots' favourites_count versus toot_time  
    - Graph can also display details about each toot when hover on it  
         
*  If user selects **User Profile**:
        
    - Program displays .html file that includes information about user
    - Display Account Statistics:
            - Toots by day of the week 
            - Toots timeseries  
            
* If user selects **Diffusion Netwok**:
    
    - Takes username as an input and displays a Diffusion Network graph.
        
* If user selects **Word Cloud**:

    - Program gets toots' content from Pure object, and creates a word cloud in shape of a mastodon


## Bot Template
* Listener:
    - Listener class inherits mastodon.py's StreamListener class.
    - Listener class listens the server with its every method and executes the followings according to corresponding server response.
    - By default follows back when a user follows the logged in account.
    - Replies mentions with `Dont disturb me 😡.` sentence.
    - Replies the toots on the current stream with sentiment analysis scores.

```python
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

    def handle_heartbeat(self):
        """The server has sent us a keep-alive message. This callback may be
        useful to carry out periodic housekeeping tasks, or just to confirm
        that the connection is still open."""

        print('Bot script is working...')
```


* MastodonBot:
    - Bot class for handling content.
        - Cleans the returned values' content for analysis.
        - Detects the language and sentiment of shared content.
    - This can be customized for the user's needs.
```python
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

    def context(self,status):
        toot_context = self.cleanhtml(status['content'])
        return toot_context
```

### Running the bot

* First create a MastodonBot object for handling content
* Create a Pure object with your credentials to communicate with server.
* Initialize the Listener object with the MastodonBot and Pure objects.
* Connect the Listener object to desired stream.
    - For streaming options, check [Streaming](https://mastodonpy.readthedocs.io/en/stable/#streaming) link.

Example bot initalization.

```python
bot = MastodonBot()
pure = Pure(access_token='./secrets/pure_user.secret',api_base_url='https://mastodon.social')
listener = Listener(bot,pure)
pure.stream_local(listener)
```