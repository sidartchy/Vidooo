from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from langchain.schema import Document
import re 
import logging
from typing import List

def _extract_video_id(url: str) -> str:
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query)

        
        if 'v' in query:
            return query['v'][0]
        match = re.search(r"youtu\.be/([^?&/]+)", url)
        if match:
            return match.group(1)
        
        match = re.search(r"youtube\.com/embed/([^?&/]+)", url)
        if match:
            return match.group(1)

        raise ValueError("Cannot extract video ID from URL")
    except Exception as e:
        print(f"Error: {e}")
        return ""
    
def load_transcript_document(transcript: List[dict], vid_id: str) -> List[Document]:
    if not transcript:
        raise ValueError('No transcript found')
    documents = [] 
    logging.debug(f'Started transcribing...')
    for idx, entry in enumerate(transcript):
        start_time = entry['start']
        end_time = start_time + entry['duration']
        video_id = vid_id
        text = entry['text']

        # format timestamp as H:MM:SS
        def format_time(seconds):
            m, s = divmod(int(seconds), 60)
            h, m = divmod(m, 60)
            return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

        metadata = {
            'start_time': start_time,
            'end_time': end_time,
            'timestamp':  f"{format_time(start_time)} - {format_time(end_time)}",
            'video_id': video_id,
            "source": f"https://www.youtube.com/watch?v={vid_id}&t={int(start_time)}s",
            "language": "en", 
        }

        documents.append(Document(page_content=text, metadata= metadata))
        logging.debug(f'Entry {idx} transcribed')
    return documents

def load_documents(url: str, language: str = 'en'):
    ytt_api = YouTubeTranscriptApi()
    video_id = _extract_video_id(url)
    if not video_id:
        raise Exception('Video ID not found')
    
    try:
        # Try to get transcript in specified language
        transcript = ytt_api.fetch(video_id, languages=[language]).to_raw_data()
    except Exception as e:
        print(f"Warning: Could not fetch transcript in {language}. Trying default language...")
        # Fallback to default language if specified language not available
        transcript = ytt_api.fetch(video_id).to_raw_data()
    
    if not transcript:
        raise Exception('Transcript not found')
    documents = load_transcript_document(transcript, video_id)
    return documents




if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    url : str = 'https://www.youtube.com/watch?v=5WQgLboa_I8&t=160s'
    documents = load_documents(url)
    print(documents[100].page_content[:100])
    print(documents[100].metadata)
    
