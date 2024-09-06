from mail import send_email


def signup_email(event: dict, recipient: dict, language: str, participant_id):
    """true

    Args:
        event (dict): the dict of the event
        recipient (dict): the dict of the recipient
        language (str): the language
    """

    introductions = event.get("introductions")

    if language == "en":
        subject = f'Thank you for signing up for event "{event.get("title_en")}"'

        content = f"""<h2>Thank you for signing up!</h2>
        
        Hi {recipient.get('name')},
        
        <br><br>
        
        You have signed up for the following event: <br>

        <strong>{event.get('title_en')}</strong>
        
        <br><br>
        
        When you signed up, you gave us the following information:
        
        <br><br>
        
        Roles:
        
        <ul>
        """
        for role in recipient.get("roles"):
            content += f"<li>{role}</li>"  # Every role is part of list

        content += f"""
        </ul>
                        
        <h2>Info of event:</h2>
        
        
        Date: {event.get('date')}
        Location: {event.get('location_en')}
        Telegram group (please join): {event.get('telegram_group')}       
        """

        if not len(introductions) == 0:
            content += f"""<br><br>There is introductions for the roles that you have selcted, information below: <br><br>"""

        for introduction in introductions:
            text = f"""
        Date and time: {introduction.get('date')} {introduction.get('time')} <br>
        Address: {introduction.get('location')}<br>
        <br>
        """

            # HACK to make sure that we don't send same brief multiple times...
            if not text in content:
                content += text

            else:
                continue

        if not len(introductions) == 0:  # type: ignore
            content += "If you're unable to come into the introduction, please let us know, so we can send you instructions."

        content += (
            "<br><br><a href=%s>You can cancel your signup by clicking here</a>"
            % f"https://sinimustaahallitustavastaan.org/participant_remove/{participant_id}"
        )

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
        for role in recipient.get("roles"):
            content += f"<li>{role}</li>"  # Every role is part of list

        content += f"""
        </ul>
                        
        <h2>Tapahtuman tiedot</h2>
        
        
        Päivämäärä: {event.get('date')}
        Sijainti: {event.get('location_fi')}
        Telegram ryhmä (kannattaa liittyä): {event.get('telegram_group')}       
        """

        if not len(introductions) == 0:
            content += f"""<br><br>Valitsemillesi rooleille järjestetään briiffejä, tiedot alla: <br><br>"""

        for introduction in introductions:
            text = f"""
        Päiväys ja aika: {introduction.get('date')} {introduction.get('time')} <br>
        Osoite: {introduction.get('location')}<br>
        <br>
        """

            # HACK to make sure that we don't send same brief multiple times...
            if not text in content:
                content += text

            else:
                continue

        if not len(introductions) == 0:
            content += "Mikäli et pääse briiffiin, ilmoitathan siitä niin voimme toimittaa kirjallisen briiffimateriaalin."

        content += (
            "<br><br><a href=%s>Peru ilmoittautumisesi napauttamalla tästä</a>"
            % f"https://sinimustaahallitustavastaan.org/participant_remove/{participant_id}"
        )

    send_email(recipient.get("email"), subject, content)
