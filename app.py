import streamlit as st, json, os
from services.tts import speak
from services.pexels import fetch_background
from services.subtitles import build
from services.video import render

TMP = "output/temp"
OUT = "output/videos"
os.makedirs(TMP, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

with open("data/bukhari.json", encoding="utf-8") as f:
    hadiths = json.load(f)["hadiths"]

st.title("Hadith Shorts Generator")

selected = st.multiselect(
    "Select Hadith(s)",
    hadiths,
    format_func=lambda h: h["reference"],
    max_selections=3
)

if st.button("Generate") and selected:
    for h in selected:
        st.write("Generating:", h["reference"])

        bg = f"{TMP}/{h['id']}_bg.mp4"
        fetch_background(st.secrets["PEXELS_API_KEY"], bg)

        audios = []
        if h["contains_dua"]:
            ar = f"{TMP}/{h['id']}_ar.mp3"
            speak(h["dua_arabic"], "ar-SA-HamedNeural", ar)
            audios.append(ar)

        ur = f"{TMP}/{h['id']}_ur.mp3"
        speak(h["urdu_explanation"], "ur-PK-AsadNeural", ur)
        audios.append(ur)

        subs = f"{TMP}/{h['id']}.ass"
        with open(subs,"w",encoding="utf-8") as f:
            f.write(build(
                h["dua_arabic"] if h["contains_dua"] else "",
                h["urdu_explanation"],
                h["reference"],
                20
            ))

        out = f"{OUT}/{h['id']}.mp4"
        render(bg, audios, subs, out)

        st.success(f"Done: {h['reference']}")
        st.video(out)
