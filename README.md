# Spotify_downloader

This project is a Python-based application that allows you to input Spotify song or playlist links. It utilizes the Spotify API to retrieve song details and then uses the YouTube API to search for the corresponding song and download its MP3 audio.

## Features

- Input a Spotify song or playlist link.
- Utilize the Spotify API to fetch song details such as artist, album, and track name.
- Use the YouTube API to search for the song based on its details.
- Download the identified song from YouTube as an MP3 audio file.

## Prerequisites

- Python 3.x
- [Spotify Developer Account](https://developer.spotify.com/dashboard/login) and API credentials
- [YouTube Data API Key](https://developers.google.com/youtube/registering_an_application)

## Installation

1. Clone this repository
2. Navigate to the project directory
3. Install the required dependencies: `pip install -r requirements.txt`

## Configuration

1. Replace the placeholders in `.env` with your actual API credentials.

## Usage

1. Run the application: `main.py`
2. Enter a Spotify song or playlist link when prompted.
3. The application will use the Spotify API to retrieve song details.
4. It will then use the YouTube API to search for the song and download its MP3 audio.

## Disclaimer

This project is intended for educational purposes only. Ensure you have the necessary rights to download and use the music files as per your local laws and regulations.



