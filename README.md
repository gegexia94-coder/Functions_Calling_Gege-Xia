# Design Assistant Tools

Mini assistente AI per consulenze di interior design.

Il progetto replica la logica della video-lezione sul Function Calling:
- l'utente fa una domanda
- il modello decide se chiamare un tool
- Python esegue il tool
- il modello costruisce una risposta finale

Dominio scelto: interior design.


Questo progetto replica la logica della video-lezione sul Function Calling.

Dominio scelto: consulenze di interior design.

L'assistente può usare 3 tool:

1. `get_design_service_info`
   - restituisce informazioni su consulenze per camera, soggiorno o cucina

2. `suggest_materials`
   - suggerisce materiali in base allo stile richiesto

3. `book_consultation`
   - simula la prenotazione di una consulenza con un designer

## Esempi di domande

- Che servizio avete per una camera?
- Consigliami materiali per stile japandi.
- Prenota una consulenza il 2026-06-05 alle 10:00.
...................................
