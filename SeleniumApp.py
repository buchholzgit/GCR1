import streamlit as st
import pandas as pd


def StationärCrawler(Gemeinde, Umkreis, Anzahl, User, Fahrzeitberechnung: bool):
    import os
    import os.path
    import time
    import selenium
    import pandas as pd
    import numpy as np
    import streamlit as st
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager

    pd.set_option("display.max_rows", None, "display.max_columns", None)


    # -----------------------------------
    user = User
    # Suchkriterien
    PLZ = Gemeinde  #Längere Listen sind möglich. Sowohl PLZ als auch Ortsangabe ist möglich.
    Umkreis = Umkreis  # in km. Bezieht sich auf alle in PLZ_Liste genannten Orte. Mögliche Werte: 5, 10, 15, 25, 50
    AnzahlEinrichtungen = int(Anzahl)  #Code versucht x Pflegedienste zu finden. In 10er Schritten.
    # -----------------------------------

    # Webdriver Setup
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    chrome_options.add_experimental_option("prefs", {"download.prompt_for_download": False, "download.directory_upgrade": True, "plugins.always_open_pdf_externally": True})

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # Listen Setup
    Such_PLZ = []
    Einrichtungen = []
    Entfernungen = []
    Adressen = []
    Telefon = []
    Websites = []
    Emails = []
    Anteile_PG1_ohneIK = []
    Anteile_PG2_ohneIK = []
    Investitionskosten = []
    Plätze = []
    davon_KZP = []
    davon_Einzelzimmer = []
    davon_Doppelzimmer = []
    Fahrtdauer = []
    Fahrtstrecke = []
    Unterkunftskosten = []
    Verpflegungskosten = []

    driver.get("https://pflegelotse.de")
    time.sleep(0.5)
    driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/a[2]/span").click()
    try:
        driver.find_element(By.CLASS_NAME, "okButtonCookie").click()
    except NoSuchElementException:
        pass
    Auswahl_Button1 = driver.find_element(By.CSS_SELECTOR, "button:nth-child(1)")
    Auswahl_Button1.click()
    time.sleep(0.2)  # Wichtig, damit sich untere Felder öffnen können.
    Auswahl_Button2 = driver.find_element(By.XPATH, '//*[@id="ctl00_MasterBody"]/main/section[2]/div/div/button[1]')
    Auswahl_Button2.click()
    time.sleep(0.2)  # Wichtig, damit sich untere Felder öffnen können.
    Auswahl_Button3 = driver.find_element(By.ID,
        "ctl00_ContentPlaceHolder1_suche_btn_versorgung2"
    )
    Auswahl_Button3.click()
    time.sleep(0.2)  # Wichtig, damit sich untere Felder öffnen können.
    Auswahl_Button4 = driver.find_element(By.ID,
        "ctl00_ContentPlaceHolder1_suche_btn_pflegeart1"
    )
    Auswahl_Button4.click()
    Input_Feld1 = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_suche_bezirk")
    Input_Feld1.send_keys(PLZ)
    time.sleep(0.75)  # Wichtig, damit sich Dropdown für Ortsauswahl öffnet.
    Input_Feld1.send_keys(Keys.ENTER)
    Auswahl_Umkreis = driver.find_element(By.XPATH,
        "//*[@id='ctl00_ContentPlaceHolder1_suche_umkreis']/option[@value={}]".format(
            Umkreis
        )
    )
    Auswahl_Umkreis.click()
    Suche_Button = driver.find_element(By.ID,
        "ctl00_ContentPlaceHolder1_suche_btn_suche"
    )
    Suche_Button.click()
    time.sleep(1)


    AnzahlErgebnisse = int(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_count_results_header").text.split(" ")[0])
    print(AnzahlErgebnisse)
    ProgressBar = st.progress(0)


    GefAnzahl = 0
    i = 0
    j = 1


    while i <= 9:
        try:
            Distance = driver.find_element(By.XPATH,
                "//*[@id='results_vollstationaer']/tbody/tr[{}]/td[2]".format(i + 1)).text
            Distance1 = Distance.split(" ", 1)[0]
            Entfernungen.append(Distance1)
            Res = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_lvDesktopVollstationaer_ctrl{}_DetailButton".format(
                    i
                )
            )
            Res.click()
        except NoSuchElementException:
            time.sleep(2)
            try:
                Distance = driver.find_element(By.XPATH,
                    "//*[@id='results_vollstationaer']/tbody/tr[{}]/td[2]".format(
                        i + 1)
                ).text
                Distance1 = Distance.split(" ", 1)[0]
                Entfernungen.append(Distance1)
                Res = driver.find_element(By.ID,
                    "ctl00_ContentPlaceHolder1_lvDesktopVollstationaer_ctrl{}_DetailButton".format(
                        i
                    )
                )
                Res.click()
            except NoSuchElementException:
                print(
                    "Nur",
                    GefAnzahl,
                    "Einrichtungen im Ort",
                    PLZ,
                    "und Umkreis",
                    Umkreis,
                    "km gefunden.",
                )
                break
        time.sleep(0.5)
        try:
            Einrichtung = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_h2_name_header"
            ).text
        except NoSuchElementException:
            try:
                time.sleep(1.0)
                Einrichtung = driver.find_element(By.ID,
                    "ctl00_ContentPlaceHolder1_h2_name_header"
                ).text
            except NoSuchElementException:
                time.sleep(10.0)
                Einrichtung = driver.find_element(By.ID,
                    "ctl00_ContentPlaceHolder1_h2_name_header"
                ).text
            except NoSuchElementException:
                time.sleep(20.0)
                Einrichtung = driver.find_element(By.ID,
                    "ctl00_ContentPlaceHolder1_h2_name_header"
                ).text
        Einrichtungen.append(Einrichtung)
        Such_PLZ.append(PLZ)
        Adresse = driver.find_element(By.ID,
            "ctl00_ContentPlaceHolder1_p_adresse_header"
        ).text
        try:
            Tel = Adresse.split("\n", 2)[2].split("Tel.: ", 1)[1]
        except IndexError:
            Tel = "_"
        if Tel[0] == "0":
            Tel = Tel
        elif Tel[0] == "(":
            Tel = Tel
        else:
            Tel = "_"
        Telefon.append(Tel)
        Adressen.append(Adresse)

        try:
            Website = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_a_webseite_header"
            ).text
        except NoSuchElementException:
            Website = "_"
        Websites.append(Website)
        try:
            Email = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_a_mail_header"
            ).text
        except NoSuchElementException:
            Email = "_"
        Emails.append(Email)
        try:
            PlatzzahlString = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_p_details_pflegeeinrichtung_platzzahl").text
            print(PlatzzahlString)
            if "Gesamt" in PlatzzahlString:
                try:
                    Platzzahl = int(PlatzzahlString.split("Gesamt: ")[1].split("\n")[0])
                except IndexError:
                    int(PlatzzahlString.split("Gesamt: ")[1])
            else:
                Platzzahl = "_"
            if "Kurzzeitpflege" in PlatzzahlString:
                try:
                    KZP_Plätze = int(PlatzzahlString.split("davon Anzahl der Plätze für Kurzzeitpflege: ")[1].split("\n")[0])
                except IndexError:
                    KZP_Plätze = int(PlatzzahlString.split("davon Anzahl der Plätze für Kurzzeitpflege: ")[1])
            else:
                KZP_Plätze = "_"
            if "Einzel" in PlatzzahlString:
                try:
                    Einzelzimmerplätze = int(PlatzzahlString.split("davon Anzahl der Plätze in Einzelzimmern: ")[1].split("\n")[0])
                except IndexError:
                    Einzelzimmerplätze = int(PlatzzahlString.split("davon Anzahl der Plätze in Einzelzimmern: ")[1])
            else:
                Einzelzimmerplätze = "_"
            if "Doppel" in PlatzzahlString:
                try:
                    Doppelzimmerplätze = int(PlatzzahlString.split("davon Anzahl der Plätze in Doppelzimmern: ")[1].split("\n")[0])
                except IndexError:
                    Doppelzimmerplätze = int(PlatzzahlString.split("davon Anzahl der Plätze in Doppelzimmern: ")[1])
            else:
                Doppelzimmerplätze = "_"


        except NoSuchElementException:
            Platzzahl = "_"
            KZP_Plätze = "_"
            Einzelzimmerplätze = "_"
            Doppelzimmerplätze = "_"

        Plätze.append(Platzzahl)
        davon_KZP.append(KZP_Plätze)
        davon_Einzelzimmer.append(Einzelzimmerplätze)
        davon_Doppelzimmer.append(Doppelzimmerplätze)

        try:
            Anteil_PG1_ohneIK = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_lvDesktopVollstationaerVereinfacht_ctrl0_tdPreis1OberzeileMitHilfe"
            ).text
            if "vereinbart" in Anteil_PG1_ohneIK:
                Anteil_PG1_ohneIK = "_"
        except NoSuchElementException:
            Anteil_PG1_ohneIK = "_"
        Anteile_PG1_ohneIK.append(Anteil_PG1_ohneIK)
        try:
            Anteil_PG2_ohneIK = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_lvDesktopVollstationaerVereinfacht_ctrl0_tdPreis2OberzeileMitHilfe"
            ).text
        except NoSuchElementException:
            Anteil_PG2_ohneIK = "_"
        try:
            IK = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_lvDesktopVollstationaerVereinfacht_ctrl1_spanOberzeileMitHilfePreis2Jahr1"
            ).text
            if "nicht vereinbart" in IK:
                IK = "_"
        except NoSuchElementException:
            IK = "_"
        Investitionskosten.append(IK)
        try:
            Subtabelle = driver.find_element(By.ID,"button_Anteil des Versicherten (ohne Investitionskosten)")
            Subtabelle.click()
            time.sleep(0.5)
            Unterkunft = driver.find_element(By.XPATH,
                '//*[@id="ctl00_ContentPlaceHolder1_lvDesktopVollstationaer_ctrl9_spanUnterzeileOhneHilfePreis2Jahr1"]').text
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            Verpflegung = driver.find_element(By.XPATH,
                '//*[@id="ctl00_ContentPlaceHolder1_lvDesktopVollstationaer_ctrl10_spanUnterzeileOhneHilfePreis2Jahr1"]').text
            Anteil_PG2_ohneIK = driver.find_element(By.XPATH,
                '//*[@id="ctl00_ContentPlaceHolder1_lvDesktopVollstationaer_ctrl11_spanUnterzeileMitHilfePreis2Jahr1"]').text
        except NoSuchElementException:
            Unterkunft = "_"
            Verpflegung = "_"
            Anteil_PG2_ohneIK = "_"
        Unterkunftskosten.append(Unterkunft)
        Verpflegungskosten.append(Verpflegung)
        Anteile_PG2_ohneIK.append(Anteil_PG2_ohneIK)

        Trefferliste = driver.find_element(By.ID,
            "ctl00_ContentPlaceHolder1_spanZurueck"
        )
        Trefferliste.click()
        i = i + 1
        j = j + 1

        ProgressBar.progress(round(1/AnzahlErgebnisse))

        GefAnzahl = GefAnzahl + 1
        if GefAnzahl == AnzahlErgebnisse:
            print(
                "Suche erfolgreich durchgeführt für",
                GefAnzahl,
                "Einrichtungen im Ort",
                PLZ,
                "und",
                Umkreis,
                "km Umkreis."
            )
            break
        if i < 10:
            continue
        elif j < AnzahlEinrichtungen:
            i = i - 10
            NextSite = driver.find_element(By.CSS_SELECTOR, "li.pager__item.pager__next")
            NextSite.click()
            try:
                Cookie = driver.find_element(By.CLASS_NAME, "okButtonCookie")
                Cookie.click()
            except NoSuchElementException:
                pass
            Res = driver.find_element(By.ID,
                "ctl00_ContentPlaceHolder1_lvDesktopVollstationaer_ctrl{}_DetailButton".format(
                    i
                )
            )
            driver.execute_script("return arguments[0].scrollIntoView(true);", Res)
            continue
        else:
            print(
                "Suche erfolgreich durchgeführt für",
                GefAnzahl,
                "Einrichtungen im Ort",
                PLZ,
                "und",
                Umkreis,
                "km Umkreis."
            )
            break
    driver.quit()

    Adressen_Series = pd.Series(Adressen)
    Adressen_SeriesA = Adressen_Series.str.split("\n", n=4, expand=True)
    Straße = Adressen_SeriesA.iloc[:, 0]
    Ort = Adressen_SeriesA.iloc[:, 1]
    PLZ1 = Ort.str.split(" ", n=1, expand=True)[0]
    Ort1 = Ort.str.split(" ", n=1, expand=True)[1]

    PD_df = pd.DataFrame(
        list(
            zip(
                Such_PLZ,
                Einrichtungen,
                Entfernungen,
                Straße,
                PLZ1,
                Ort1,
                Telefon,
                Websites,
                Emails,
                Plätze,
                davon_KZP,
                davon_Einzelzimmer,
                davon_Doppelzimmer,
                Anteile_PG1_ohneIK,
                Anteile_PG2_ohneIK,
                Unterkunftskosten,
                Verpflegungskosten,
                Investitionskosten,
            )
        ),
        columns=[
            "Such-PLZ",
            "Einrichtung",
            "Luftlinie",
            "Straße",
            "PLZ",
            "Ort",
            "Telefon",
            "Website",
            "E-Mail",
            "Plätze",
            "davon Plätze KZP",
            "davon Einzelzimmer",
            "davon Doppelzimmer",
            "Anteil PG1",
            "Anteil PG 2-5",
            "Unterkunftskosten",
            "Verpflegungskosten",
            "I-Kosten",
        ],
    )
    return PD_df



st.set_page_config(page_title = "Webcrawler",
                   page_icon=":bar_chart:",
                   layout="wide")

st.write("Bitte füllen Sie die nachfolgenden Felder, damit der Webcrawler die Marktanalyse durchführen kann.")


GemeindeInput = st.text_input("Für welchen Ort soll die Konkurrenzrecherche durchgeführt werden?")
UmkreisInput = st.selectbox("In welchem Umkreis soll nach Einrichtungen gesucht werden?", options=[5, 10, 15, 25, 50])
AnzahlInput = st.text_input("Wie viele Einrichtungen sollen maximal wiedergegeben werden?")
StartKnopf = st.button("Starten Sie die Analyse!")
ErgebnisKnopf = st.button("Zeigen Sie die Ergebnisse!")



def ShowDataFrame(df):
    st.dataframe(df)

def convert_df_to_excel(df):
    return df.to_excel(r"C:\Users\buchholz\Downloads\StreamLitExport.xlsx")



if StartKnopf:
    try:
        df_Results = StationärCrawler(GemeindeInput, UmkreisInput, AnzahlInput, "buchholz", Fahrzeitberechnung=False)
        df_Results.dtypes.astype(str)
        ShowDataFrame(df_Results)
    except:
        st.write("Not possible currently!")
