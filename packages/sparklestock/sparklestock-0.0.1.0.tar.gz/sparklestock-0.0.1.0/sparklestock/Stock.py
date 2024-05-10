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


    def get_current_price(self) -> float:
        self.check_login()
        while True:
            try:
                response = get(self.address + '/api/getprice').text
                break
            except:
                print("가격을 불러오는 중 에러가 발생했습니다. 재시도합니다.")
                continue
        if response == '"close"':
            print("폐장되었습니다.")
        self.price = float(response)
        return self.price


    def get_price_history(self) -> list:
        self.check_login()

        price_history = get(self.address+'/api/gethistory').text
        self.history = eval(price_history)
        return self.history


    def buy_stock(self, amount:int):
        self.check_login()

        buying_status = post(self.address+'/api/buy', json={'id':self.id, 'pw':self.pw, 'amount':str(int(amount))}).text
        if buying_status == 'true':
            print("매수에 성공했습니다.")
        else:
            raise ConnectionError(buying_status)


    def sell_stock(self, amount:int):
        self.check_login()

        selling_status = post(self.address+'/api/sell', json={'id':self.id, 'pw':self.pw, 'amount':str(int(amount))}).text
        if selling_status == 'true':
            print("매도에 성공했습니다.")
        else:
            raise ConnectionError(selling_status)


    def check_my_asset(self):
        self.check_login()

        checking_status = post(self.address+'/api/check', json={'id':self.id, 'pw':self.pw}).text
        if checking_status[0] != '{':
            raise ConnectionError(checking_status)
        self.asset = eval(checking_status)
        self.asset['money'] = int(self.asset['money'])
        self.asset['stock'] = int(self.asset['stock'])
        self.money = self.asset['money']
        self.stock = self.asset['stock']
        return self.asset