import subprocess

def render(bg, audios, subs, out):
    inputs = []
    for a in audios:
        inputs += ["-i", a]

    cmd = [
        "ffmpeg","-y","-i",bg,
        *inputs,
        "-filter_complex",f"concat=n={len(audios)}:v=0:a=1[a]",
        "-map","0:v","-map","[a]",
        "-vf",f"subtitles='{subs}'",
        "-pix_fmt","yuv420p",
        out
    ]
    subprocess.run(cmd)
