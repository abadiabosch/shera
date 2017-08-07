import os
import erppeek


def setup_peek(**kwargs):
    config = {
        'server': os.getenv('PEEK_SERVER', None), 
        'db': os.getenv('PEEK_DB', None),
        'user': os.getenv('PEEK_USER', None),
        'password': os.getenv('PEEK_PASSWORD')
    }
    config.update(kwargs)
    return erppeek.Client(**config)

def setup_pool():
    return OpenERP() 

class OpenERP(object):
    def __init__(self):
        self.O = setup_peek()

    def send_reports(self, reports):
        pool_obj = self.O.model('giscedata.polissa')
        pol_obj.send_empowering_report(reports)

    def get_partner_data(self, contract_id):
        def get_dict_data(data,key):
            if key not in data or len(data[key]) < 2:
                print "get_partner_data::Error " + str(key) + " not found!"
                return None 
            return data[key][1]
        
        def get_dict_power(data,key):
            if key not in data:
                print "getPartner_data::Error " + str(key) + " not found!"
            try:
                power = float(data[key])
            except:
                print "getPartner_data::Error " + str(key) + " not a float!"
                return None
            return "%.1f kW" % power
        result = {}
        pol_obj = self.O.model('giscedata.polissa')
        pol_ids = pol_obj.search([('name', '=', contract_id)])    
        if len(pol_ids) != 1:
            print "get_partner_data::Error finding contract in erp"
            return None
    
        pol_data = pol_obj.read(pol_ids , ['potencia',
                                           'cups',
                                           'state',
                                           'active',
                                           'tarifa',
                                           'cups_direccio',
                                           'pagador'])
        if len(pol_data) != 1:
            print "get_partner_data::Error reading data from polisse \
                id "+str(pol_ids)
            return None

        str_limit = 60  # Based on empirical results files 
        result['power'] = get_dict_power(pol_data[0],'potencia')[:str_limit]
        result['cups'] = get_dict_data(pol_data[0],'cups')[:str_limit]
        result['tariff'] = get_dict_data(pol_data[0],'tarifa')[:str_limit]
        result['address'] = pol_data[0]['cups_direccio'][:str_limit] \
                            if 'cups_direccio' in pol_data[0] else None
        result['lang'] = get_dict_data(pol_data[0],'lang')[:str_limit]
        compound_name = get_dict_data(pol_data[0],'pagador')[:str_limit]
        if not result['power'] or not result['cups'] or not result['tariff']\
            or not result['address'] or not compound_name:
            return None
    
        splited = compound_name.split(',',1)
        if len(splited) == 1:
            result['name'] = compound_name.strip()
            result['surname'] = ''
        else:
            result['name'] = splited[1].strip()
            result['surname'] = splited[0].strip()
        return result
