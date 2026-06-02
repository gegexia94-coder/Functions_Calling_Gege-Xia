from typing import Optional


class DesignServiceTool:
    def __init__(self):
        self.services = {
            "camera": {
                "name": "Consulenza camera",
                "description": "Studio colori, letto, armadio, luci e zona relax.",
                "duration": "60 minuti",
                "price": 90,
            },
            "soggiorno": {
                "name": "Consulenza soggiorno",
                "description": "Layout divano, TV, libreria, luci e zona conversazione.",
                "duration": "75 minuti",
                "price": 110,
            },
            "cucina": {
                "name": "Consulenza cucina",
                "description": "Distribuzione, materiali, piano lavoro e illuminazione.",
                "duration": "90 minuti",
                "price": 130,
            },
        }

    def get_service_info(self, room_type: str) -> str:
        key = room_type.lower().strip()
        service = self.services.get(key)

        if not service:
            return f"Servizio non trovato. Stanze disponibili: {list(self.services.keys())}"

        return (
            f"Servizio: {service['name']}\n"
            f"Descrizione: {service['description']}\n"
            f"Durata: {service['duration']}\n"
            f"Prezzo: €{service['price']}"
        )


class MaterialSuggestionTool:
    def __init__(self):
        self.materials = {
            "japandi": ["legno chiaro", "lino", "microcemento", "vetro satinato"],
            "moderno caldo": ["rovere", "tessuti bouclé", "ottone spazzolato", "pittura sabbia"],
            "minimal": ["bianco caldo", "gres grande formato", "metallo nero", "vetro trasparente"],
        }

    def suggest_materials(self, style: str) -> str:
        key = style.lower().strip()
        materials = self.materials.get(key)

        if not materials:
            return f"Stile non trovato. Stili disponibili: {list(self.materials.keys())}"

        return f"Materiali consigliati per stile {style}: {', '.join(materials)}"


class ConsultationBookingTool:
    def __init__(self):
        self.slots = [
            {"designer_id": "D001", "name": "Designer Marta", "date": "2026-06-05", "time": "10:00"},
            {"designer_id": "D002", "name": "Designer Luca", "date": "2026-06-06", "time": "15:30"},
            {"designer_id": "D003", "name": "Designer Elena", "date": "2026-06-10", "time": "11:00"},
        ]

    def book_consultation(self, date: str, time: str, designer_id: Optional[str] = None) -> str:
        available = [slot for slot in self.slots if slot["date"] == date and slot["time"] == time]

        if designer_id:
            available = [slot for slot in available if slot["designer_id"] == designer_id]

        if not available:
            return f"Nessuna disponibilità trovata. Slot disponibili: {self.slots}"

        slot = available[0]
        return f"Prenotazione confermata con {slot['name']} il {slot['date']} alle {slot['time']}."
