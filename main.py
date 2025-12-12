import json
import unittest
from datetime import datetime

with open("./data-1.json","r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json","r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json","r") as f:
    jsonExpectedResult = json.load(f)


def convertFromFormat1(jsonObject):
    # Format 1 already uses milliseconds timestamp
    # Location is a single string with / separators

    # Split the location string
    loc_parts = jsonObject["location"].split("/")

    return {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],   # already correct
        "location": {
            "country": loc_parts[0],
            "city": loc_parts[1],
            "area": loc_parts[2],
            "factory": loc_parts[3],
            "section": loc_parts[4]
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"]
        }
    }


def convertFromFormat2(jsonObject):
    # Convert ISO timestamp → milliseconds
    dt = datetime.fromisoformat(jsonObject["timestamp"].replace("Z", "+00:00"))
    ms_timestamp = int(dt.timestamp() * 1000)

    return {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": ms_timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"]
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"]
        }
    }


def main(jsonObject):
    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 1 failed')

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult, 'Converting from Type 2 failed')


if __name__ == '__main__':
    unittest.main()
