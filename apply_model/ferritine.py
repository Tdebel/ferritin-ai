import pickle
import numpy
import sklearn
import pandas as pd
import sys
import glob


if __name__ == '__main__':

    columns = ['GESLACHT', 'LEEFTIJD', 'HB', 'ERY', 'MCV', 'MCH', 'TRMB', 'LEU', 'CRP']
    synonyms = {'geslacht': 'Geslacht','sex': 'Geslacht','gender': 'Geslacht','leeftijd': 'Leeftijd','age': 'Leeftijd', 'leukocyten': 'LEU','leukocytes': 'LEU','leukocyte': 'LEU','total leukocyte count': 'LEU','white blood cell count': 'LEU','white blood cells': 'LEU','wbc': 'LEU', 'crp': 'CRP','c-reactive protein': 'CRP','c reactive protein': 'CRP', 'trombocyten': 'TRMB','trombocytesthrombocytes': 'TRMB', 'mcv': 'MCV','mean cellular volume': 'MCV', 'mch': 'MCH','mean cellular hemoglobin': 'MCH','mean cellular haemoglobin': 'MCH', 'erytrocyten': 'ERY','erytrocyte count': 'ERY','erytrocytes': 'ERY','erythrocytes': 'ERY', 'hb': 'HB','hemoglobine': 'HB','hemoglobin': 'HB','haemoglobin': 'HB'}
    
    anemie_filepath = ''
    try:
        anemie_filepath = sys.argv[1]
    except:
        anemie_filepath = [f for f in glob.glob('./*.xls*') if '$' not in f][0]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else 'output.xlsx'
    model = './model/siemens_model.sav'
    clf = pickle.load(open(model, 'rb'))
    try:
        df = pd.read_excel(anemie_filepath, sheet_name=0, engine='openpyxl')
    except:
        raise NameError('no excel file found!')
    
    df.rename(columns=str.lower, inplace=True)
    df.rename(columns=synonyms, inplace=True)
    df.rename(columns=str.upper, inplace=True)
    df.replace({'GESLACHT': {'M': 1.0, 'V': 0.0}}, inplace=True)
    Xnp = df[columns].to_numpy()
    ynp = clf.predict_proba(Xnp)
    df['model_output'] = ynp[:,1]
    df.replace({'GESLACHT': {1: 'M', 0: 'V'}}, inplace=True)
    with pd.ExcelWriter(r'./{}'.format(output_filename)) as writer:
        df.to_excel(writer, index=False)
    print('model prediction was succesful, output in {}'.format(output_filename))