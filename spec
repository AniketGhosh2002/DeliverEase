public HashMap<String, String> postOrPatchSpecData(Context context, String[] args) throws IOException {
	URL url;
	OutputStream stream;
	String inputLine = null;
	String baseURL = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader", context.getLocale(), "TRUSpecRightDataLoader.SpecRight.BaseUrl");
	int responseCode = 0;
	int retryCount = 0;

	String jsonString = args[0];
	String accessToken = args[1];
	String connectionType = args[2]; // e.g., "Account/"
	String methodType = args[3];     // "PATCH" or "POST"
	String specRightId = (args.length > 4) ? args[4] : ""; // Optional

	JSONObject content = new JSONObject(jsonString);
	JSONObject json = new JSONObject();
	json.put("content", content);
	byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);

	StringBuffer response = new StringBuffer();
	String message = "";
	String returnJsonString = "";
	String responseUrl = "";

	try {
		while ((responseCode != 200 && responseCode != 201) && retryCount <= 3) {
			String fullURL = baseURL + connectionType + (methodType.equalsIgnoreCase("PATCH") ? specRightId : "");
			URIBuilder uri = new URIBuilder(fullURL);
			responseUrl = uri.toString();
			url = uri.build().toURL();

			HttpsURLConnection con = (HttpsURLConnection) url.openConnection();

			if (methodType.equalsIgnoreCase("PATCH")) {
				con.setRequestProperty("X-HTTP-Method-Override", "PATCH");
			}
			con.setRequestMethod("POST"); // Always POST in HTTP, PATCH is handled by override
			con.setDoOutput(true);

			String auth = "Bearer " + accessToken;
			con.setRequestProperty("Content-Type", "application/json");
			con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
			con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
			con.setRequestProperty("Authorization", auth);
			con.setConnectTimeout(60000);

			stream = con.getOutputStream();
			stream.write(out);
			stream.flush();

			responseCode = con.getResponseCode();
			System.out.println("HTTP " + methodType + " response code: " + responseCode);

			if (responseCode == 200 || responseCode == 201) {
				BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
				while ((inputLine = in.readLine()) != null) {
					response.append(inputLine);
				}
				in.close();
				returnJsonString = response.toString();
			} else {
				BufferedReader in = new BufferedReader(new InputStreamReader(con.getErrorStream()));
				StringBuffer errorResponse = new StringBuffer();
				while ((inputLine = in.readLine()) != null) {
					errorResponse.append(inputLine);
				}
				in.close();
				System.out.println("Error Response: " + errorResponse);
				JSONObject obj = new JSONObject(errorResponse.toString());
				if (obj.has("message")) {
					message = obj.getString("message");
				}
				returnJsonString = message;
			}
			retryCount++;
		}
	} catch (Exception e) {
		e.printStackTrace();
	}

	HashMap<String, String> resultMap = new HashMap<>();
	resultMap.put("ResponseCode", Integer.toString(responseCode));
	resultMap.put("ResponseUrl", responseUrl);
	resultMap.put("Response", returnJsonString);

	return resultMap;
}
