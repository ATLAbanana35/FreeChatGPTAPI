Here is a simple project that offer FREE CHATGPT API!
Some details:
There NOT ALLS FONCTIONALLITIES, like choices in messages.
OpenAI risk to block you for an hour.
This project risk to be obselete! Dues to class changes. If there is an error (in the web client) like this : `Error: cannot defind properties of null`. Please make an issue, I will correct it soon.
Ok, how that work ?
We uses a script in the web interface to interact with ChatGPT like a normal user, we send the result to a Flask server that simule the api.
How to use it.
In your project change the open ai base_url to : http://127.0.0.1:5000/v1
Then install this browser extention (ENABLE IT O.N.L.Y. WHEN YOU USE THIS PROJECT, THAT'S A SECURITY RISK) : https://chromewebstore.google.com/detail/always-disable-content-se/ffelghdomoehpceihalcnbmnodohkibj
(Use for allow the js script to talk with the Flask server
THEN : Allow mixed content in the site "https://chat.openai.com" in the site settings
THEN : Open your browser console and then paste what is in the "client.js"
THEN : Run the server by running `flask run`
***NOTES***
1. USE IT AT YOUR OWN RISK
2. I DON'T KNOW IF THAT'S LEGAL, SO USE IT ONLY FOR PRIVATE USE.
