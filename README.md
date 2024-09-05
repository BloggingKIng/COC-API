# User Guide
This is a web app to keep track of war stars earned by different members of clans in Clash of Clans 

## How to use!

1. Get you API key from COC developer website and than open the views.py file and replace the api key with your own api key and replace the clan_tag with the tag of your own clan.
2. Install the required dependencies using `pip isntall -r requirements.txt`
3. Delete the db.sqlite3 file and run the migrations using `python manage.py makemigrations` and than `python manage.py migrate`
4. Start the server using `python manage.py runserver`
5. The server will refresh the stars earned by ur clanmates every 10 minutes
   ![image](https://github.com/user-attachments/assets/5ee29957-9542-47b0-b0eb-1c3eb0a002ec)
 
