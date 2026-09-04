from preprocess import tokenize
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import PorterStemmer

STOPWORDS_EN = set(nltk_stopwords.words("english")) # definição de stopwords em inglês
_stemmer = PorterStemmer() # instância do stemmer para reduzir palavras à sua raiz

# Função para remover stopwords do texto
def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in STOPWORDS_EN]

# Função para aplicar stemming às palavras do texto
def stem(tokens: list[str]) -> list[str]:
    return [_stemmer.stem(t) for t in tokens]

# Função para pré-processar o texto: tokenização, remoção de stopwords e stemming
def preprocess_b(text: str) -> list[str]:

    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = stem(tokens)
    return tokens

if __name__ == "__main__":
  
    sample_text = ("The man discovered that the plagiarism was discovered in the documents while discovering other plagiarized documents.")
    tokens = tokenize(sample_text)
    filtered = remove_stopwords(tokens)
    stemmed = stem(filtered)

    print(f"Texto original: {sample_text}")
    print(f"Tokens (abordagem A): {tokens}")
    print(f"Sem stopwords: {filtered}")
    print(f"Após stemming: {stemmed}")
    print(f"\npreprocess_b() direto: {preprocess_b(sample_text)}")