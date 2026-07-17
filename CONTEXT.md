# Extract Expenses

Traccia e categorizza i movimenti bancari personali (Poste, BBVA, altri conti) per produrre una dashboard di monitoraggio spese/entrate.

## Language

**Transazione**:
Un singolo movimento bancario: data, importo, descrizione, banca di origine, e tipologia (Entrata o Uscita). È il dato grezzo, unica fonte di verità nel DB.
_Avoid_: Movimento (usato nei file Excel sorgente, ma nel codice/UI si usa Transazione)

**Tipologia** (Entrata / Uscita):
Distingue se una Transazione è un accredito (Entrata) o un addebito (Uscita), in base al segno dell'importo originale.
_Avoid_: Tipo di spesa, categoria — concetti distinti, vedi Categoria

**Categoria**:
Classificazione tematica di una Transazione di tipo Uscita (es. salute, casa, spesa, shopping, hobby, viaggi, fitness, auto, tasse, contanti, other), assegnata tramite fuzzy matching sulla descrizione. Calcolata al volo a partire dalle regole correnti, non persistita nel DB. Si applica solo alle Uscite, non alle Entrate.
_Avoid_: Tipologia (riservato a Entrata/Uscita)

**Banca**:
La fonte/conto bancario di una Transazione: Poste, BBVA, o Others (conti minori aggregati). Ogni banca ha un proprio formato di export Excel e un proprio parser.

**Trasferimento cross-bank**:
Una coppia di Transazioni (una Uscita, una Entrata) con stesso importo, banche diverse, e date entro 7 giorni l'una dall'altra — rappresenta uno spostamento di denaro tra propri conti, non una spesa o un'entrata reale. Va escluso dai totali di spese/entrate. Calcolato al volo dalla tabella Transazioni grezza, e materializzato in una tabella cache separata (ricostruita ad ogni caricamento batch e ad ogni avvio dell'app) a scopo di debug.

**Caricamento (Upload Batch)**:
Un evento di importazione di un file Excel per una singola Banca, tracciato con un identificativo, timestamp, banca selezionata e nome del file sorgente. Permette di annullare l'inserimento di un caricamento errato.
