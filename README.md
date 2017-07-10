# Shera

Shera is a beedata report delivery engine

Main features:

- Process beedata delivery report to identify which customers and which content to forward
- Customize PDF reports in order to add customer personal data not available by utility third-party providers
- Default OpenERP data provider
- Default OpenERP poweremail mail delivering

Setup:

```
pip install .
export PEEK_SERVER=<erp_ip_address>
export PEEK_DB=<erp_db_name>
export PEEK_USER=<erp_user>
export PEEK_PASSWORD=<erp password>
export WKHTMLTOPDF_=<path to wkhtmltopdf executable> (version 0.12.1)
```

Commands:

- **deliver_reports** Report customization and forwarding

Comand line arguments:

- **--contracts** [local filename] File downloaded from beedata which describes delivering actions (csv: contract_id;cups;power;tariff;report;body;valid)
- **--reports** [local dir] Folder downloaded from beedata which stores reports to be forwarded
- **--template** [local filename] .mako template describing PDF customization layer
- **--output** [local dir] Folder where customized reports are going to be saved

Example:

```

python runner.py deliver_reports \
    --contracts <beedata_contracts_rcvd>.csv \
    --reports <beedata_reports_pdf> \
    --template <customized_mako>.mako \
    --output <output_folder>

```
