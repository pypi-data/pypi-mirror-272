from requests import get, post

class Stock:
    def __init__(self, adress:str):
        self.address = adress
        self.id = ''
        self.pw = ''
        self.is_logged = False


    def check_login(self):
        if not self.is_logged:
            raise ConnectionError("로그인이 필요합니다")


    def login(self, id:str, pw:str):
        self.id = id
        self.pw = pw
        login_status = post(self.address + '/api/login', json={'id': id, 'pw': pw}).text
        if login_status == 'true':
            self.is_logged = True
        else:
            raise ValueError("비밀번호가 틀렸습니다.")


    def get_current_price(self) -> int:
        self.check_login()

        response = get(self.address+'/api/getprice').text
        if response == "close":
            raise ConnectionError("폐장되었습니다.")
        self.price = int(response)
        return self.price


    def get_price_history(self) -> list:
        self.check_login()

        price_history = get(self.address+'/api/gethistory').text
        return eval(price_history)


    def buy_stock(self, amount:int):
        self.check_login()

        buying_status = post(self.address+'/api/buy', json={'id':self.id, 'pw':self.pw, 'amount':str(amount)}).text
        if buying_status == 'true':
            print("매수에 성공했습니다.")
        else:
            raise ConnectionError(buying_status)


    def sell_stock(self, amount:int):
        self.check_login()

        selling_status = post(self.address+'/api/sell', json={'id':self.id, 'pw':self.pw, 'amount':str(amount)}).text
        if selling_status == 'true':
            print("매도에 성공했습니다.")
        else:
            raise ConnectionError(selling_status)


    def check_my_asset(self):
        self.check_login()

        checking_status = post(self.address+'/api/check', json={'id':self.id, 'pw':self.pw}).text
        if checking_status[0] != '{':
            raise ConnectionError(checking_status)
        return eval(checking_status)