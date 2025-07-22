# modelo_recomendación.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
spanish_stop = stopwords.words('spanish')

# 1. Cargar datos
DATA_PATH = "D:/del_naranjo/delnaranjo_products.csv"
df = pd.read_csv(DATA_PATH)

# 2. Preprocesamiento
if 'description' in df.columns:
    df['text'] = df['description'].fillna('') + ' ' + df['title'].fillna('')
else:
    df['text'] = df['title'].fillna('')

# 3. Vectorización
vectorizer = TfidfVectorizer(stop_words=spanish_stop)
tfidf_matrix = vectorizer.fit_transform(df['text'])

# 4. Función base
def recomendar_por_texto(query, top_n=5):
    query_vec = vectorizer.transform([query])
    sim_scores = cosine_similarity(query_vec, tfidf_matrix)[0]
    indices = np.argsort(sim_scores)[::-1][:top_n]
    return df.loc[indices, ['id', 'title']]

# 5. Función que usará FastAPI
def get_recommendations(product_id: str, top_n: int = 4) -> list[str]:
    """
    Devuelve una lista de product_id recomendados, basado
    en similitud de texto con el producto dado.
    """
    # 5.1. Obtener el texto del producto fuente
    row = df.loc[df['id'] == product_id]
    if row.empty:
        return []
    query = row['text'].values[0]
    # 5.2. Obtener recomendaciones
    recs = recomendar_por_texto(query, top_n=top_n + 1)  # +1 porque incluye la misma
    # 5.3. Filtrar para quitar el mismo ID
    recs = recs[recs['id'] != product_id].head(top_n)
    return recs['id'].tolist()


# 6. Prueba local
if __name__ == "__main__":
    ejemplo = df['id'].iloc[0]
    print("Recs para", ejemplo, "→", get_recommendations(ejemplo))
