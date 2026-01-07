from AI_Models.blogai.summarizer import Blogsummarizer

# Create a single, shared instance of the summarizer when the module is loaded.
summarizer = Blogsummarizer()

def generate_summary(content):
    """A placeholder function to generate a summary."""
    # Use the shared instance to generate the summary.
    summary = summarizer.summarize(content)
    return summary