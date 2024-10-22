import json

# Load the two JSON files
with open('ServiceCreationPayload-3GPP-NetSlice-Adapted4ITAv-NoValues.json', 'r') as f_no_values:
    data_no_values = json.load(f_no_values)

with open('ServiceCreationPayload-3GPP-NetSlice-Adapted4ITAv-Bootstrapped-Example.json', 'r') as f_with_values:
    data_with_values = json.load(f_with_values)

# Create a dictionary from the file with values, using characteristic names as keys
value_map = {}
for char in data_with_values.get('serviceSpecCharacteristic', []):
    name = char['name']
    if char["valueType"] == "ENUM":
        continue
    for values in char['serviceSpecCharacteristicValue']:
        if values.get("value") and values.get("value").get("value"):
            value_map[name] = {
                "isDefault": values["isDefault"],
                "valueType": values["valueType"],
                'validFor': {'endDateTime': '2043-12-31T23:59:59.999Z', 'startDateTime': '2024-01-01T00:00:00.001Z'},
                'value': {'value': values["value"]["value"], 'alias': values["value"]["alias"]}
            }

            #print(value_map[name])


# Update the file without values by copying the values from the value_map
for char in data_no_values.get('serviceSpecCharacteristic', []):
    name = char['name']
    if name in value_map:
        char['serviceSpecCharacteristicValue'] = [value_map[name]]


# Save the updated data back to the no-values file
with open('ServiceCreationPayload-3GPP-NetSlice-Adapted4ITAv-WithDefaultValues_tmp.json', 'w') as f_out:
    json.dump(data_no_values, f_out, indent=4)
