# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json


global config
with open("config.json", "r") as f:
    config = json.load(f)

def signup_email(event, recipient, language):
    if language == 'en': #TODO Make English version
        language = 'fi' # Make sure something is sent
        
        subject = f'Thanks for signing up for "{event.get("name_en")}"'
        content = f"""Hi {recipient.get('firstname')}. 
        Thank you very much for signing up for "{event.get('name_en')} on our website.
        
        <h2>Event Details</h2>
        
        You have signed up for event called "{event.get('name_en')}" on our website sinimustaahallitustavastaan.org. Below are the details of your registration and event.
        """
    introductions = event.get("introductions")
    if language == "fi":
        subject = f'Kiitos ilmoittautumisestasi tapahtumaan "{event.get("title_fi")}"'
        
        content = f"""<h2>Kiitos ilmoittautumisestasi!</h2>
        
        Hei {recipient.get('name')},
        
        <br><br>
        
        Olet ilmoittautunut seuraavaan tapahtumaan: <br>

        <strong>{event.get('title_fi')}</strong>
        
        <br><br>
        
        Ilmoittautuessasi annoit seuraavat tiedot:
        
        <br><br>
        
        Roolit:
        
        <ul>
        """
        for role in recipient.get('roles'):
            content += f"<li>{role}</li>"  # Kukin rooli on oma listan kohteensa
            
        content += f"""
        </ul>
                        
        <h2>Tapahtuman tiedot</h2>
        
        
        Päivämäärä: {event.get('date')}       
        """
        
        if not len(introductions) == 0:
            content += f"""<br><br>Valitsemillesi rooleille järjestetään briiffejä, tiedot alla: <br><br>"""

        for introduction in introductions:
            content += f"""
        Päiväys ja aika: {introduction.get('date')} {introduction.get('time')} <br>
        Osoite: {introduction.get('location')}<br>
        <br>
        """
        
        if not len(introductions) == 0:
            content += "Mikäli et pääse briiffiin, ilmoitathan siitä niin voimme toimittaa kirjallisen briiffimateriaalin."
        
    msg = MIMEMultipart()
    msg['From'] = config.get('email').get('address')
    msg['To'] = recipient.get("email")
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html', 'utf-8'))  # Käytetään HTML-muotoilua
    
    try:
        mail = smtplib.SMTP(config.get('email').get('server'), config.get('email').get('port'))
        mail.ehlo()
        mail.starttls()
        mail.login(config.get('email').get('address'), config.get('email').get('password'))
        mail.sendmail(msg['From'], msg['To'], msg.as_string())
        mail.close()
        print("Sähköposti lähetetty onnistuneesti.")
    except Exception as e:
        print(f"Virhe sähköpostia lähettäessä: {str(e)}")

def join_email(recipient, language):
    if language == 'en':        
        subject = f'Thanks for joinings us!'
        content = f"""Hi {recipient.get('name')},
        
        Thank you very much for joining us!
        
        We use telegram on communication, so you should download it, if you don't already have it.
        
        Link to our main channel is:
        https://t.me/+OpSHLCqznS5hMThk
        
        When you joined us on our website, you said that your skills are:
        """
        
        for role in recipient.get("roles"):
            content += role + "," + "\n"
        
        content += """Is the information correct? If not, you can inform us about that, by answering this email.
        
        
        """
            
    if language == "fi":
        subject = f'Kiitos kun liityit meihin!'
        
        content = f"""Hei {recipient.get('name')},
        
        Kiitos kun liityit meihin!
        
        Käytämme sisäisessä kommunikaatiossa telegramia, joten sinun kannattaa ladata se, ellei sinulla jo ole sitä.
        
        Pääryhmämme linkki on:
        https://t.me/+OpSHLCqznS5hMThk

        Ilmoittautuessasi mukaan, ilmoitit että taitojasi ovat:
        """.replace("\n", "<br>")
        
        for role in recipient.get("roles"):
            content += role + "," + "\n"
        
        content += """Ovatko tiedot oikein? Mikäli eivät, voit saattaa asian tietoomme vastaamalla sähköpostiin.
    
        
        Ystävällisin terveisin,
        SMHV Bot
        """
        
    msg = MIMEMultipart()
    msg['From'] = config.get('email').get('address')
    msg['To'] = recipient.get("email")
    msg['Subject'] = subject
    msg.attach(MIMEText(content.replace("\n", "<br>"), 'html', 'utf-8'))  # We use utf-8 formatting
    
    try:
        mail = smtplib.SMTP(config.get('email').get('server'), config.get('email').get('port'))
        mail.ehlo()
        mail.starttls()
        mail.login(config.get('email').get('address'), config.get('email').get('password'))
        mail.sendmail(msg['From'], msg['To'], msg.as_string())
        mail.close()
        print("Sähköposti lähetetty onnistuneesti.")
        
    except Exception as e:
        print(f"Virhe sähköpostia lähettäessä: {str(e)}")