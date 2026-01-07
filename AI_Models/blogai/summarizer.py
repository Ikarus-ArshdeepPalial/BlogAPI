from transformers import pipeline

class Blogsummarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
        
    def summarize(self, text: str):
        # Manually truncate input text to a safe length to prevent IndexError.
        truncated_text = text[:2000]
        result = self.summarizer(truncated_text, max_length=150, min_length=80, do_sample=False)
        if result and isinstance(result, list) and 'summary_text' in result[0]:
            return result[0]['summary_text']
        return ""