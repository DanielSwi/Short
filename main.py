import math
import random
from gtts import gTTS
import datetime
from moviepy.editor import *
import cv2
import matplotlib.pyplot as plt
import subprocess
from moviepy.video.fx.resize import resize

from bing_image_downloader import downloader


class ShortMaker:
    BUFFER = 10
    def __init__(self, background_id):
        self.language = "fr"  # can change language
        self.attrs = self.get_attrs()
        self.background_path = f"./backgrounds/{background_id}.jpg"
        self.o_path = f"./blank_videos/{background_id}.mp4"
        self.text = self.get_text()
        self.audio_path = self.get_audio()
        self.download_players()
        print(f"Making Video")
        self.make_video()
        print("Video done")

    def make_video(self):

        audio = AudioFileClip(self.audio_path)
        video_length = audio.duration * 1.5

        background_music = AudioFileClip("./music/music_1.wav")
        s = random.randint(0, int(background_music.duration - video_length) - self.BUFFER)
        background_music = background_music.set_start(s).set_duration(video_length)
        self.make_video_background(video_length)
        clip = VideoFileClip(self.o_path)
        # Add text to the clip

        player_1 = ImageClip(f"./players/{self.attrs[0]}/Image_1.jpg").set_start(0.5).set_duration(video_length - 1) \
                                            .set_position((400, 400))
        player_2 = ImageClip(f"./players/{self.attrs[1]}/Image_1.jpg").set_start(0.5).set_duration(video_length - 1) \
                                            .set_position((400, 1200))

        player_1 = resize(player_1, height=400, width=400)
        player_2 = resize(player_2, height=400, width=400)

        text_1 = TextClip(self.attrs[0], fontsize=70, color='white')
        text_1 = text_1.set_position((400, 300)).set_start(1).set_duration(video_length - 1)
        text_2 = TextClip(self.attrs[1], fontsize=70, color='white')
        text_2 = text_2.set_position((400, 1700)).set_start(1).set_duration(video_length - 1)

        # Combine the video clip and the text clip
        final_clip = CompositeVideoClip([clip, text_1, text_2, player_1, player_2])

        # with AudioFileClip(f"./music/music_1.wav").set_duration(video_length - 1) as snd:  # from a numeric array
        #    final_clip = final_clip.set_audio(snd)
        final_audio = CompositeAudioClip([audio, background_music])

        final_clip = final_clip.set_audio(final_audio)
        # Save the final video clip to a new file
        final_clip.write_videofile("my_edited_video.mp4")
        audio.close()
        background_music.close()


    def get_attrs(self):
        return ["Messi", "Ronaldo"]

    def make_video_background(self, time):
        if os.path.exists(self.o_path):
            return
        command = f'''ffmpeg -framerate 30 -i {self.background_path} -t {time} \
                        -c:v libx265 -x265-params lossless=1 \
                        -pix_fmt yuv420p -vf "scale=3840:2160,loop=-1:1" \
                        -s 1080x1920 \
                        -movflags faststart {self.o_path}'''
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Video created successfully at {self.o_path}")
        except subprocess.CalledProcessError as error:
            print(f"Error creating video: {error}")

    def get_text(self):
        return f"""
        Qui est le meilleur joueur entre {self.attrs[0]} et {self.attrs[1]} ?
        Double clique sur le meilleur joueur.
        
        
        """

    def get_audio(self):

        audio = gTTS(self.text, lang="fr", slow=True)
        audio_path = './audio_pip.wav'
        audio.save(audio_path)  # Save output in .WAV file
        return audio_path

    def download_players(self):
        for attr in self.attrs:
            if os.path.exists(f"./players/{attr}/"):
                continue
            downloader.download(attr, limit=1, output_dir="players", adult_filter_off=False)


def main():
    vid = ShortMaker(background_id=1)





if __name__ == "__main__":
    main()