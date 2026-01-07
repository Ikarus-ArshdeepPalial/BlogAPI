from AI_Models.blogai.classifier import TextClassifier

# Create a single, shared instance of the classifier when the module is loaded.
classifier = TextClassifier()

def get_category(content):
    """function to determine the category of the blog post."""
    # Use the shared instance to classify the content.
    category = classifier.classify(content)
    return category