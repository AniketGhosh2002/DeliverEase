// PATCH method for Supplier
	
	public String patchSupplierData(Context context, String[] args) throws Exception {
    URL url;
	OutputStream stream;
    String inputLine = null;
    int responseCode = 0;
    int retryCount = 0;
	
	JSONObject jsonobject = new JSONObject(args[0]);
    String supplierId = jsonobject.optString("SupplierId");

    if (supplierId == null || supplierId.isEmpty()) {
        System.out.println("SupplierId is required for PATCH");
    }

    JSONObject content = new JSONObject();
    for (String key : jsonobject.keySet()) {
        if (!"SupplierId".equalsIgnoreCase(key)) {
            content.put(key, jsonobject.get(key));
        }
    }

    JSONObject json = new JSONObject();
    json.put("content", content);
	
	byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);

    try {
        while ((responseCode != 200 && responseCode != 201) && retryCount <= 3) {
            URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers/" + supplierId);
            System.out.println("PATCH to: " + uri.toString());
            url = uri.build().toURL();

            HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
            con.setRequestProperty("X-HTTP-Method-Override", "PATCH");
            con.setRequestMethod("POST");
			String accessToken = generateToken(context, args);  
            String auth = "Bearer " + accessToken;			
            con.setDoOutput(true);

            con.setRequestProperty("Content-Type", "application/json");
			con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
			con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
			con.setRequestProperty("Authorization", auth);
			con.setConnectTimeout(60000);
			
			stream = con.getOutputStream();
			stream.write(out);
			// Flush the stream to ensure all data is sent
			stream.flush();

            responseCode = con.getResponseCode();
            if (responseCode == 200 || responseCode == 201 ) {
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
				StringBuffer response = new StringBuffer();
				while ((inputLine = in.readLine()) != null) {
					response.append(inputLine);
				}
                in.close();
                System.out.println("PATCH Success");
				//System.out.println("Supplier updated with Name: " + newName);
            } else {
                inputLine = "Error: " + responseCode;
                System.out.println("PATCH failed responseCode: " + responseCode);
            }
			
			retryCount++;
		}

    } catch (Exception e) {
        e.printStackTrace();
    }

    return inputLine;
	}





{
    "data": [
        {
            "fields": [
                {
                    "field": "Id",
                    "label": "Supplier ID",
                    "value": "001WF00000MgEt7YAF"
                }
            ]
        }
    ],
    "success": true
}



/suppliers?limit=50&fields=Id&filter=%7B%22Name%22%3A%22NewSiteTest001%22%7D&sort=Name:asc
