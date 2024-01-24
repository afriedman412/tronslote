### SETUP:

1. Put the key .json file in the home directory.
2. Make a ".env" file in the home directory. Put the following things in it:
PROJECT_ID=tronslote
GOOGLE_APP_CREDENTIALS_FILE=(name of the key .json file)
3. Run `make install-dev` to install all the dependencies
4. Run `source venv/bin/activate` to activate the environment.
5. (optional) Run `make install-dev` and `make test` to verify your setup works.
4. Run `flask run` to run the app.

### INSTRUCTIONS:
The submission form will load at http://localhost:5000/.

If you just want to use it as an endpoint for the translation script, make a POST request to http://localhost:5000/api/submit with the format:

```
{
    'base_lang': 'en', 
    'input_lang': 'en',
    'input_text': 'You are lying to the governor.',
    'interim_langs': ['es', 'he', 'ak', 'fr']
}
```

The languages live in `.src.LANGUAGES`, and you can add more there if you want assuming they are supported by Google Translate! If you want to get real freaky, [here's a list of all the ISO-639 language codes](https://www.loc.gov/standards/iso639-2/php/code_list.php).