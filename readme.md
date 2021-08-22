
## Install dependencies
To install all dependencies please run `requirements.txt`  file first:

 ` pip3 install -r requirements.txt`

## Preview the project
To view dashboard on your local host run: 
    ``` streamlit run main.py```


# Technicality: 

## Steamlit
Streamlit is an open-source app framework used to create a Dashboard with Python.  
`main.py` is the main frontend source file to run the project.  

## Pure.py  
 - serves as a `server communicator` between Mastadon and Dashboard  

### Creating an actual Mastodon API instance:
By creating a `Pure` object you create an actual mastadon API instance.  It has an API that allows you to interact with mastodon's every aspect.  
Generate your own secret files with `Mastodon.py` class and substitute your details to Pure object.


#### *Pure* object's functionality :



 1. Get a title and a description from the server  - when conducting research on other mastodon servers your dashboard will automatically update its title
 2. Get a timeline of specific logged in user
 3. Create a dataframe which includes `{user_ids, usernames, toot_ids, toot_time, favourites_count, toot_content}`
 4. Get *user_id* provided a username
 5. Provide *user_toots* given a user_id
 6. Create a **Following Network** of 400 users starting from given a user_id.
 7. Create detailed .html file that includes **account_information** provided a username 
 8. Get clean content of last 400 toots provided a user_id implemented to create a **Word Cloud**
 


## Main.py
Main.py file functionality:  
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
        
        - Takes username as an input and displays Diffusion Network  
        
* If user selects **Word Cloud**:

        - Program gets toots' content from Pure object, and creates a word cloud in shape of Mastodon


