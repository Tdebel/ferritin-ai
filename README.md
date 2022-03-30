# ferritin-ai

This git contains the code supporting the article "Automated prediction of low ferritin concentrations using a machine learning algorithm". The paper can be accessed at: https://pubmed.ncbi.nlm.nih.gov/35258239/. The notebook has had all sensitive information removed. Data is available at the corresponding author upon reasonable request. 

This software is licensed under MIT license.

# How to use
The model requires the following parameters as input: ['SEX', 'AGE', 'HB', 'ERY', 'MCV', 'MCH', 'TRMB', 'LEU', 'CRP'].

A small script has been added in apply_model to apply the model to an excel file; create the following folder structure:
```
|- ferritine.py
|- model
  |- siemens_model.py # change the name in the script to roche if you want to use the other model
|- input_excel.xlsx
```

Make sure that the excel file has the column names as depeicted above. The ferritine scores predicted by the model will be written to `output.xlsx`.
