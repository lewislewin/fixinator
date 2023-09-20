from src.fixr_engine import FixrEngine as Fixr
from src.stripe_engine import StripeEngine as Stripe
def main():
    email = ''
    password = ''
    eventId = 768050021
    ticketId = 625472

    #Get username and password from config file (TODO)
    #getLoginInfo()

    fixr = Fixr(email, password, eventId, ticketId)
    stripe = Stripe()
    fixr.login()
    fixr.reserve()
    fixr.getCheckout()
    fixr.protectTicket()
    fixr.freeze()
    stripe.confirmPayment(fixr.getPaymentMethodId(), fixr.getKey(), fixr.getClientSecret())

    
    return True

if __name__ == '__main__':
    try:
        main()
    except:
        exit(1)