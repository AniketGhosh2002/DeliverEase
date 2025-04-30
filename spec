public String postSupplierData(Context context, String[] args) throws Exception {
			URL url;
			StringBuilder response = new StringBuilder();
			String inputLine = null;
			String fieldKey = "fields";
			String fieldList = "Name";
			System.out.println(fieldList);
			String strObjName = args[0];
			int responseCode = 0;
			int retryCount = 0;
			while (responseCode != 200 && retryCount <= 3) {
				try {
					URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers");
					System.out.println(uri.toString());
					url = uri.build().toURL();
					HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
					con.setRequestMethod("POST");
					con.setDoOutput(true);
					
					String accessToken = generateToken(context, args);
					String auth = "Bearer " + accessToken;
					//con.setDoOutput(true);
					con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
					con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
					con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
					con.setRequestProperty("Authorization", auth);
					
					String jsonInputString = "{\"Name\": \"" + strObjName + "\"}";
					
					try (OutputStream outStream = con.getOutputStream()) {
		                byte[] input = jsonInputString.getBytes("utf-8");
		                outStream.write(input, 0, input.length);
		            }
					
					responseCode = con.getResponseCode();
					if(responseCode==200) {
						BufferedReader in = new BufferedReader(
								new InputStreamReader(con.getInputStream()));
						//StringBuffer response = new StringBuffer();
						while ((inputLine = in.readLine()) != null) {
							response.append(inputLine);
						}
						in.close();
						System.out.println(response.toString());
					} else {
						System.out.println("...............responseCode: "+responseCode);
						System.out.println("...............response: "+response);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			return inputLine;
		}
