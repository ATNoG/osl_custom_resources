import json

input_file = 'ServiceCreationPayload-3GPP-NetSlice.json'
output_file = input_file.split(".json")[0] + "-NoValues.json"

# Open and read the JSON file
with open(input_file, 'r') as file:
    data = json.load(file)

    for characteristic in data["serviceSpecCharacteristic"]:
        value_type = characteristic["valueType"]

        if value_type != "ENUM":
            # Remove Characteristic Values
            characteristic["serviceSpecCharacteristicValue"] = []
        else:
            # Remove repeaded values
            initial_values = characteristic["serviceSpecCharacteristicValue"]
            # Check for repetitions
            values = {}
            for initial_value in initial_values:
                 values[initial_value["value"]["value"]] = initial_value
            # Update without repeated elements
            characteristic["serviceSpecCharacteristicValue"] = list(values.values())

    
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

