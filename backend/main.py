from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

# --- Modelos Pydantic ---
class Book(BaseModel):
    id: UUID
    title: str
    author: str
    illustrator: Optional[str] = None
    price: float
    description: str
    cover_image: str
    category: str           # e.g. "novedades", "bestsellers"
    age_group: str          # e.g. "0-3", "4-7", "8-12", "13+"
    bestseller: bool = False
    novelty: bool = False

class CartItem(BaseModel):
    book_id: UUID
    quantity: int = 1

# --- Datos de ejemplo ---
sample_books = [
    Book(
        id=uuid4(),
        title="El bosque mágico",
        author="Ana Pérez",
        illustrator="Juan López",
        price=950.0,
        description="Una aventura en el bosque para los más pequeños.",
        cover_image="/img/book1.jpeg",
        category="novedades",
        age_group="4-7",
        novelty=True
    ),
    Book(
        id=uuid4(),
        title="Las estrellas de papel",
        author="María García",
        illustrator="Luis Ramírez",
        price=1200.0,
        description="Cuentos que brillan como el cielo nocturno.",
        cover_image="/img/book2.jpeg",
        category="bestsellers",
        age_group="8-12",
        bestseller=True
    ),
    # ... añade más libros según tu base real ...
]

cart: List[CartItem] = []

# --- App FastAPI ---
app = FastAPI(title="API Del Naranjo")

# Permitir peticiones desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Servir estáticos (tu frontend)
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")

# --- Endpoints API ---

@app.get("/api/books", response_model=List[Book])
def list_books(
    category: Optional[str] = Query(None, description="novedades o bestsellers"),
    age: Optional[str] = Query(None, description="0-3, 4-7, 8-12, 13+"),
    search: Optional[str] = Query(None, description="texto en título o autor")
):
    results = sample_books
    if category:
        results = [b for b in results if b.category == category]
    if age:
        results = [b for b in results if b.age_group == age]
    if search:
        q = search.lower()
        results = [b for b in results if q in b.title.lower() or q in b.author.lower()]
    return results

@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: UUID):
    for b in sample_books:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@app.get("/api/recommendations", response_model=List[Book])
def get_recommendations(limit: int = 4):
    # Retorna los primeros "limit" como ejemplo
    return sample_books[:limit]

@app.post("/api/cart/add", response_model=List[CartItem])
def add_to_cart(item: CartItem):
    # chequea existencia
    if not any(b.id == item.book_id for b in sample_books):
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    # agrega al carrito (simple)
    cart.append(item)
    return cart
