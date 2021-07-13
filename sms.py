import requests
      
def send_textbelt_sms(phone, msg, apikey):
    """
    Sends an SMS through the Textbelt API.
    :param phone: Phone number to send the SMS to.
    :param msg: SMS message. Should not be more than 160 characters.
    :param apikey: Your textbelt API key. 'textbelt' can be used for free for 1 SMS per day.
    :returns: True if the SMS could be sent. False otherwise.
    :rtype: bool
    """
    result = True
    json_success = False
    # Attempt to send the SMS through textbelt's API and a requests instance.
    try:
        resp = requests.post('https://textbelt.com/text', {
            'phone': phone,
            'message': msg,
            'key': apikey,
        })
    except:
        result = False
    # Extract boolean API result
    if result:
        try:
            json_success = resp.json()["success"]
        except:
            result = False
    # Evaluate if the SMS was successfully sent.
    if result:
        if not json_success:
            result = False
    # Give the result back to the caller.
    return result






