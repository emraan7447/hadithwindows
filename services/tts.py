import asyncio, edge_tts

async def _speak(text, voice, out):
    await edge_tts.Communicate(text, voice).save(out)

def speak(text, voice, out):
    asyncio.run(_speak(text, voice, out))
