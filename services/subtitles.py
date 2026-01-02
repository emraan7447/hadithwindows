def build(ar, ur, ref, dur):
    return f"""[Script Info]
PlayResX:1080
PlayResY:1920

[V4+ Styles]
Style: Arabic,Amiri,56,&H00FFFFFF,8,300
Style: Urdu,Noto Nastaliq Urdu,42,&H00FFFFFF,2,140
Style: Ref,Arial,28,&H00FFFFFF,2,60

[Events]
Dialogue:0,0:00:00.00,0:00:{dur}.00,Ref,,,{ref}
Dialogue:0,0:00:00.00,0:00:06.00,Arabic,,,{ar}
Dialogue:0,0:00:06.00,0:00:{dur}.00,Urdu,,,{ur}
"""