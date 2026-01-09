from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .labels import CATEGORIES


class TextClassifier:
    def __init__(self, threshold=0.4):
        self.model=SentenceTransformer("all-MiniLM-L6-v2")
        self.threshold = threshold
        self.category_embeddings = self._embed_categories()
        
    def _embed_categories(self):
        embeddings={}
        for category, keyword in CATEGORIES.items():
            
            emb=self.model.encode(keyword)
            embeddings[category]=np.array(emb)
        return embeddings
    
    def classify(self, text:str):
        # Truncate text to a reasonable length for the model to avoid errors.
        truncated_text = text[:1500]
        text_embedding = self.model.encode(truncated_text)
        text_embedding = np.array(text_embedding).reshape(1, -1)
        
        best_category = ""
        max_confidence = -1.0

        for category, keyword_embeddings in self.category_embeddings.items():
            # Compare the text embedding against all keyword embeddings for the category.
            similarities = cosine_similarity(text_embedding, keyword_embeddings)
            
            # The confidence for the category is the highest similarity found.
            category_max_similarity = np.max(similarities)
            
            if category_max_similarity > max_confidence:
                max_confidence = category_max_similarity
                best_category = category
        
        # if max_confidence >= self.threshold:
        #     return best_category
        # else:
        #     # Return empty string, suitable for a CharField with blank=True
        #     return ""

        return best_category
            
 
 