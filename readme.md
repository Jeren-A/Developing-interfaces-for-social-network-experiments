
## Install dependencies
To install all dependencies please run `requirements.txt`  file first:
` pip install -r requirements.txt`  -> python2 users
` pip3 install -r requirements.txt` -> python3 users

## Run the project
To see dashboard on your local host run: 
    ``` streamlit run main.py```


# Technicality: 

## Steamlit
Streamlit is an open-source app framework used to create a Dashboard with Python. `main.py` is the main frontend source file to run the project.

## Main.py
Main.py file functionality:
1. Create a *Pure* object
2. Display *Options Menu : 'User Toots','User Profile','Diffusion Netwok', 'Word Cloud'*
3. If user selects **User Toots**:
        - By getting a username from the user, program calls `get_user_id` and `get_user_toots` methods of Pure object and displays a graph of toots' favourites_count versus toot_time.
            - Graph can also display details about each toot when clicked on it.
    4.  If user selects **User Profile**:
        - Program displays *.html* file that includes information about .... of user
        - Display Account Statistics: 
                -  **Toots by day of week** - frequency of last 40 toots accorgins to the days of the week
                -  **Toots timeseries** - frequency of last 40 toots according to the timespan
    5. If user selects **Diffusion Netwok**:
        - Program gets user id from username
        - Creates `followings_network` from Pure object 
        - Displays Diffusion Network on Dashboard
            
    6. If user selects **Word Cloud**:
        - Program gets toots' content from Pure object and creates a word cloud of upto 3000 words in shape of Mastodon



## Pure.py
 - serves as a `server communicator` between Mastadon and ...

### Creating an actual Mastodon API instance:
By creating a `Pure` object you create an actual mastadon API instance.  It has an API that allows you to interact with matodon's every aspect. 

#### *Pure* object's functionality :

 1. Assig a title and a descriction for the server
 2. Get a timeline of specific logged in user
 3. Create a dataframe which includes `{user_ids, usernames, toot_ids, toot_time, favourites_count, toot_content}`
 4. Get *user_id* provided a username
 5. Provide *user_toots* given a user_id
 6. Create a **Following Network** of 400 users starting from given a user_id.
 7. Create detailed .html file that includes **account_information** provided a username 
 8. Get clean content of last 400 toots provided a user_id implemented to create a **Word Cloud**
 

## Deploy Dashboard on Streamlit
 - Host your project in a public GitHub repo
 - Sign up for Streamlit sharing:
        1. Request an invite at streamlit.io/sharing.  (usually it takes couple of days to receive an invite)
        2. After receiveing your invite email, you can deploy your app by following the steps here https://docs.streamlit.io/en/stable/deploy_streamlit_app.html 
        
        



 
 
 


-  
