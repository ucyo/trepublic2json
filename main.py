# importing all the required modules
import pypdf
from glob import glob
from datetime import datetime
import json
import os

base_path = os.path.join(os.path.dirname(__file__), 'pdfs')
search = os.path.join(base_path, '*.pdf')
pdfs = glob(search)

# creating a pdf reader object
pdfs = [pypdf.PdfReader(x) for x in pdfs]

def parse_pdf(pdf):
    text = pdf.pages[0].extract_text()
    header, details = text.split('\nAUSFÜHRUNG ', 1)
    order, transaction = header[-9:], details[:9]

    header, details = text.split('VERRECHNUNGSKONTO WERTSTELLUNG BETRAG\n', 1)
    account,rem = details.split(' ', 1)
    date,rem = rem.split(' ', 1)
    amount,rem = rem.split(' EUR', 1)

    header,details = rem.split('PREIS BETRAG\n',1)
    order_type = parse_order_type(header)
    share,_ = parse_obj(details)
    isin,_ = parse_isin(details)
    pieces,_ = parse_pieces(details)
    single_price,_ = parse_single_price(details)
    total_price,_ = parse_total_price(details)

    date = datetime.strptime(date, '%d.%m.%Y')
    date = date.strftime('%Y-%m-%d')
    amount = make_ger_float_us_float(amount)
    amount = float(amount)

    return dict(account=account, date=date, total_check_amount=amount, order_id=order, transaction_id=transaction,
                name=share, isin=isin, shares=pieces, share_price=single_price, 
                total_share_price=total_price, total_share_price_calc=pieces*single_price, 
                order_type=order_type)

def parse_order_type(header):
    _, tmp = header.split('Market-Order ')
    if tmp.startswith('Kauf'):
        return 'buy'
    elif tmp.startswith('Verkauf'):
        return 'sell'
    else:
        raise ValueError('Unknown order type')

def parse_obj(details):
    share, rem = details.split('ISIN:', 1)
    return share.replace('\n', ' ').strip(), rem

def parse_isin(details):
    _, rem = parse_obj(details)
    rem = rem.strip()
    isin_len = 12
    return rem[:isin_len].strip(), rem[isin_len:]

def parse_pieces(details):
    _, rem = parse_isin(details)
    pieces, rem = rem.split(' Stk. ', 1)
    pieces = make_ger_float_us_float(pieces).strip()
    return float(pieces), rem

def parse_single_price(details):
    _, rem = parse_pieces(details)
    price, rem = rem.split(' EUR', 1)
    price = make_ger_float_us_float(price).strip()
    return float(price), rem

def parse_total_price(details):
    _, rem = parse_single_price(details)
    price, _ = rem.split(' EUR', 1)
    price = make_ger_float_us_float(price).strip()
    return float(price), rem

def make_ger_float_us_float(ger_float):
    ger_float = ger_float.replace('.','')
    us_float = ger_float.replace(',','.')
    return us_float

res = [parse_pdf(pdf) for pdf in pdfs]
res = json.dumps(res, indent=2, sort_keys=True)
print(res)