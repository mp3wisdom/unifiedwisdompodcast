import os
import sys
import datetime
import mutagen
from mutagen.mp3 import MP3

# Base info
PODCAST_TITLE = "Unified Wisdom Podcast"
PODCAST_LINK = "https://mp3wisdom.github.io/unifiedwisdompodcast/"
PODCAST_DESCRIPTION = "Exploring stories, reflections, and wisdom"
AUTHOR = "Kishore"
IMAGE_URL = "https://mp3wisdom.github.io/unifiedwisdompodcast/cover.png"

# Cloudflare R2 public base URL
BASE_URL = "https://pub-f000923aafd841f79859a973467e4669.r2.dev/"

# Episodes folder (in repo, where MP3 files are placed)
EPISODE_FOLDER = "episodes"

def format_duration(seconds: int) -> str:
    mins, secs = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    if hrs > 0:
        return f"{hrs:02}:{mins:02}:{secs:02}"
    else:
        return f"{mins:02}:{secs:02}"

def generate_item(file_path, file_name):
    audio = MP3(file_path)
    size = os.path.getsize(file_path)
    duration = format_duration(audio.info.length)

    title = os.path.splitext(file_name)[0].replace("_", " ").title()
    pub_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    url = BASE_URL + file_name

    return f"""
  <item>
    <title>{title}</title>
    <description>{title} episode</description>
    <pubDate>{pub_date}</pubDate>
    <enclosure url="{url}" length="{size}" type="audio/mpeg"/>
    <guid>{url}</guid>
    <itunes:duration>{duration}</itunes:duration>
  </item>
"""

def main():
    items = []
    for file_name in sorted(os.listdir(EPISODE_FOLDER)):
        if file_name.lower().endswith(".mp3"):
            file_path = os.path.join(EPISODE_FOLDER, file_name)
            items.append(generate_item(file_path, file_name))

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
<channel>
  <title>{PODCAST_TITLE}</title>
  <link>{PODCAST_LINK}</link>
  <description>{PODCAST_DESCRIPTION}</description>
  <language>en-us</language>
  <itunes:author>{AUTHOR}</itunes:author>
  <itunes:explicit>false</itunes:explicit>
  <itunes:category text="Society &amp; Culture"/>
  <itunes:image href="{IMAGE_URL}"/>
{''.join(items)}
</channel>
</rss>
"""
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write(rss_content)

if __name__ == "__main__":
    main()
