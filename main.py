from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import Customer, LedgerEntry
from fastapi import UploadFile, File, Form
from ai_parser import parse_entry, transcribe
from fastapi.responses import FileResponse
from corrector import correct_item

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CustomerIn(BaseModel):
    name: str
    phone: str

@app.get("/")
def home():
    return {"message": "BahiKhata.AI is running"}

@app.post("/customers")
def add_customer(data: CustomerIn, db: Session = Depends(get_db)):
    c = Customer(name=data.name, phone=data.phone)
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"id": c.id, "name": c.name, "phone": c.phone}

@app.get("/customers")
def list_customers(db: Session = Depends(get_db)):
    return [{"id": c.id, "name": c.name, "phone": c.phone} for c in db.query(Customer).all()]

class PurchaseIn(BaseModel):
    customer_id: int
    item: str
    quantity: float
    price: float

class PaymentIn(BaseModel):
    customer_id: int
    amount: float

@app.post("/purchase")
def add_purchase(data: PurchaseIn, db: Session = Depends(get_db)):
    e = LedgerEntry(customer_id=data.customer_id, entry_type="purchase",
                    item=data.item, quantity=data.quantity, price=data.price,
                    total=data.quantity * data.price)
    db.add(e)
    db.commit()
    return {"message": "saved", "total": e.total}

@app.post("/payment")
def add_payment(data: PaymentIn, db: Session = Depends(get_db)):
    e = LedgerEntry(customer_id=data.customer_id, entry_type="payment",
                    total=data.amount)
    db.add(e)
    db.commit()
    return {"message": "payment saved"}

@app.get("/customers/{customer_id}/balance")
@app.get("/customers/{customer_id}/balance")
def balance(customer_id: int, db: Session = Depends(get_db)):
    entries = db.query(LedgerEntry).filter(LedgerEntry.customer_id == customer_id).all()
    bought = sum(e.total for e in entries if e.entry_type == "purchase")
    paid = sum(e.total for e in entries if e.entry_type == "payment")
    due = bought - paid
    return {"bought": bought, "paid": paid, "balance_due": due,
            "status": "advance" if due < 0 else "due" if due > 0 else "settled"}


class TextIn(BaseModel):
    customer_id: int
    text: str
@app.post("/ai-entry")
def ai_entry(data: TextIn, db: Session = Depends(get_db)):
    p = parse_entry(data.text)
    p["item"] = correct_item(p["item"], db)      # <-- NEW LINE
    e = LedgerEntry(customer_id=data.customer_id, entry_type="purchase",
                    item=p["item"], quantity=p["quantity"], price=p["price"],
                    total=p["quantity"] * p["price"])
    db.add(e)
    db.commit()
    return {"parsed": p, "total": e.total}
@app.post("/voice-entry")
async def voice_entry(customer_id: int = Form(...),
                      language: str = Form(None),
                      audio: UploadFile = File(...),
                      db: Session = Depends(get_db)):
    audio_bytes = await audio.read()
    text = transcribe(audio.filename, audio_bytes, language or None)
    p = parse_entry(text)
    p["item"] = correct_item(p["item"], db)     # <-- NEW LINE
    e = LedgerEntry(customer_id=customer_id, entry_type="purchase",
                    item=p["item"], quantity=p["quantity"], price=p["price"],
                    total=p["quantity"] * p["price"])
    db.add(e)
    db.commit()
    return {"heard": text, "parsed": p, "total": e.total}


@app.get("/recorder")
def recorder():
    return FileResponse("recorder.html")
