def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    # TODO
    album = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            linee = f.readlines()
            for linea in linee[1:]:
                campi = linea.strip().split(',')
                if len(campi) == 5:
                    codice = campi[0].strip()
                    titolo = campi[1].strip()
                    autore = campi[2].strip()
                    mese = int(campi[3].lstrip())
                    anno = int(campi[4].strip())
                    foto= {
                        "codice" : codice,
                        "titolo" : titolo,
                        "mese" : mese,
                        "anno" : anno
                    }

                    anno_trovato = False
                    for blocco in album:
                        if blocco[0] == anno:
                            blocco[1].append(foto)
                            anno_trovato = True
                            break
                    if not anno_trovato:
                        nuovo_blocco = [anno,[foto]]
                        album.append(nuovo_blocco)
        return album
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # TODO
    if not (1<= mese <= 12):
        return None

    if cerca_foto(album, codice) is not None:
        return None

    foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese,
        "anno": anno
    }
    anno_trovato = False
    for blocco in album:
        if blocco[0] == anno:
            blocco[1].append(foto)
            anno_trovato = True
            break

    if not anno_trovato:
        album.append([anno, [foto]])

    # Aggiorno il file aggiungendo la nuova riga in fondo
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n{codice},{titolo},{autore},{mese},{anno}")
        return foto
    except FileNotFoundError:
        return None

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    # TODO
    for blocco in album:
        for foto in blocco[1]:
            if foto["codice"] == codice:
                return f"{foto['codice']}, {foto['titolo']}, {foto['autore']}, {foto['mese']}, {foto['anno']}"
    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    # TODO
    for blocco in album:
        if blocco[0] == anno:
            titoli = [foto["titolo"] for foto in blocco[1]]
            titoli.sort()
            return titoli
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    print("Album caricato con successo.")
                    break
                else:
                    print("File non trovato. Riprova.")
        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto (codice duplicato, mese non valido o file non trovato).")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
