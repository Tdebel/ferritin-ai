import os.path
import pickle
import numpy
import sklearn
import pandas as pd
import sys
import glob


if __name__ == "__main__":

    # Expected columns in the excel file.
    columns = ["GESLACHT", "LEEFTIJD", "HB", "ERY", "MCV", "MCH", "TRMB", "LEU", "CRP"]

    # Synonyms that are allowed for the expected column names
    synonyms = {
        "geslacht": "Geslacht",
        "sex": "Geslacht",
        "gender": "Geslacht",
        "leeftijd": "Leeftijd",
        "age": "Leeftijd",
        "leukocyten": "LEU",
        "leukocytes": "LEU",
        "leukocyte": "LEU",
        "total leukocyte count": "LEU",
        "white blood cell count": "LEU",
        "white blood cells": "LEU",
        "wbc": "LEU",
        "crp": "CRP",
        "c-reactive protein": "CRP",
        "c reactive protein": "CRP",
        "trombocyten": "TRMB",
        "trombocytes": "TRMB",
        "thrombocytes": "TRMB",
        "mcv": "MCV",
        "mean cellular volume": "MCV",
        "mch": "MCH",
        "mean cellular hemoglobin": "MCH",
        "mean cellular haemoglobin": "MCH",
        "erytrocyten": "ERY",
        "erytrocyte count": "ERY",
        "erytrocytes": "ERY",
        "erythrocytes": "ERY",
        "hb": "HB",
        "hemoglobine": "HB",
        "hemoglobin": "HB",
        "haemoglobin": "HB",
    }

    # Either get the input excel from the command line arguments, or search for it in the current working directory
    anemie_filepath = ""
    try:
        anemie_filepath = sys.argv[1]
    except:
        anemie_filepath = [f for f in glob.glob("./*.xls*") if "$" not in f][0]
    output_filename = sys.argv[2] if len(sys.argv) == 3 else "output.xlsx"

    # Get the model path
    if os.path.exists("./model/siemens_model.sav"):
        model = "./model/siemens_model.sav"
    else:
        model = "./model/roche_model.sav"
        if not os.path.exists(model):
            raise FileNotFoundError(
                f"no model found in {os.path.join(os.getcwd(), 'model')}, put either the siemens or roche model here"
            )

    # load the model and the excel file
    clf = pickle.load(open(model, "rb"))
    try:
        df = pd.read_excel(anemie_filepath, sheet_name=0)
    except:
        raise NameError("no excel file found!")

    # normalize the column names and values
    df.rename(columns=str.lower, inplace=True)
    df.rename(columns=synonyms, inplace=True)
    df.rename(columns=str.upper, inplace=True)
    df.replace({"GESLACHT": {"M": 1.0, "V": 0.0}}, inplace=True)

    # get input array from excel
    Xnp = df[columns].to_numpy()

    # predict the probabilities and add them to the excel file
    ynp = clf.predict_proba(Xnp)
    df["model_output"] = ynp[:, 1]

    # save the excel file
    df.replace({"GESLACHT": {1: "M", 0: "V"}}, inplace=True)
    with pd.ExcelWriter(r"./{}".format(output_filename)) as writer:
        df.to_excel(writer, index=False)

    # finish
    print("model prediction was succesful, output in {}".format(output_filename))
