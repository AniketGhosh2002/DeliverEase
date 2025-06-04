HashMap<String, String> getReturnMap1 = getSpecData(context, fieldList, getTypeConnection, filterList);
			String jsonResponseForId = (String) getReturnMap1.get("Response");
			System.out.println("Response from get generic method: "+jsonResponseForId);
			String getResponseCode = (String) getReturnMap1.get("ResponseCode");
			System.out.println("Response code from get generic method: "+getResponseCode);
			
			if("200".equals(getResponseCode) || "201".equals(getResponseCode)){
				JSONObject jsonAllData = new JSONObject(jsonResponseForId);
				JSONArray dataArray = jsonAllData.getJSONArray("data");
				JSONObject firstObject = dataArray.getJSONObject(0);
				JSONArray fieldsArray = firstObject.getJSONArray("fields");

				String specrightId = null;
				for (int i = 0; i < fieldsArray.length(); i++) {
					JSONObject fieldObject = fieldsArray.getJSONObject(i);
					if (fieldObject.getString("field").equals("Id")) {
						specrightId = fieldObject.getString("value");
						break;
					}
				}

				System.out.println("***getResponse***"+specrightId);







Response from get generic method: {"data":[],"success":true}
Response code from get generic method: 200
