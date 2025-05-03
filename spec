// SupplierData POST and PATCH method
					String objectType = hmJsonFieldMap.get("RecordType"); 
					String supplierId = hmJsonFieldMap.get("Id");
					String supplierName = hmJsonFieldMap.get("Name");
					
					// Post Supplier to SpecRight
					if ("Supplier".equalsIgnoreCase(objectType) && supplierName != null) {
						if( supplierId == null) {
							System.out.println("Trigger: Posting Supplier to SpecRight - " + supplierName);

							String[] postArgs = new String[]{ supplierName };

							TRUSpecRightDataLoader_mxJPO supplierSync = new TRUSpecRightDataLoader_mxJPO();
							String result = supplierSync.postSupplierData(context, postArgs);

							System.out.println("SpecRight API Response ID: " + result);
						} else {
							// Patch Supplier to SpecRight
							System.out.println("Trigger: Patching supplier in SpecRight");
							
							JSONObject content = new JSONObject();
 
							for (Map.Entry<String, String> entry : hmJsonFieldMap.entrySet()) {
								String key = entry.getKey();
								if (!"Id".equalsIgnoreCase(key) && !"RecordType".equalsIgnoreCase(key)) {
									content.put(key, entry.getValue());
								}
							}
 
							JSONObject inputJson = new JSONObject();
							inputJson.put("SupplierId", supplierId);
							inputJson.put("content", content);
 
							System.out.println( inputJson.toString());

							String[] patchArgs = new String[]{ inputJson.toString() };
							TRUSpecRightDataLoader_mxJPO patchCall = new TRUSpecRightDataLoader_mxJPO();
							String patchResponse = patchCall.patchSupplierData(context, patchArgs);

							System.out.println("Patch Response: " + patchResponse);
						}
					}
