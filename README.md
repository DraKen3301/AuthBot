# AuthBot
Just a simple tool in python to grab access tokens of users.

# Setup

## On Heroku

> https://heroku.com/

1. Fork the repository.
2. Connect it to an heroku app.
3. Add heroku/python buildpack.
4. Go to config vars and add required variables.
    - client_id = Client ID of your application.
    - client_secret = Client Secret of your application.
    - redirect_uri = URL obtained in step 7.
    - client_token = Token of your bot.
    - client_db = Project key of https://deta.sh/
    - webhook_url = URL of the logging webhook.
5. Replace the guild_id and role_id in line 11-12.
6. Procfile and requirements.txt are already configured, just enable dynos and let it run.
7. Go to App Settings > Domains > Copy the domain of your app.


## On Repl.it

> https://replit.com/

1. Fork the repository.
2. Create a new repl from this repository.
3. Go to secrets and add required secrets.
    - client_id = Client ID of your application.
    - client_secret = Client Secret of your application.
    - redirect_uri = URL obtained in step 8.
    - client_token = Token of your bot.
    - client_db = Project key of https://deta.sh/
    - webhook_url = URL of the logging webhook.
4. Replace the guild_id and role_id in line 11-12.
5. Install requirements.txt somehow idk i don't use replit.
6. Remove `#` from line 113.
7. Run the repl.
8. Copy the URL of your website by going to the web section.

# Developers

- [@DraKen3301](https://github.com/DraKen3301)

# Troubleshooting and Suggestions

> You can mail me at ask@drakencodes.tech or dm me on discord at DraKen#3301.
