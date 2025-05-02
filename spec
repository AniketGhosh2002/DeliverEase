Impacted Site and/or Supplier is activated in TRU	A manufacturing site, marketing company, business unit or a supplier/distributor is activated in TRU	"- TRU sends back feed to SpecRight.
- TRU sends creates/updates supplier in SpecRight."	TRU sends site/supplier name, status (Active), other required fields & "Success"/"Published" flag back to SpecRight.			As the TRU system owner, I want TRU to be integrated with SpecRight to send back response when any supplier or site is activated, updated or deactivated.	"1. Supplier/Site activated in TRU

2. Supplier/SIte updated in TRU

3. Supplier/SIte deactivated in TRU"
Impacted Site (and/or Supplier) is deactivated in TRU	A manufacturing site, marketing company, business unit or a supplier/distributor is deactivated in TRU	"- TRU sends back feed to SpecRight.
- TRU marks supplier as Inactive in SpecRight."	TRU sends site/supplier status (Inactive) & "Success"/"Published" flag back to SpecRight.				




{
	"content": {
		"Name": "SupplierTest04"
	}
}


{
    "data": "001WF00000MFLlqYAH",
    "success": true
}

System Error: #5000002: Compile error:
/usr/tmp/1069820/TruSpecRightTransactionTrigger_mxJPOe8661e0b0100000146.java:139: error: cannot find symbol
                                                        String patchResponse = patchCall.patchSupplierData(context, patchArgs);
                                                                                        ^
  symbol:   method patchSupplierData(matrix.db.Context,java.lang.String[])
  location: variable patchCall of type TRUSpecRightDataLoader_mxJPO3e650e6c0100000249
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
Note: /usr/tmp/1069820/TruSpecRightTransactionTrigger_mxJPOe8661e0b0100000146.java uses unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.



JSONObject json = new JSONObject();
		json.put("content", jsonContent);
		System.out.println(json.toString());
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);


public String patchSupplierData(Context context, String[] args) throws Exception {
    URL url;
    String inputLine = null;

    String supplierId = args[0];     
    String newName = args[1];        

    int responseCode = 0;
    int retryCount = 0;

    while ((responseCode != 200 && responseCode != 204 && responseCode != 201) && retryCount <= 3) {
        try {
            URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers/" + supplierId);
            System.out.println("PATCH to: " + uri.toString());
            url = uri.build().toURL();

            HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
            con.setRequestProperty("X-HTTP-Method-Override", "PATCH");
            con.setRequestMethod("POST"); 
            con.setDoOutput(true);

            // Get access token
            String accessToken = generateToken(context, args);  // Replace with your logic
            String auth = "Bearer " + accessToken;

            // Set headers
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
            con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
            con.setRequestProperty("Authorization", auth);

            // Build raw JSON body
            JSONObject content = new JSONObject();
            content.put("Name", newName);

            JSONObject payload = new JSONObject();
            payload.put("content", content);

            // Send request
            try (OutputStream outStream = con.getOutputStream()) {
                byte[] input = payload.toString().getBytes("utf-8");
                outStream.write(input, 0, input.length);
            }

            // Read response
            responseCode = con.getResponseCode();
            if (responseCode == 200 || responseCode == 201 || responseCode == 204) {
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                while ((inputLine = in.readLine()) != null) {
                    // Capture the last response line
                }
                in.close();
                System.out.println("PATCH Success. Last line: " + inputLine);
            } else {
                inputLine = "HTTP Error Code: " + responseCode;
                System.out.println("PATCH failed. Code: " + responseCode);
            }

        } catch (Exception e) {
            e.printStackTrace();
            inputLine = "Exception: " + e.getMessage();
        }

        retryCount++;
    }

    return inputLine;
	}



https://teams.microsoft.com/l/meetup-join/19%3ameeting_ZmIxOGU2MDEtMzQwOC00NTE2LWJmMDEtNTM0MmI1OWFlMGY4%40thread.v2/0?context=%7b%22Tid%22%3a%227ba64ac2-8a2b-417e-9b8f-fcf8238f2a56%22%2c%22Oid%22%3a%2287fa95f5-d919-484a-a1a3-0859cdecf6d1%22%7d
