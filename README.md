# Spotify Tracker

## Description

This application tries to replicate the features of IMDB for Spotify. Specifically, it has two core functionalities inspired by IMDB.
1. It allows users to track tracks and albums in their library, updating the listening status and number of tracks listened to in the album.
2. It allows users to rate and review tracks and albums, and update them too.

## Technologies

- Flask
- MongoDB
- HTML/CSS/JavaScript
- Spotify Web API

## Setup

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.