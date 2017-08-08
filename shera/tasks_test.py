import sys
import os
import tempfile
import shutil
import yaml

import unittest
import tasks
import logging

import openerp_mail

def load_yaml(path):
    _yaml = yaml.load(open(path, 'r'))
    return _yaml if _yaml else []

class TestShera(unittest.TestCase):
    def assertAlmostEqualPDF(self, obtained, expected):
        f = open(obtained, 'rb')
        obtained_ = f.read()
        f.close() 
        f = open(expected, 'rb')
        expected_ = f.read()
        f.close()
        self.assertEqual(abs(len(obtained_)-len(expected_)) < 1500, True)

    def assertEqualReportsData(self, obtained, test_name, contracts_id):
        path = os.path.join('data', test_name, 'contracts.yaml')
        contracts = load_yaml(path)
        for contract in obtained:
            contract_id = contract['contract_id']
            self.assertEqual(contract_id in contracts_id, True)
            contracts_id.remove(contract_id)
            self.assertEqual(contract['name'], contracts[contract_id]['name'])
            self.assertEqual(contract['lang'], contracts[contract_id]['lang'])
            self.assertEqual(contract['surname'], contracts[contract_id]['surname'])
            self.assertEqual(contract['cups'], contracts[contract_id]['cups'])
            self.assertEqual(contract['address'], contracts[contract_id]['address'])
            self.assertEqual(contract['power'], contracts[contract_id]['power'])
            self.assertEqual(contract['tariff'], contracts[contract_id]['tariff'])
            self.assertEqual(contract['report'] is not None, True)
            self.assertEqual(contract['report_name'] is not None, True)
            self.assertEqual(contract['pdf'] is not None, True)
            self.assertEqual(contract['body'] is not None, True)
        self.assertEqual(contracts_id, [])


    def assertReportNotCreated(self, tempdir, contract_filename):
        return os.path.exists(os.path.join(tempdir, contract_filename))

    def setUp(self):
        openerp_mail.sent_reports = []
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def _test_deliver(self, test_name):
        os.environ['RQ_ASYNC'] = str(False)
        dirname = os.path.dirname(os.path.abspath(__file__))
        contracts = os.path.join(dirname, 'data/%s/201701.csv' % test_name)
        reports = os.path.join(dirname, 'data/%s/reports' % test_name)
        template = os.path.join(dirname, 'data/%s/customize.mako' % test_name)
        tasks.deliver_reports(contracts, reports, template, self.tempdir, testing=True)

    def test_ok_single(self):
        self._test_deliver('test_ok_single')
        obtained = os.path.join(self.tempdir, '1111.pdf')
        expected = 'b2back/test_ok_single/1111.pdf'
        self.assertAlmostEqualPDF(obtained, expected)
        self.assertEqualReportsData(openerp_mail.sent_reports, 'test_ok_single', ['1111'])

    def test_ok_two(self):
        self._test_deliver('test_ok_two')
        obtained = [os.path.join(self.tempdir, '1111.pdf'),
                    os.path.join(self.tempdir, '2222.pdf')]
        expected = ['b2back/test_ok_two/1111.pdf',
                    'b2back/test_ok_two/2222.pdf']
        self.assertAlmostEqualPDF(obtained[0], expected[0])
        self.assertAlmostEqualPDF(obtained[1], expected[1])
        self.assertEqualReportsData(openerp_mail.sent_reports, 'test_ok_two', ['1111','2222'])

    def test_donotdeliver_two(self):
        self._test_deliver('test_donotdeliver_two')
        obtained = [os.path.join(self.tempdir, '1111.pdf'),
                    os.path.join(self.tempdir, '2222.pdf')]
        expected = ['b2back/test_donotdeliver_two/1111.pdf',
                    'b2back/test_donotdeliver_two/2222.pdf']
        self.assertAlmostEqualPDF(obtained[0], expected[0])
        self.assertAlmostEqualPDF(obtained[1], expected[1])
        self.assertReportNotCreated(self.tempdir, '3333.pdf')
        self.assertReportNotCreated(self.tempdir, '4444.pdf')
        self.assertEqual(len(openerp_mail.sent_reports), 2)
        self.assertEqualReportsData(openerp_mail.sent_reports,
            'test_donotdeliver_two', ['1111','2222'])
        self.assertEqualReportsData(openerp_mail.sent_reports,
            'test_donotdeliver_two', ['1111','2222'])

    def _test_field_missing(self, field):
        test_name = 'test_%s_missing' % field
        self._test_deliver(test_name)
        obtained = [os.path.join(self.tempdir, '1111.pdf')]
        expected = ['b2back/%s/1111.pdf' % test_name]
        self.assertAlmostEqualPDF(obtained[0], expected[0])
        self.assertReportNotCreated(self.tempdir, '2222.pdf')
        self.assertEqual(len(openerp_mail.sent_reports), 1)
        self.assertEqualReportsData(openerp_mail.sent_reports, test_name, ['1111'])

    def test_contractid_missing(self):
        self._test_field_missing('contractid')

    def test_power_missing(self):
        self._test_field_missing('power')

    def test_tariffid_missing(self):
        self._test_field_missing('tariffid')

    def test_report_missing(self):
        self._test_field_missing('report')

    def test_body_missing(self):
        self._test_field_missing('body')

    def test_valid_missing(self):
        self._test_field_missing('valid')

    def test_report_file_missing(self):
        self._test_deliver('test_report_file_missing')
        obtained = os.path.join(self.tempdir, '1111.pdf')
        expected = 'b2back/test_report_file_missing/1111.pdf'
        self.assertAlmostEqualPDF(obtained, expected)
        self.assertReportNotCreated(self.tempdir, '2222.pdf')
        self.assertEqualReportsData(openerp_mail.sent_reports, 'test_report_file_missing', ['1111'])

    def test_mako_notvalid(self):
        self._test_deliver('test_mako_notvalid')
        self.assertReportNotCreated(self.tempdir, '1111.pdf')
        self.assertReportNotCreated(self.tempdir, '2222.pdf')
        self.assertEqualReportsData(openerp_mail.sent_reports, 'test_mako_notvalid', [])

    def test_contractid_notexists(self):
        self._test_deliver('test_contractid_notexists')
        obtained = [os.path.join(self.tempdir, '1111.pdf'),
                    os.path.join(self.tempdir, '2222.pdf')]
        expected = ['b2back/test_contractid_notexists/1111.pdf',
                    'b2back/test_contractid_notexists/2222.pdf']
        self.assertAlmostEqualPDF(obtained[0], expected[0])
        self.assertAlmostEqualPDF(obtained[1], expected[1])
        self.assertEqualReportsData(openerp_mail.sent_reports,
            'test_contractid_notexists', ['1111','2222'])

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout)
    logging.getLogger('shera').setLevel(logging.INFO)
    unittest.main()
