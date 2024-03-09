
<center>
<img src="./assets/logo.svg" alt="SVG mit img laden" width="200" height="100" >
<h1> trepublic2json
</center>

This is a library for parsing reports and invoices from [Trade Republic](traderepublic.com) to JSON. 
The library provides the command line tool: `trepublic2json`.
It only takes the path to the folder of pdf files as an argument and returns a single json with information from all pdf files.
 
An example output with a folder containing a single pdf file.
```json
[
    {
        "account_num": "AB01234567890123456",
        "date": "2001-01-01",
        "depot_num": "0123456789",
        "depot_owner": "John Doe",
        "filename": "/path/to/pdfs/ab012345678901234567890123456789.pdf",
        "isin": "GB0123456789",
        "name": "A Company that Manufactures Everything (ACME)",
        "order_id": "c829-8f27",
        "order_type": "buy",
        "share_price": 0.07,
        "shares": 900.0,
        "total_check_amount": -64.0,
        "total_share_price": 63.0,
        "total_share_price_calc": 63.00000000000001,
        "transaction_id": "o832-a928"
    }
]
```

## Install

You can install `trepublic2json` using either pypi:

```bash
pip install trepublic2json
```

Or from source using [`rye`](https://rye-up.com/guide/):

```bash
git clone git@github.com:ucyo/trepublic.git && cd trepublic && rye install .
```