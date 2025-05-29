POST Success: {"data":"001WF00000OTFM4YAP","success":true}





responseCode = con.getResponseCode();
				if (responseCode == 200 || responseCode == 201) {
					BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println("POST Success: " + response.toString());
					inputLine = response.toString(); 
				} else {
					inputLine = "Error: " + responseCode;
					System.out.println("POST failed responseCode: " + responseCode);
				}

				retryCount++;
			}

		} catch (Exception e) {
			e.printStackTrace();
			inputLine = "Exception: " + e.getMessage();
		}

		responseMap.put("responseCode", String.valueOf(responseCode));
		responseMap.put("response", inputLine);
		return responseMap;
