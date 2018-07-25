import os
import csv
import base64
import topdf
import tempfile
import shutil

def nameit(report, month):
    return report + '_' + month + '.pdf'

def get_reports(contracts_path, reports_path):
    def is_valid(x):
        return x is not None and x not in ['','""']

    def is_valid_file(reports_path, x):
        return os.path.exists(os.path.join(reports_path, x))

    contract_id_offset = 0
    cups_offset = 1
    power_offset = 2
    tariff_id_offset = 3
    report_name_offset = 4
    body_offset = 5
    valid_offset = 6
    report_offset = 7

    with open(contracts_path, 'rb') as file_:
        reader = csv.reader(file_, delimiter=';', quotechar='|')
        month = os.path.splitext(os.path.basename(contracts_path))[0]
        return [
            {'contract_id': contract[contract_id_offset],
             'body': contract[body_offset], 
             'report': os.path.join(reports_path, contract[contract_id_offset] + '.pdf'),
             'report_name': nameit(
                 contract[contract_id_offset] + '_' + contract[report_name_offset], month)}
            for contract in reader
                if (contract and
                   is_valid(contract[contract_id_offset]) and
                   is_valid(contract[power_offset]) and
                   is_valid(contract[tariff_id_offset]) and
                   is_valid_file(reports_path, contract[contract_id_offset] + '.pdf'))]
    return [] 


def render_reports(O, reports, template_name, output):
    path_aux = tempfile.mkdtemp()
    failed = []
    for report_idx,report in enumerate(reports):
        partner_data = None
        try:
            partner_data = O.get_partner_data(report['contract_id'])
        except Exception as e:
            partner_data = None
        if not partner_data:
            failed.append(report_idx)
            continue
        report.update(partner_data)
        try:
            new_report = topdf.customize(
                report = report,
                template_name = template_name,
                path_aux = path_aux,
                path_output = output)
            reports[report_idx]['pdf'] = None
            with open(new_report, 'rb') as report_file:
                data = base64.b64encode(report_file.read())
                reports[report_idx]['pdf'] = data
            if not reports[report_idx]['pdf']:
                raise Exception('Null report pdf content')
        except Exception as e:
            failed.append(report_idx)
    for idx in failed:
        del reports[idx]
    shutil.rmtree(path_aux)
