from dotenv import load_dotenv
import os 
import base64
from requests import post,get
import json
import pprint
from moviepy.editor import *
from pytube import YouTube
from googleapiclient.discovery import build
#load data from .env
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string= client_id +":"+client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes),"utf-8")

    url="https://accounts.spotify.com/api/token"
    headers={"Authorization":"Basic " +auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"}
    data={"grant_type": "client_credentials"}
    result=post(url,headers=headers,data=data)#post and get json str
    json_result=json.loads(result.content)
    token=json_result["access_token"]
    return token

def  get_auth_header(token):
    return {"Authorization":"Bearer " + token}

def main():
    url=input("Paste the Song Link from Spotify:    ")
    #get single tracks info
    if "track" in url:
        track_id=url.split('/')[-1].split('?')[0]   
        songs=get_song(token, track_id)
    #get playlists all tracks info    
    elif "playlist" in url:
        palylist_id=url.split('/')[-1].split('?')[0] 
        songs=get_playlist(token,palylist_id) 
    #search for tracks in youtube   
    count=len(songs) 
    for i in range(len(songs)):
        search_string=songs[i]+" audio"
        link_for_song=find_youtube(search_string)
        audio=download_audio(link_for_song)
        if audio:
            #set_metadata(track_info, audio)
            os.replace(audio, f"../music/{os.path.basename(audio)}")
            print(
                f"Downloaded song {i+1} of {count}"
            )
            #downloaded += 1
        else:
            print("File exists. Skipping...")


def get_song(token,track_id):
    url="https://api.spotify.com/v1/tracks/"
    headers=get_auth_header(token)
    query_url=url+track_id
    result=get(query_url, headers=headers)
    song_data=json.loads(result.content)
    song_name=song_data["name"]
    artist=song_data["artists"][0]["name"]
    track_info =[f"{song_name} by {artist}"]
    return track_info


def get_playlist(token,playlist_id):
    url="https://api.spotify.com/v1/playlists/"
    headers=get_auth_header(token)
    query_url=url+playlist_id+""
    result=get(query_url, headers=headers)
    playlist_jdata=json.loads(result.content)
    playlist_data=[]
    for i in range(len(playlist_jdata['tracks']['items'])):
        x=len(playlist_jdata['tracks']['items'][i]['track']['artists'])
        playlist_data.append(f"{playlist_jdata['tracks']['items'][i]['track']['name']} by {playlist_jdata['tracks']['items'][i]['track']['artists'][0]['name']}")
    return playlist_data


def find_youtube(query):
    yt_api=os.getenv("yt_api_key")
    youtube=build('youtube','v3',developerKey=yt_api)
    req=youtube.search().list(q=query,part='snippet',type='video',maxResults=1)
    #tries to get track info for only 2 times  
    tries=0
    while tries<2:
        try:
            #sending request to get data
            result=req.execute()
            break
        except:
            tries+=1
    else:
        print("Couldn't connect to youtube")    
    #returning video links for given track        
    for item in result['items']:
        vid_link = "https://www.youtube.com/watch?v=" + item['id']['videoId']
        return vid_link


def download_audio(link_for_song):
    song=YouTube(link_for_song)
    #remove all cahr which can be in folder path or name
    song.title="".join([c for c in song.title if c not in ['/', '\\', '|', '?', '*', ':', '>', '<', '"']])
    video=song.streams.filter(only_audio=True).first()
    video_file=video.download(output_path="../music/tmp")
    #video to audio(mp3)
    cur_file=os.path.splitext(video_file)[0]
    audio_file=cur_file+".mp3"
    mp4_no_frame = AudioFileClip(video_file)
    mp4_no_frame.write_audiofile(audio_file, logger=None)
    mp4_no_frame.close()
    #saving downloaded audioin pre-designated location
    os.remove(video_file)
    os.replace(audio_file, f"../music/tmp/{song.title}.mp3")
    audio_file = f"../music/tmp/{song.title}.mp3"
    return audio_file



if __name__ == '__main__':
    token=get_token()
    main()
    
