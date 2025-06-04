HashMap<String, String> getReturnMap1 = getSpecData(context, fieldList, getTypeConnection, filterList);
String jsonResponseForId = getReturnMap1.get("Response");
System.out.println("Response from get generic method: " + jsonResponseForId);
String getResponseCode = getReturnMap1.get("ResponseCode");
System.out.println("Response code from get generic method: " + getResponseCode);

if ("200".equals(getResponseCode) || "201".equals(getResponseCode)) {
    JSONObject jsonAllData = new JSONObject(jsonResponseForId);
    JSONArray dataArray = jsonAllData.getJSONArray("data");

    if (dataArray.length() == 0) {
        System.out.println("No records found in SpecRight (data array is empty).");
    } else {
        JSONObject firstObject = dataArray.getJSONObject(0);
        JSONArray fieldsArray = firstObject.getJSONArray("fields");

        String specrightId = null;
        for (int i = 0; i < fieldsArray.length(); i++) {
            JSONObject fieldObject = fieldsArray.getJSONObject(i);
            if ("Id".equals(fieldObject.optString("field"))) {
                specrightId = fieldObject.optString("value");
                break;
            }
        }

        System.out.println("***getResponse specrightId*** " + specrightId);
    }
} else {
    System.out.println("Error: Invalid response code received from SpecRight GET API.");
}
