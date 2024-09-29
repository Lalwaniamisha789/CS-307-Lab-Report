import re
import nltk
import numpy as np
from nltk.tokenize import sent_tokenize
from queue import PriorityQueue

nltk.download('punkt')

# Function to preprocess the text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Tokenize into sentences
    sentences = sent_tokenize(text)
    return sentences

# Get sentences from user
document1 = input("Enter the first document (two sentences): ")
document2 = input("Enter the second document (two sentences): ")

preprocessed_doc1 = preprocess_text(document1)
preprocessed_doc2 = preprocess_text(document2)

print("Preprocessed Document 1:", preprocessed_doc1)
print("Preprocessed Document 2:", preprocessed_doc2)

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    
    return dp[m][n]

# Example usage
sentence1 = "This is a test"
sentence2 = "This is an example"
distance = levenshtein_distance(sentence1, sentence2)
print("Edit Distance:", distance)

# Define a class to represent the search state
class State:
    def __init__(self, doc1_idx, doc2_idx, cost, path):
        self.doc1_idx = doc1_idx  # Current index in document 1
        self.doc2_idx = doc2_idx  # Current index in document 2
        self.cost = cost          # g(n) - cumulative cost so far
        self.path = path          # The alignment path

    def __lt__(self, other):
        return self.cost < other.cost

# Heuristic function (estimate remaining cost)
def heuristic(doc1, doc2, doc1_idx, doc2_idx):
    # Use Levenshtein distance as a simple heuristic between next sentences
    if doc1_idx < len(doc1) and doc2_idx < len(doc2):
        return levenshtein_distance(doc1[doc1_idx], doc2[doc2_idx])
    return 0

# A* Search function
def a_star_alignment(doc1, doc2):
    frontier = PriorityQueue()
    initial_state = State(0, 0, 0, [])  # Start from the first sentences of both docs
    frontier.put((0, initial_state))  # (f(n), state)
    
    while not frontier.empty():
        _, current_state = frontier.get()
        doc1_idx = current_state.doc1_idx
        doc2_idx = current_state.doc2_idx
        
        # Goal state: All sentences aligned
        if doc1_idx == len(doc1) and doc2_idx == len(doc2):
            return current_state.path
        
        # Generate successors (align, skip in doc1, skip in doc2)
        if doc1_idx < len(doc1) and doc2_idx < len(doc2):
            # Align sentences from both documents
            align_cost = levenshtein_distance(doc1[doc1_idx], doc2[doc2_idx])
            align_state = State(doc1_idx + 1, doc2_idx + 1, current_state.cost + align_cost, current_state.path + [(doc1_idx, doc2_idx)])
            frontier.put((align_state.cost + heuristic(doc1, doc2, doc1_idx + 1, doc2_idx + 1), align_state))
        
        if doc1_idx < len(doc1):
            # Skip sentence in doc1
            skip_doc1_state = State(doc1_idx + 1, doc2_idx, current_state.cost + 1, current_state.path + [(doc1_idx, None)])
            frontier.put((skip_doc1_state.cost + heuristic(doc1, doc2, doc1_idx + 1, doc2_idx), skip_doc1_state))
        
        if doc2_idx < len(doc2):
            # Skip sentence in doc2
            skip_doc2_state = State(doc1_idx, doc2_idx + 1, current_state.cost + 1, current_state.path + [(None, doc2_idx)])
            frontier.put((skip_doc2_state.cost + heuristic(doc1, doc2, doc1_idx, doc2_idx + 1), skip_doc2_state))

    return None  # In case no alignment is found

# Example usage
aligned_path = a_star_alignment(preprocessed_doc1, preprocessed_doc2)
print("Alignment Path:", aligned_path)

def detect_plagiarism(alignment_path, doc1, doc2, threshold=5):
    plagiarized_pairs = []
    for (i, j) in alignment_path:
        if i is not None and j is not None:
            distance = levenshtein_distance(doc1[i], doc2[j])
            if distance < threshold:
                plagiarized_pairs.append((doc1[i], doc2[j], distance))
    return plagiarized_pairs

# Example usage
plagiarism_results = detect_plagiarism(aligned_path, preprocessed_doc1, preprocessed_doc2)
for result in plagiarism_results:
    print("Doc1 Sentence:", result[0])
    print("Doc2 Sentence:", result[1])
    print("Edit Distance:", result[2])
    print()
