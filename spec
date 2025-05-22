public String patchSupplier(Context context, String[] args) throws Exception {
		URL url;
		OutputStream stream;
		String inputLine = null;
		int responseCode = 0;
		int retryCount = 0;

		String jsonString = args[0];
		String supplierId = args[1];
		String accessToken = args[2];

		JSONObject content = new JSONObject(jsonString);
		JSONObject json = new JSONObject();
		json.put("content", content);
		System.out.println(json.toString()); 
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);

		try {
			while ((responseCode != 200 && responseCode != 201) && retryCount <= 3) {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/objects/Account/" + supplierId);
				System.out.println("PATCH to: " + uri.toString());
				System.out.println(uri.toString());
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
				if (responseCode == 200 || responseCode == 201 ) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
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
