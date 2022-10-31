# # # ###########################################
# Laden der Fremdbibliotheken
# # # ###########################################

from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

console = Console()

# # # ###########################################
# Bitte nicht verändern!
# Datenbank Kram!
# Erzeugen einer neuen Datenbank Engine
rueckgabewert_db_erstellt = create_engine("sqlite:///fazebook.db")

# Basisklasse für Klassen
Hauptdatenbank = declarative_base()

# Öffne Verbindung zur Datenbank
Session = sessionmaker(bind=rueckgabewert_db_erstellt)

# Offene Verbindung zur Datenbank
session = Session()
# # # ###########################################

class C_Adressen(Hauptdatenbank):
    __tablename__ = "adressen"
    db_a_id = Column(Integer, primary_key=True)
    db_a_strasse = Column(String)
    db_a_hausnummer = Column(String)
    db_a_plz = Column(String)
    db_a_ort = Column(String)

class C_Berufe(Hauptdatenbank):
    __tablename__ = "berufe"
    db_b_id = Column(Integer, primary_key=True)
    db_b_beruf = Column(String)

class C_Emailadressen(Hauptdatenbank):
    __tablename__ = "emailadressen"
    db_e_id = Column(Integer, primary_key=True)
    db_e_emailadresse = Column(String)

class C_Fazebook(Hauptdatenbank):
    __tablename__ = "fazebook"
    db_f_id = Column(Integer, primary_key=True)
    db_f_vorname = Column(String)
    db_f_nachname = Column(String)
    db_f_bemerkung = Column(String)
    db_f_geburtsdatum = Column(String)

    # Foreignkeys
    db_f_sprache_id = Column(Integer, ForeignKey("sprachen.db_s_id"))
    db_f_hobby_id = Column(Integer, ForeignKey("hobbys.db_h_id"))
    db_f_beruf_id = Column(Integer, ForeignKey("berufe.db_b_id"))
    db_f_telefonnummer_id = Column(Integer, ForeignKey("telefonnummern.db_t_id"))
    db_f_emailadresse_id = Column(Integer, ForeignKey("emailadressen.db_e_id"))
    db_f_adresse_id = Column(Integer, ForeignKey("adressen.db_a_id"))
    
    def __repr__(self) -> str:
        return f"{self.db_f_vorname} {self.db_f_nachname}"

class C_Hobbys(Hauptdatenbank):
    __tablename__ = "hobbys"
    db_h_id = Column(Integer, primary_key=True)
    db_h_hobby = Column(String)

class C_Sprachen(Hauptdatenbank):
    __tablename__ = "sprachen"
    db_s_id = Column(Integer, primary_key=True)
    db_s_sprache = Column(String)

class C_Telefonnummern(Hauptdatenbank):
    __tablename__ = "telefonnummern"

    db_t_id = Column(Integer, primary_key=True)
    db_t_telefonnummer = Column(String)

def F_Init_Datenbank():
    """
    Init die Datenbanken und erstelle alle Tabellen.

    See more here: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """
    Hauptdatenbank.metadata.create_all(rueckgabewert_db_erstellt)


def F_Datenbank_add_Freund(freund: C_Fazebook):
    """
    Database command to add a new freund.
    """
    session.add(freund)
    session.commit()

def F_neuer_freund():
    l_vorname = input("Bitte geben den Vornamen an\t: ")
    l_nachname = input("Bitte geben den Nachnamen an\t: ")
    l_bemerkung = input("Bitte geben eine Bemrkungen ein\t: ")
    l_geburtsdatum = input("Bitte geben den Geburtstag an\t: ")
    l_neuer_freund = C_Fazebook(db_f_vorname=l_vorname, db_f_nachname=l_nachname, db_f_bemerkung=l_bemerkung, db_f_geburtsdatum=l_geburtsdatum)
    F_Datenbank_add_Freund(l_neuer_freund)

def F_Datenbank_hole_alle_freunde():
    """
    Database command to get all f_freunde.
    """
    return session.query(C_Fazebook).all()

