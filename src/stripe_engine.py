#An engine object to manage interaction with the Stripe API
from .rest_engine import RestEngine
class StripeEngine():
    BASE_URL = 'https://api.stripe.com/v1/'


    def __init__(self) -> None:
        self.rest = RestEngine(self.BASE_URL)

    def getPaymentMethods(self):
        pass

    def confirmPayment(self, paymentIntentId, paymentMethodId, key, clientSecret):
        result = self.rest.post(f'payment_intents/{paymentIntentId}/confirm?payment_method={paymentMethodId}&expected_payment_method_type=card&use_stripe_sdk=true&key={key}&_stripe_version=2022-11-15&client_secret={clientSecret}')
        return result
