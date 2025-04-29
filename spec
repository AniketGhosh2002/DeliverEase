public String getSupplierData(Context context, String[] args) throws Exception {
		URL url;
		String inputLine = null;
		String fieldKey = "fields";
		String fieldList = "Id,Name,specright__Status__c";
		System.out.println(fieldList);
		String filterKey = "filter";
		String filterList = "{\"SR_State__c\":\"Unpublished\"},{\"IsDeleted\":\"false\"}}";
		//URL obj = new URL("{{host}}/objects/specright__Specification__c?");
		int responseCode = 0;
		int retryCount = 0;
		while (responseCode != 200 && retryCount <= 3) {
			try {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers?").addParameter(fieldKey, "Id,Name");
				System.out.println(uri.toString());
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestMethod("GET");
				String accessToken = generateToken(context, args);
				String auth = "Bearer " + accessToken;
				//con.setDoOutput(true);
				con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
				con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
				con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
				con.setRequestProperty("Authorization", auth);

				responseCode = con.getResponseCode();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
				} else {

				}
			}catch (Exception e) {
				e.printStackTrace();
			}
			retryCount++;
		}
		return inputLine;
	}
	
	// Post method for ImpactedSites and Supplier
	
	public String postSupplierData(Context context, String[] args) throws Exception {
		URL url;
		String inputLine = null;
		String fieldKey = "fields";
		String fieldList = "Name";
		System.out.println(fieldList);
		int responseCode = 0;
		int retryCount = 0;
		while (responseCode != 200 && retryCount <= 3) {
			try {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers");
				System.out.println(uri.toString());
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestMethod("POST");
				String accessToken = generateToken(context, args);
				String auth = "Bearer " + accessToken;
				//con.setDoOutput(true);
				con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
				con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
				con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
				con.setRequestProperty("Authorization", auth);
				
				responseCode = con.getResponseCode();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
				} else {

				}
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
		return inputLine;
	}









 public String postSupplierData(Context context, String[] args) throws Exception {
    URL url;
    String inputLine = null;
    int responseCode = 0;
    int retryCount = 0;

    // Validate input
    if (args == null || args.length == 0 || args[0] == null || args[0].isEmpty()) {
        throw new IllegalArgumentException("Supplier name must be provided in args[0]");
    }
    String supplierName = args[0]; // Get the name from the method arguments

    while (responseCode != 200 && responseCode != 201 && retryCount <= 3) {
        try {
            URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers");
            System.out.println(uri.toString());
            url = uri.build().toURL();
            HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
            con.setRequestMethod("POST");
            con.setDoOutput(true); // Allow body in POST

            String accessToken = generateToken(context, args);
            String auth = "Bearer " + accessToken;

            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
            con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
            con.setRequestProperty("Authorization", auth);

            // Create JSON body with dynamic name
            String jsonInputString = "{\"Name\": \"" + supplierName + "\"}";

            try (OutputStream os = con.getOutputStream()) {
                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }

            responseCode = con.getResponseCode();
            if (responseCode == 200 || responseCode == 201) {
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                StringBuffer response = new StringBuffer();
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                System.out.println(response.toString());
                return response.toString();
            } else {
                System.out.println("POST request failed with code: " + responseCode);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
        retryCount++;
    }
    return inputLine;
}