def F_hole_freund(f_f_freund_id: int):
    """
    Database command to get one friend by ID.
    """
    return session.query(C_Fazebook).get(f_f_freund_id)
    
def F_loesche_freund():
    f_freund_id = int(input("Bitte gebe die ID des Freundes an: "))
    f_freund = F_hole_freund(f_freund_id)
    console.print(f"Lösche Freund {f_freund.db_f_vorname} {f_freund.db_f_nachname}.", style="red")
    session.delete(f_freund)
    session.commit()

def F_Zeige_alle_freunde():
    f_freunde = F_Datenbank_hole_alle_freunde()
    table = Table(show_header=True, header_style="bold green")
    table.add_column("db_f_id", style="dim")
    table.add_column("db_f_vorname")
    table.add_column("db_f_nachname")
    table.add_column("db_f_bemerkung")
    table.add_column("db_f_geburtsdatum")
    
    for f_freund in f_freunde:
        table.add_row(str(f_freund.db_f_id), f_freund.db_f_vorname, f_freund.db_f_nachname, f_freund.db_f_bemerkung, f_freund.db_f_geburtsdatum)

    console.print(table)

def F_veraendere_ein_freund():
    f_freund_id = int(input("Bitte gebe die ID des Freundes an: "))
    f_freund = F_hole_freund(f_freund_id)
    f_freund_felder = {}
    
    # Test
    print({f_freund_felder.db_f_vorname})
    print(f"Vorname \t[{f_freund_felder.db_f_vorname }]: ")
    # Test

    f_neuer_wert_vorname = input(f"Vorname \t[{f_freund_felder.db_f_vorname }]: ")
    if f_neuer_wert_vorname:
        f_freund_felder["f_freund_felder.db_f_vorname"] = f_neuer_wert_vorname

    f_neuer_wert_nachname = input(f"Nachname \t[{f_freund_felder.db_f_nachname}]: ")
    if f_neuer_wert_nachname:
        f_freund_felder["f_freund_felder.db_f_nachname"] = f_neuer_wert_nachname

    f_neuer_wert_bemerkung = input(f"Bewwertung \t[{f_freund_felder.db_f_bemerkung}]: ")
    if f_neuer_wert_bemerkung:
        f_freund_felder["f_freund_felder.db_f_bewertung"] = f_neuer_wert_bemerkung

    f_neuer_wert_geburtsdatum = input(f"Geburtstag \t[{f_freund_felder.db_f_geburtsdatum}]: ")
    if f_neuer_wert_geburtsdatum:
        f_freund_felder["f_freund_felder.db_f_geburtstagdatum"] = f_neuer_wert_geburtsdatum
  

    console.print(f"\nVerändere Freund {f_freund_felder.db_f_vorname} {f_freund_felder.db_f_nachname}\nVeränderte Bemerkung \t {f_freund_felder.db_f_bemerkung}\nVeränderter Geburtstag \t {f_freund_felder.db_f_geburtstagdatum}.", style="green")
    rueckgabewert_db_erstellt(f_freund, f_freund_felder)


# # # ###########################################
# # # Main
# # # ###########################################
if __name__ == "__main__":
    F_Init_Datenbank()

g_schleife=True

while g_schleife:
    print("""
    ----------------------------------------
    Menu: 
    - (A)nlegen eine neuen Freundes
    - (V)erändern eines Freundes
    - (L)öschen alle Freunde
    - (Z)eige alle Freunde
    - (E)nde des Programmes
    ----------------------------------------
    """)

    g_menuauswahl = input("Wähle bitte (A) (V) (L) (Z) oder (E): ")
    g_menuauswahl = g_menuauswahl.upper()
    
    if g_menuauswahl == "A":
        F_neuer_freund()
    elif g_menuauswahl == "V":
        F_veraendere_ein_freund()
    elif g_menuauswahl == "L":
        F_loesche_freund()
    elif g_menuauswahl == "Z":
        F_Zeige_alle_freunde()
    elif g_menuauswahl == "E":
        g_schleife=False
    else:
        continue

######################
