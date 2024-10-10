import math
from collections import Counter
import re

class MatchingUtils:
    @staticmethod
    def tokenize(text):
        """
        Tokenizes a string into lowercase words, including numeric characters.

        Args:
            text (str): The string to tokenize.

        Returns:
            list: A list of lowercase words from the string.
        """
        return re.findall(r'\b\w+\b', text.lower())

    @staticmethod
    def vectorize(text, vocabulary):
        """
        Converts a text into a vector based on a given vocabulary (bag of words).

        Args:
            text (str): The product name to vectorize.
            vocabulary (list): The list of all unique words across product names.

        Returns:
            list: A vector representing the frequency of words from the vocabulary in the text.
        """
        word_count = Counter(MatchingUtils.tokenize(text))
        return [word_count.get(word, 0) for word in vocabulary]

    @staticmethod
    def cosine_similarity(vec1, vec2):
        """
        Computes the cosine similarity between two vectors.

        Args:
            vec1 (list): First vector.
            vec2 (list): Second vector.

        Returns:
            float: The cosine similarity between vec1 and vec2.
        """
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude_vec1 = math.sqrt(sum(a**2 for a in vec1))
        magnitude_vec2 = math.sqrt(sum(b**2 for b in vec2))

        if magnitude_vec1 == 0 or magnitude_vec2 == 0:
            return 0.0

        return dot_product / (magnitude_vec1 * magnitude_vec2)

    @staticmethod
    def get_best_match(query, products):
        """
        Finds the product with the highest cosine similarity to the query and returns the percentage similarity.

        Args:
            query (str): The product name to search for.
            products (list): The list of products from Grocy, each with a 'name' field.

        Returns:
            dict: The product with the highest similarity to the query and its percentage similarity.
        """
        all_product_names = [product['name'] for product in products]
        all_words = set(word for name in all_product_names for word in MatchingUtils.tokenize(name))
        vocabulary = list(all_words)

        query_vector = MatchingUtils.vectorize(query, vocabulary)

        best_match = None
        highest_similarity = -1
        for product in products:
            product_vector = MatchingUtils.vectorize(product['name'], vocabulary)
            similarity = MatchingUtils.cosine_similarity(query_vector, product_vector)

            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = product

        # Convert similarity to percentage
        similarity_percentage = highest_similarity * 100

        if best_match:
            return {
                'product': best_match,
                'similarity_percentage': similarity_percentage
            }

        return None
