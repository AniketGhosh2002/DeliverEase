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

							String[] patchArgs = new String[]{ supplierId, supplierName };
							TRUSpecRightDataLoader_mxJPO patchCall = new TRUSpecRightDataLoader_mxJPO();
							String patchResponse = patchCall.patchSupplierData(context, patchArgs);

							System.out.println("Patch Response: " + patchResponse);
						}
					}
