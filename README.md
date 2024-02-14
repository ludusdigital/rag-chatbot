
# RAG Chatbot sa Streamlit-om

## Opis

RAG chatbot je aplikacija zasnovana na Streamlit-u koja koristi LLaMA indeks i OpenAI za stvaranje interaktivnog chatbota. Korisnici mogu postavljati pitanja, a aplikacija generiše odgovore koristeći unapred definisanu bazu znanja. Idealan je za pružanje specijalizovanih odgovora u različitim domenima, omogućavajući korisnicima da brzo pristupe informacijama koje su im potrebne.

## Funkcionalnosti

- Učitavanje i indeksiranje dokumentacije iz određenog direktorijuma.
- Generisanje odgovora na pitanja korisnika pomoću LLaMA indeksa i GPT-3.5 Turbo modela.
- Chat interfejs za postavljanje pitanja i prikazivanje odgovora sa prilagođenim avatarima.

## Instalacija

Da biste pokrenuli ovu aplikaciju, potrebno je da imate Python instaliran na vašem računaru. Aplikacija zahteva instalaciju nekoliko zavisnosti, koje su navedene u `requirements.txt` fajlu.

1. Klonirajte repozitorijum ili preuzmite izvorni kod aplikacije.
2. Otvorite terminal i navigirajte do direktorijuma aplikacije.
3. Instalirajte potrebne pakete koristeći:

```bash
pip install -r requirements.txt
```

4. Pokrenite Streamlit aplikaciju komandom:

```bash
streamlit run your_app_name.py
```

Zamenite `your_app_name.py` sa imenom Python skripte koju ste preuzeli ili kreirali.

## Konfiguracija

Da biste koristili aplikaciju, potrebno je da konfigurišete sledeće:

- Postavite svoj OpenAI API ključ u `st.secrets` za autentikaciju prilikom generisanja odgovora. Ovo možete učiniti kreiranjem `.streamlit/secrets.toml` fajla i dodavanjem vašeg ključa:
  
```toml
openai_key="Vaš_OpenAI_API_ključ"
```

- Pripremite bazu znanja koja će biti korišćena za generisanje odgovora, smeštajući dokumente u `./data` direktorijum.

## Korišćenje

Nakon pokretanja aplikacije, otvoriće se web interfejs u vašem pretraživaču. Možete početi da postavljate pitanja u chat input polju. Aplikacija će automatski generisati odgovore koristeći vašu bazu znanja i prikazati ih u chat prozoru.


