import http.client
import urllib


class Execution(object):
    def __init__(self, domain, access_token, account_id):
        self.domain = domain
        self.access_token = access_token
        self.account_id = account_id
        self.conn = self.obtain_connection()

    def obtain_connection(self):
        return http.client.HTTPSConnection(self.domain)

    def execute_order(self, event):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer " + self.access_token
        }
        params = urllib.parse.urlencode({
            "instrument" : event.instrument,
            "units" : event.units,
            "type" : event.order_type,
            "side" : event.side
        })
        self.conn.request(
            "POST",
            "/v1/accounts/%s/orders" % str(self.account_id),
            params, headers
        )
        response = self.conn.getresponse().read().decode("utf-8").replace("\n","").replace("\t","")
        print (response)
        self.conn.close()
