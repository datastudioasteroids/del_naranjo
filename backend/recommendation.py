from pathlib import Path
import sys
# app/recommendation.py
from modelo_recomendación import get_recommendations
# Ajustamos el path para importar tu módulo existente
BACKEND_ROOT = Path(__file__).parent.parent
sys.path.append(str(BACKEND_ROOT))

# Importamos tu script de recomendaciones
from modelo_recomendación import get_recommendations  # asumiendo que exporta esta función

def recommend(product_id: str, top_n: int = 4):
    """
    Llama a tu función de modelo para obtener recomendaciones.
    Debe devolver una lista de IDs de producto.
    """
    return get_recommendations(product_id, top_n)
