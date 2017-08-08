import sys
import os

import inspect
import yaml

def setup_pool():
    return OpenERPMockup()

def load_yaml(path):
    _yaml = yaml.load(open(path, 'r'))
    return _yaml if _yaml else []

class OpenERPMockup(object):
    def __init__(self):
        pass

    def send_reports(self, reports):
        #global sent_reports
        #import tasks_test
        #tasks_test.sent_reports += reports
        #import tasks_test
        #tasks_test.send_reports(reports)
        import openerp_mail 
        openerp_mail.sent_reports += reports

    def get_partner_data(self, contract_id):
        frame = inspect.stack()[11]
        test_name = frame[3]

        # Tricky workaround to be manage different stacks
        if not test_name.startswith('test_'):
            frame = inspect.stack()[12]
            test_name = frame[3]

        path = os.path.join('data', test_name, 'contracts.yaml')
        contracts = load_yaml(path)
        if contract_id not in contracts:
            raise Exception('contract_id: %s not in test contracts' % contract_id)
        return contracts[contract_id]
