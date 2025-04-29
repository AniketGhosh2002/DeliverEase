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
