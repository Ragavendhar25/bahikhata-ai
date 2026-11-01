from rapidfuzz import process, fuzz
from models import LedgerEntry

def correct_item(item, db):
    rows = db.query(LedgerEntry.item).distinct().all()
    known = [r[0] for r in rows if r[0]]
    if not known:
        return item
    match = process.extractOne(item.lower(), [k.lower() for k in known],
                               scorer=fuzz.WRatio, score_cutoff=80)
    if match:
        return known[match[2]]
    return item