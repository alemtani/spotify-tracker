# Spotify Tracker

This application is a lite version of what an IMDb for Spotify would look like.

## Deployment

https://spotify-tracker-eta.vercel.app/

## Technologies

- Flask
- MongoDB
- Vercel
- Spotify Web API

## Configure Environment

Create a `.env` file with the following keys.

`SECRET_KEY`

Generate a secret key by copying the output of this command.

```
python3 -c 'import secrets; print(secrets.token_hex())'
```

`MONGODB_HOST`

This is your connection string to the MongoDB Atlas cluster. For instructions on how to get it, see [here](https://www.mongodb.com/docs/guides/atlas/connection-string/). An example string looks like this:

```
mongodb+srv://<mongodbuser>:<password>@cluster0.gy12rxn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
```

`CLIENT_ID`

This is the Spotify Client ID you get when you create an app by following the instructions [here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started).

`CLIENT_SECRET`

Follow the instructions linked above, just like for `CLIENT_ID`.

## Running Locally

Make sure Python 3 is installed on your computer, and make sure you are in your project directory.

You should create a virtual environment when running this project. Here's how to do so (if you use a Windows machine, you really should use [WSL](https://learn.microsoft.com/en-us/windows/wsl/about)).

```
python3 -m venv venv
```

Now activate the environment.

```
source ./venv/bin/activate
```

With the virtual environment, go ahead and install the requirements for the project.

```
pip3 install -r requirements.txt
```

And now you can start!

```
flask run
```

## Writeup

This project was completed as coursework for **CMSC388J: Building Secure Web Applications** at the University of Maryland. Please find the writeup for the project [here](WRITEUP.md).