public HashMap<String, String> postSupplier(Context context, String[] args) throws Exception {
		URL url;
		OutputStream stream;
		String inputLine = "";
		String baseURL = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.BaseUrl");
		String postURL = "";
		int responseCode = 0;
		int retryCount = 0;

		String jsonString = args[0];           
		String accessToken = args[1];          
		String postConnectionType = args[2];
		
		Map<String, String> responseMap = new HashMap<>();
		
		JSONObject content = new JSONObject(jsonString);
		JSONObject json = new JSONObject();
		json.put("content", content);
		System.out.println(json.toString()); 
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);
		StringBuffer response = new StringBuffer();
		String message = "";
		String returnJsonString = "";

		try {
			while ((responseCode != 200 && responseCode != 201) && retryCount <= 3) {
				URIBuilder uri = new URIBuilder(baseURL + postConnectionType);
				System.out.println("POST to: " + uri.toString());
				postURL = uri.toString();
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestProperty("X-HTTP-Method-Override", "PATCH");
				con.setRequestMethod("POST");
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
				if (responseCode == 200 || responseCode == 201) {
					BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
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
					returnJsonString = errorResponse.toString();
				}

				retryCount++;
			}

		} catch (Exception e) {
			e.printStackTrace();
			inputLine = "Exception: " + e.getMessage();
		}
		
		HashMap<String, String> postReturnMap = new HashMap<String, String>();
		postReturnMap.put("ResponseCode", Integer.toString(responseCode));
		postReturnMap.put("ResponseUrl", postURL);
		postReturnMap.put("Response", returnJsonString);

		return postReturnMap;
	}





getting error while response code 404


java.lang.NullPointerException
        at java.base/java.io.Reader.<init>(Reader.java:167)
        at java.base/java.io.InputStreamReader.<init>(InputStreamReader.java:72)
        at TRUSpecRightDataLoader_mxJPO3e650e6c0100000d47.postSupplier(TRUSpecRightDataLoader_mxJPO3e650e6c0100000d47.java:3651)
        at TRUSpecRightDataLoader_mxJPO3e650e6c0100000d47.createOrActiveBulkSupplierData(TRUSpecRightDataLoader_mxJPO3e650e6c0100000d47.java:2801)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:572)
        at matrix.db.JPOSupport.invokeObject(JPOSupport.java:442)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
        at java.base/jdk.internal.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
        at java.base/java.lang.reflect.Method.invoke(Method.java:572)
        at com.dassault_systemes.platform.ipmodeling.jni.EnoviaKernelUtils._invoke(EnoviaKernelUtils.java:71)
        at com.dassault_systemes.platform.ipmodeling.jni.EnoviaKernelUtils.invoke(EnoviaKernelUtils.java:51)
        at com.dassault_systemes.platform.ipmodeling.jni.EnoviaKernelUtils.invokeObject(EnoviaKernelUtils.java:148)
