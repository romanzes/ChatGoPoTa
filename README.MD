This was meant to be hosted on repl.io. Repl.io allows you to store 
secrets as environmental variables, so you need to have the following 
environment variables defined:
- `OPENAI_USER`: Your username on the OpenAI website
- `OPENAI_PASSWORD`: The password for your OpenAI account
- `OPENAI_MICROSOFT_LOGIN`: Whether or not you log with a Microsoft account 
(true/false)
- `TELEGRAM_BOT_NAME`: The username of your bot
- `TELEGRAM_BOT_TOKEN`: self-explanatory
- `TELEGRAM_GROUP_WHITELIST`: an array of group IDs where your bot can 
respond. This is needed so others don't add start using your bot in their 
groups and exhaust your quota.
