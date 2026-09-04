from preprocess import tokenize
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import PorterStemmer

STOPWORDS_EN = set(nltk_stopwords.words("english"))
_stemmer = PorterStemmer()

def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS_EN]

def stem(tokens: list[str]) -> list[str]:
    return [_stemmer.stem(t) for t in tokens]

if __name__ == "__main__":

    sample_text = ( "The man discovered that the plagiarism was discovered in the  documents while discovering other plagiarized documents.")
    tokens = tokenize(sample_text) 
    filtered = remove_stopwords(tokens)
    stemmed = stem(filtered)

    print(f"Texto original: {sample_text}")
    print(f"Tokens (abordagem A): {tokens}")
    print(f"Sem stopwords: {filtered}")
    print(f"Após stemming: {stemmed}")