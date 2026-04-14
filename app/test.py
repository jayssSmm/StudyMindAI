from services.yt_services import transcript_extractor

a=input("link = ")
print(transcript_extractor.get_transcript(a))