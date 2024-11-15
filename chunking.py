import nltk
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity
import torch


nltk.download('punkt')
nltk.download('punkt_tab')

def get_sentence_embeddings(sentences):
    # Load pretrained model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Tokenize sentences and get embeddings
    inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Average pooling
    
    return embeddings

def split_text_by_context(text, similarity_threshold=0.5, max_sentences_per_section=5, min_sentences_per_section=2):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    sentence_embeddings = get_sentence_embeddings(sentences)

    sections = []
    current_section = [sentences[0]]
    current_section_embedding = sentence_embeddings[0].unsqueeze(0)  # Initial embedding of the first sentence

    for i in range(1, len(sentences)):
        sentence_embedding = sentence_embeddings[i].unsqueeze(0)
        similarity = cosine_similarity(current_section_embedding, sentence_embedding).item()

        # Check if the section should end based on length and similarity threshold
        if (len(current_section) >= max_sentences_per_section or similarity < similarity_threshold) and len(current_section) >= min_sentences_per_section:
            sections.append(" ".join(current_section))
            current_section = [sentences[i]]
            current_section_embedding = sentence_embedding  # Reset embedding for the new section
        else:
            # Add sentence to the current section
            current_section.append(sentences[i])
            # Update the section embedding (average of section embeddings)
            current_section_embedding = torch.mean(torch.stack([current_section_embedding, sentence_embedding]), dim=0)

    # Append the last section if it has at least 2 sentences
    if len(current_section) >= min_sentences_per_section:
        sections.append(" ".join(current_section))
    
    return sections

# Example usage
book_text = """Your full book text goes here. Replace this with the actual text."""
sections = split_text_by_context(book_text, similarity_threshold=0.5, max_sentences_per_section=5, min_sentences_per_section=1)
for i, section in enumerate(sections):
    print(f"Section {i+1}:\n{section}\n")
