#An engine object to manage interaction with the Fixr API
import uuid
from .rest_engine import RestEngine
import requests
class FixrEngine():
    BASE_URL = 'https://api.fixr.co/api/v2/app/'
    LOGIN_PATH = 'user/authenticate/with-email'
    RESERVE_PATH = 'reservations'
    EPHKEY_PATH = 'stripe/ephemeral-key'
    headers = {
            "accept": "application/json",
            "accept-language": "en-GB",
            "authorization": "Token 41773014339d6d8e906451bfcc1d16368d866dc8",
            "content-type": "application/json",
            "fixr-app-version": "7.4.0",
            "fixr-channel": "fixr-website",
            "fixr-channel-meta": "e30=",
            "fixr-platform": "web",
            "fixr-platform-version": "Chrome/116.0.0.0",
            "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }
    #
    email = None
    password = None
    uuid = str(uuid.uuid4())
    eventId = None
    ticketId = None
    authToken = None
    customerId = None
    partsId = None
    eventData = None
    paymentMethodId = 'pm_0Npy7bIUW1BjRog9cj1r7Q3G' #comes from a stripe request
    clientSecret = None #comes from https://api.fixr.co/api/v2/app/reservations/e753f326-cb48-47f3-a78f-45b2b424e78b?reservation_flow=v2
    key = 'pk_live_Jc9zYhZyq3a4JviHWZFBFRdp' # comes from https://api.fixr.co/api/v2/app/event/768050021
    paymentIntentId = None # comes from this request https://api.stripe.com/v1/payment_intents/pi_2NqEPtIUW1BjRog91TTFfGyW?key=pk_live_Jc9zYhZyq3a4JviHWZFBFRdp&_stripe_version=2022-11-15&is_stripe_sdk=false&client_secret=pi_2NqEPtIUW1BjRog91TTFfGyW_secret_mI7VUIcW01RPtJ7Iwq5w3EXxo

    def __init__(self, email, password, eventId, ticketId) -> None:
        self.rest = RestEngine(self.BASE_URL)
        self.email = email
        self.password = password
        self.eventId = eventId
        self.ticketId = ticketId

        self.fetchEvent()

    def login(self):
        result = self.rest.post(self.LOGIN_PATH, {'email': self.email, 'password': self.password})
        if result.status_code == 200:
            self.authToken = result.json()['auth_token']
            self.rest.setAuth(self.authToken)
            self.rest.setHeaders(
                self.headers
            )
            self.findCustomerId()
            return True
        else:
            return False
        
    def reserve(self):
        data = {
            "event_id": self.eventId,
            "parts": [{"amount": 1, "ticket_type_id": self.ticketId}],
            "tracking_reference": None,
            "idempotency_key": self.uuid
        }

        response = self.rest.post(self.RESERVE_PATH, data)
        if response.status_code == 201:
            self.partsId = response.json()['parts'][0]['id']
            return True
        else:
            return False

    def findCustomerId(self):
        result = self.rest.post(self.EPHKEY_PATH, {'stripe_version': '2022-11-15', 'config_id': None})
        data = result.json()
        if result.status_code == 201:
            self.customerId = data['associated_objects'][0]['id']
            return True
        else:
            return False
        

    def freeze(self):
        result = self.rest.post(f'{self.RESERVE_PATH}/{self.uuid}/freeze?reservation_flow=v2')
        pass

    def protectTicket(self):
        result = self.rest.patch(f'{self.RESERVE_PATH}/{self.uuid}/ticket-protection?reservation_flow=v2', {
            'parts': [
                {'id': self.partsId, 'ticket_protection_enabled': False}
            ]
        })
        pass
    
    def getCheckout(self):
        fixrweb = RestEngine('https://fixr.co/')
        fixrweb.setHeaders(
            self.headers
        )
        fixrweb.setAuth(self.authToken)
        result = fixrweb.get(f'event/{self.eventData["routing_part"]}-{self.eventId}/checkout?key={self.uuid}')
        if result.status_code == 200:
            return True
        else:
            return False

    def getCustomerId(self):
        return self.customerId

    def fetchReservation(self):
        result = self.rest.get(self.RESERVE_PATH + '/' + self.uuid)
    
    def fetchEvent(self):
        result = self.rest.get(f'event/{self.eventId}')
        self.eventData = result.json()

    def getClientSecret(self):
        return self.clientSecret
    
    def getPaymentMethodId(self):
        return self.paymentMethodId
    
    def getKey(self):
        return self.key
    
    def getPaymentIntentId(self):
        return self.paymentIntentId