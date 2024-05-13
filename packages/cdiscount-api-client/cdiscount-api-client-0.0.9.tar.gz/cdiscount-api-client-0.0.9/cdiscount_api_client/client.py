import requests as rq

from cdiscount_api_client import (
    resources,
    utils
)

class AuthError:
    pass

class CdiscountClient:
    # BASE_URL = 'https://marketplaceapi.cdiscount.com'
    BASE_URL = 'https://api.octopia-io.net'

    def __init__(self, client_id, client_secret, seller_id, subscription_keys={}):
        self._session = rq.Session()

        self._client_id = client_id
        self._client_secret = client_secret
        self._seller_id = seller_id
        self._subscription_keys = subscription_keys

        self._urls = {
            # 'token': "https://oauth2.cdiscount.com/auth/realms/maas-international-sellers/protocol/openid-connect/token",
            'token': "https://auth.octopia.com/auth/realms/maas/protocol/openid-connect/token"
            
        }
        self._base_url_v2 = utils.urljoin(self.BASE_URL, 'seller', 'v2')
        self._resources = {
            'product_management': resources.ProductManagementPool(
                utils.urljoin(self.BASE_URL, 'productManagement'), self._session, self._subscription_keys.get('product')
            ),
            'order_management': resources.OrderManagementPool(
                utils.urljoin(self.BASE_URL, 'OrderManagement/orders'), self._session, self._subscription_keys.get('order')
            ),
            'offer_management': resources.OfferManagementPool(
                utils.urljoin(self.BASE_URL, 'offerManagement'), self._session, self._subscription_keys.get('offer')
            ),
            'fulfillment': resources.FFMPool(
                utils.urljoin(self._base_url_v2, 'fulfillment'), self._session, self._subscription_keys.get('v2')
            ),
            'stocks': resources.StocksPool(
                utils.urljoin(self._base_url_v2, 'stocks'), self._session, self._subscription_keys.get('v2')
            ),
            'orders': resources.OrdersPool(
                utils.urljoin(self._base_url_v2, 'orders'), self._session, self._subscription_keys.get('v2')
            )
        }

        self._authenticate()

    def _authenticate(self):
        auth_data = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'client_credentials'
        }
        res = self._session.post(self._urls['token'], data=auth_data)
        if res.status_code != 200:
            raise AuthError('Error {}: {}'.format(res.status_code, res.text))

        access_token = res.json()['access_token']
        self._session.headers.update({
            'Authorization': 'Bearer {}'.format(access_token),
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json-patch+json',
            'SellerId': self._seller_id
        })

    @property
    def resources(self):
        return self._resources

    @property
    def product_management(self):
        return self._resources['product_management']

    @property
    def order_management(self):
        return self._resources['order_management']

    @property
    def offer_management(self):
        return self._resources['offer_management']                
    
    @property
    def fulfillment(self):
        return self._resources['fulfillment']
    
    @property
    def stocks(self):
        return self._resources['stocks']   
    
    @property
    def orders(self):
        return self._resources['orders']        