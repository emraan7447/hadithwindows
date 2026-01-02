import streamlit as st
import os, json, subprocess, asyncio
from dotenv import load_dotenv
import google.generativeai as genai
import edge_tts

load_dotenv()

BASE = os.getcwd()
TEMP_AUDIO = os.path.join(BASE, "temp", "audio")
TEMP_VIDEO = os.path.join(BASE, "temp", "video")

os.makedirs(TEMP_AUDIO, exist_ok=True)
os.makedirs(TEMP_VIDEO, exist_ok=True)

with open("data/bukhari.json", encoding="utf-8") as f:
    hadiths = json.load(f)["hadiths"]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_urdu_explanation(text):
    model = genai.GenerativeModel("gemini-pro")
    r = model.generate_content(
        f"Explain this hadith briefly in simple Urdu:\n{text}"
    )
    return r.text.strip()

async def tts(text, voice, out):
    c = edge_tts.Communicate(text, voice)
    await c.save(out)

def make_tts(text, voice, out):
    asyncio.run(tts(text, voice, out))

st.title("Hadith Shorts Generator")

nums = [h["hadith_number"] for h in hadiths]
num = st.selectbox("Select Hadith", nums)

if st.button("Generate Video"):
    h = next(x for x in hadiths if x["hadith_number"] == num)

    urdu_exp = get_urdu_explanation(h["urdu"])
    urdu_audio = os.path.join(TEMP_AUDIO, "urdu.mp3")
    make_tts(urdu_exp, "ur-PK-AsadNeural", urdu_audio)

    inputs = [f"-i {urdu_audio}"]

    if h.get("contains_dua"):
        arabic_audio = os.path.join(TEMP_AUDIO, "arabic.mp3")
        make_tts(h["dua_arabic"], "ar-SA-HamedNeural", arabic_audio)
        inputs = [f"-i {arabic_audio}", f"-i {urdu_audio}"]

    subs = f"""[Script Info]
PlayResX:1080
PlayResY:1920

[V4+ Styles]
Style: Arabic,Amiri,56,&H00FFFFFF,8,200
Style: Urdu,Noto Nastaliq Urdu,42,&H00FFFFFF,2,140

[Events]
Dialogue:0,0:00:00.00,0:00:08.00,Arabic,,,{h.get("dua_arabic","")}
Dialogue:0,0:00:08.00,0:00:20.00,Urdu,,,{urdu_exp}
"""

    subs_path = os.path.join(TEMP_VIDEO, "subs.ass")
    with open(subs_path, "w", encoding="utf-8") as f:
        f.write(subs)

    bg = os.path.join(TEMP_VIDEO, "bg.mp4")
    subprocess.run([
        "ffmpeg","-y","-f","lavfi","-i",
        "color=c=black:s=1080x1920:d=20",
        bg
    ])

    out = os.path.join(TEMP_VIDEO, "final.mp4")

    cmd = f'''
    ffmpeg -y -i "{bg}" {" ".join(inputs)}
    -filter_complex "[0:a][1:a]concat=n={len(inputs)}:v=0:a=1[a]"
    -map 0:v -map "[a]"
    -vf subtitles='{subs_path}'
    -t 20 -pix_fmt yuv420p "{out}"
    '''

    subprocess.call(cmd, shell=True)
    st.video(out)
