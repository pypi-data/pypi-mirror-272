from wheelz_idp_validations.sanitizers.plate import sanitize_plate
from wheelz_idp_validations.sanitizers.vin import sanitize_vin
from wheelz_idp_validations.sanitizers.date import sanitize_dates

def sanitize_pcv2(table_json):
    # Sanitize número de matrícula. Campo A
    if "A" in table_json:
        try:
            table_json["A"] = sanitize_plate(table_json["A"])
        except Exception as e:
            table_json["A"] = ""
            print("Error sanitizing field A:", str(e))
    else:
        print("Warning: 'A' has not been validated because not found in the response dictionary.")

    # Sanitize número de bastidor o VIN. Campo E
    if "E" in table_json:
        try:
            table_json["E"] = sanitize_vin(table_json["E"])
        except Exception as e:
            table_json["E"] = ""
            print("Error sanitizing field E:", str(e))
    else:
        print("Warning: 'E' has not been validated because not found in the response dictionary.")
    
    # Sanitize field fecha de primera matriculación. Campo B
    if "B" in table_json:
        try:
            table_json["B"] = sanitize_dates(table_json["B"])
        except Exception as e:
            table_json["B"] = ""
            print("Error sanitizing field B:", str(e))
    else:
        print("Warning: 'B' has not been validated because not found in the response dictionary.")

    # Sanitize field periodo de validez del permiso. Campo H
    if "H" in table_json:
        try:
            table_json["H"] = sanitize_dates(table_json["H"])
        except Exception as e:
            table_json["H"] = ""
            print("Error sanitizing field H:", str(e))
    else:
        print("Warning: 'H' has not been validated because not found in the response dictionary.")

    # Sanitize field fecha de matriculación a la que se refiere el presente permiso. Campo I
    if "I" in table_json:
        try:
            table_json["I"] = sanitize_dates(table_json["I"])
        except Exception as e:
            table_json["I"] = ""
            print("Error sanitizing field I:", str(e))
    else:
        print("Warning: 'I' has not been validated because not found in the response dictionary.")

    # Sanitize field fecha de expedición. Campo I.1
    if "I.1" in table_json:
        try:
            table_json["I.1"] = sanitize_dates(table_json["I.1"])
        except Exception as e:
            table_json["I.1"] = ""
            print("Error sanitizing field I.1:", str(e))
    else:
        print("Warning: 'I.1' has not been validated because not found in the response dictionary.")

    return table_json

