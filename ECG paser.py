import os
import argparse

import pandas as pd

import xml.etree.cElementTree as ET

patient_counter = 0
patients = {}

fields = ['pamp', 'pdur', 'parea', 'ppamp', 'ppdur', 'pparea', 'qamp', 'qdur', 'ramp', 'rdur',
          'samp', 'sdur', 'rpamp', 'rpdur', 'spamp', 'spdur', 'vat', 'qrsppk', 'qrsdur', 'qrsarea',
          'ston', 'stmid', 'st80', 'stend', 'stdur', 'stslope', 'tamp', 'tdur', 'tarea',
          'tpamp', 'tpdur', 'tparea', 'print', 'prseg', 'qtint']

scaler = {'pamp': 1000, 'pdur': 1, 'parea': 10, 'ppamp': 1000, 'ppdur': 1, 'pparea': 10, 'qamp': 1000, 'qdur': 1, 'ramp': 1000, 'rdur': 1,
          'samp': 1000, 'sdur': 1, 'rpamp': 1000, 'rpdur': 1, 'spamp': 1000, 'spdur': 1, 'vat': 1, 'qrsppk': 1000, 'qrsdur': 1, 'qrsarea': 10,
          'ston': 1000, 'stmid': 1000, 'st80': 1000, 'stend': 1000, 'stdur': 1, 'stslope': 1, 'tamp': 1000, 'tdur': 1, 'tarea': 10,
          'tpamp': 1000, 'tpdur': 1, 'tparea': 10, 'print': 1, 'prseg': 1, 'qtint': 1}

crosslead_fields = ['transqrsinitangle', 'transqrsinitmag', 'transqrsmaxangle', 'transqrsmaxmag', 'transqrstermangle', 'transqrstermmag', 'transqrscwrot',
                    'pfrontaxis', 'phorizaxis', 'i40frontaxis', 'i40horizaxis', 'qrsfrontaxis', 'qrshorizaxis', 't40frontaxis', 't40horizaxis', 'stfrontaxis',
                    'sthorizaxis', 'tfrontaxis', 'thorizaxis', 'atrialrate', 'meanventrate', 'meanprint', 'meanprseg', 'meanqrsdur', 'meanqtint',
                    'meanqtc', 'qtintdispersion']

crosslead_scalers = {'transqrsinitangle': 1, 'transqrsinitmag': 1000,
                     'transqrsmaxangle': 1, 'transqrsmaxmag': 1000, 'transqrstermangle': 1, 'transqrstermmag': 1000, 'transqrscwrot': 1,
                     'pfrontaxis': 1, 'phorizaxis': 1, 'i40frontaxis': 1, 'i40horizaxis': 1, 'qrsfrontaxis': 1, 'qrshorizaxis': 1,
                     't40frontaxis': 1, 't40horizaxis': 1, 'stfrontaxis': 1, 'sthorizaxis': 1, 'tfrontaxis': 1, 'thorizaxis': 1,
                     'atrialrate': 1, 'meanventrate': 1, 'meanprint': 1, 'meanprseg': 1, 'meanqrsdur': 1, 'meanqtint': 1, 'meanqtc': 1,
                     'qtintdispersion': 1}

results = pd.DataFrame(
    columns=['num', 'id', 'date', 'time', 'sensor'] + fields + crosslead_fields)


def parse_xml(xml_tree):

    global patient_counter
    global patients
    global results

    data = {'I': {}, 'II': {}, 'III': {}, 'aVR': {}, 'aVL': {}, 'aVF': {},
            'V1': {}, 'V2': {}, 'V3': {}, 'V4': {}, 'V5': {}, 'V6': {}}

    root = xml_tree.getroot()

    date = root.find(
        './{http://www3.medical.philips.com}reportinfo').attrib['date']
    time = root.find(
        './{http://www3.medical.philips.com}reportinfo').attrib['time']
    patient = root.find(
        './{http://www3.medical.philips.com}patient/{http://www3.medical.philips.com}generalpatientdata/{http://www3.medical.philips.com}patientid').text
    patient = patient.upper()
    
    if patient not in patients:
        patient_counter += 1
        patients[patient] = patient_counter

    leads = root.findall(
        './{http://www3.medical.philips.com}internalmeasurements/{http://www3.medical.philips.com}leadmeasurements/{http://www3.medical.philips.com}leadmeasurement')

    for lead in leads:
        sensor = lead.attrib['leadname']
        sensor_data = {}

        for field in fields:
            val = lead.find('./{http://www3.medical.philips.com}' + field).text
            if val != "Indeterminate" and val != "failed" and val != "Invalid":
                if val is not None:
                    val = int(val) / scaler[field]
                else: val = 0.0
                    
            sensor_data[field] = val
            
        sensor_data['stshape'] = lead.find(
                './{http://www3.medical.philips.com}stshape').text

        sensor_data['pnotchflag'] = lead.attrib['pnotchflag']

        sensor_data['qrsnotchflag'] = lead.attrib['qrsnotchflag']

        sensor_data['qrsdeltaflag'] = lead.attrib['qrsdeltaflag']

        sensor_data['tnotchflag'] = lead.attrib['tnotchflag']
            
        data[sensor] = sensor_data
        
    crosslead_data = root.findall(
        './{http://www3.medical.philips.com}internalmeasurements/{http://www3.medical.philips.com}crossleadmeasurements/*')
    _crosslead_data = {}
    for crosslead in crosslead_data:
        crosslead_field = crosslead.tag.replace(
            '{http://www3.medical.philips.com}', '')
        if crosslead_field in crosslead_fields:
            val = crosslead.text
            if val != "Indeterminate" and val != "Failed" and val != "Invalid":
                if val is not None:
                    val = float(val)/crosslead_scalers[crosslead_field]
                else: val = 0.0
            _crosslead_data[crosslead_field] = val

    for sensor, sensor_data in data.items():
        temp = sensor_data
        temp['num'] = patients[patient]
        temp['id'] = patient
        temp['date'] = date
        temp['time'] = time
        temp['sensor'] = sensor
        for crosslead_field, crosslead_val in _crosslead_data.items():
            temp[crosslead_field] = crosslead_val

        results = results.append(temp, ignore_index=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', type=str, default='./data/raw/')
    parser.add_argument('out_path', type=str, default='./')

    args = parser.parse_args()

    for filename in os.listdir(args.data_path):
        print(args.data_path + filename)
        tree = ET.parse(args.data_path + filename)
        print('Parsing {}...'.format(filename))
        parse_xml(tree)

    reshaped_results = results.set_index(
        ['num', 'id', 'date'] + crosslead_fields + ['time', 'sensor']).unstack(level=-1)

    if not os.path.isdir(args.out_path):
        os.mkdir(args.out_path)

    print('\nWriting results.xlsx to {} ...'.format(args.out_path))
    reshaped_results.to_excel(args.out_path + 'results.xlsx', 'Results')
    
    print('Done!')

