public HashMap<String, String> patchSpecData(Context context, String[] args) throws IOException {
		URL url;
		OutputStream stream;
		String inputLine = null;
		String baseURL = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.BaseUrl");;
		int responseCode = 0;
		int retryCount = 0;

		String jsonString = args[0];
		String specRightId = args[1];
		String accessToken = args[2];
		String patchConnectionType = args[3];
		JSONObject content = new JSONObject(jsonString);
		JSONObject json = new JSONObject();
		json.put("content", content);
		System.out.println(json.toString()); 
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);
		StringBuffer response = new StringBuffer();
		String message = "";
		String returnJsonString = "";
		String responseUrl = "";
		try {
			//String accessToken = generateToken(context, args);
			while (responseCode != 200 && retryCount <= 3) {
				URIBuilder uri = new URIBuilder(baseURL + patchConnectionType + specRightId);
				System.out.println(uri.toString());
				responseUrl = uri.toString();
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestProperty("X-HTTP-Method-Override", "PATCH");
				con.setRequestMethod("POST");
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
				System.out.println(responseCode);

				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					returnJsonString = response.toString();
					System.out.println(response.toString());

				} else {
					BufferedReader in = new BufferedReader(new InputStreamReader(con.getErrorStream()));
					StringBuffer errorResponse = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						errorResponse.append(inputLine);
					}
					in.close();
					System.out.println("Error Response: " + errorResponse.toString());
					String errorJson = errorResponse.toString();

					JSONObject obj = new JSONObject(errorJson);
					if (obj.has("message")) {
						message = obj.getString("message");
					}
					returnJsonString = message;
				}
				retryCount++;
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
		HashMap<String, String> patchReturnMap = new HashMap<String, String>();
		patchReturnMap.put("ResponseCode", Integer.toString(responseCode));
		patchReturnMap.put("ResponseUrl", responseUrl);		
		patchReturnMap.put("Response", returnJsonString);

		return patchReturnMap;

	}
