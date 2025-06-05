public void createOrActiveSupplierDetailsToSpecRight(Context context, String[] args) throws Exception {
		System.out.println("*** Inside createOrActiveSupplierDetailsToSpecRight ***");
		//generatetoken
		String accessToken = generateToken(context);
		System.out.println("accessToken: "+accessToken);
		try{
			String strTxnObjId = args[0]; 
			System.out.println("Spec txn Id: "+strTxnObjId);
			DomainObject txnObj = new DomainObject(strTxnObjId);
			String sTRUObjId = txnObj.getAttributeValue(context,ATTRIBUTE_DC_SPEC_ID);
			String specRightName = txnObj.getAttributeValue(context,ATTRIBUTE_DC_SPEC_NUMBER);
			String txnEvent = txnObj.getAttributeValue(context,ATTRIBUTE_TRANSACTION_EVENT);
			//String sTRUObjId = args[0];
			//String specRightName = args[1];
			System.out.println("Suppplier bus Id from TXN: "+sTRUObjId);
			System.out.println("Suppplier bus Name from TXN: "+specRightName);
			System.out.println("Suppplier bus Event from TXN: "+txnEvent);

			DomainObject doObj = new DomainObject(sTRUObjId);
			StringList selectList = new StringList(3);
			selectList.add(DomainConstants.SELECT_TYPE);
			selectList.add(DomainConstants.SELECT_NAME);
			selectList.add(DomainConstants.SELECT_CURRENT);
			selectList.add(DomainConstants.SELECT_DESCRIPTION);
			selectList.add("attribute[" + ATTRIBUTE_STATE_REGION + "]");
			selectList.add("attribute[" + ATTRIBUTE_POSTAL_CODE + "]");
			selectList.add("attribute[" + ATTRIBUTE_ORGANIZATION_PHONE_NUMBER + "]");
			selectList.add("attribute[" + ATTRIBUTE_ORGANIZATION_FAX_NUMBER + "]");
			selectList.add("attribute[" + ATTRIBUTE_WEB_SITE + "]");
			selectList.add("attribute[" + ATTRIBUTE_REGION + "]");
			selectList.add("attribute[" + ATTRIBUTE_ALTERNATE_NAME + "]");
			selectList.add("attribute[" + ATTRIBUTE_CITY + "]");
			selectList.add("attribute[" + ATTRIBUTE_COUNTRY + "]");
			selectList.add("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");

			Map<?, ?> hashObjmap = doObj.getInfo(context, selectList);
			String strType = (String) hashObjmap.get(DomainConstants.SELECT_TYPE);
			String strName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
			String strState = (String) hashObjmap.get(DomainConstants.SELECT_CURRENT);
			String strDescription = (String) hashObjmap.get(DomainConstants.SELECT_DESCRIPTION);
			String strStateRegion = (String) hashObjmap.get("attribute[" + ATTRIBUTE_STATE_REGION + "]");
			String strPostalCode = (String) hashObjmap.get("attribute[" + ATTRIBUTE_POSTAL_CODE + "]");
			String strPhone = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ORGANIZATION_PHONE_NUMBER + "]");
			String strFax = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ORGANIZATION_FAX_NUMBER + "]");
			String strWebSite = (String) hashObjmap.get("attribute[" + ATTRIBUTE_WEB_SITE + "]");
			String strRegion = (String) hashObjmap.get("attribute[" + ATTRIBUTE_REGION + "]");
			String strAlternateName = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ALTERNATE_NAME + "]");
			String strCity = (String) hashObjmap.get("attribute[" + ATTRIBUTE_CITY + "]");
			String strCountry = (String) hashObjmap.get("attribute[" + ATTRIBUTE_COUNTRY + "]");
			String strEntityType = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");
			String externalOrNot = "External";
			
			System.out.println("***Object info from TRU in patchSupplierDetailsToSpecRight:" +strType + " " +strName + " " +strState+ " "+strEntityType);	

			String sImpactedSiteList = EnoviaResourceBundle.getProperty(context, "emxFrameworkStringResource", context.getLocale(), "emxFramework.Excel.ImpactedSiteList");
			String supplierDist = EnoviaResourceBundle.getProperty(context, "emxEngineeringCentral",context.getLocale(),"eServiceEngineeringCentral.BusinessUnit.SupplierClassification.Distributor");
			String supplierManu = EnoviaResourceBundle.getProperty(context, "emxEngineeringCentral", context.getLocale(),"eServiceEngineeringCentral.BusinessUnit.SupplierClassification.Manufacturer");

			StringList impactedSites = new StringList();
			if (sImpactedSiteList != null && !sImpactedSiteList.isEmpty()) {
				String[] siteArray = sImpactedSiteList.split(",");
				for (String site : siteArray) {
					impactedSites.add(site.trim());
				}
			}

			StringList supplierTypes = new StringList();
			if (supplierDist != null && !supplierDist.isEmpty()) {
				supplierTypes.add(supplierDist.trim());
			}
			if (supplierManu != null && !supplierManu.isEmpty()) {
				supplierTypes.add(supplierManu.trim());
			}

			String unitType = null;
			String kenvueCode = null;
			String recordTypeId = null;

			String SupplierKenvueCode =  EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Supplier.Fields");
			String FillSiteKenvueCode =  EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.ImpactedSite.Fields");
			String SupplierRecordTypeId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Supplier.RecordTypeId");
			String FillSiteRecordTypeId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.FillSite.RecordTypeId");

			if (impactedSites.contains(strEntityType)) {
				unitType = "Impacted Site";
				if(!strEntityType.contains("External")){
					externalOrNot = "Internal";
				}
				kenvueCode = FillSiteKenvueCode;
				recordTypeId = FillSiteRecordTypeId;
				System.out.println(kenvueCode+" "+recordTypeId);
			} else if (supplierTypes.contains(strEntityType)) {
				unitType = "Supplier";
				kenvueCode = SupplierKenvueCode;
				recordTypeId = SupplierRecordTypeId;
				System.out.println(kenvueCode+" "+recordTypeId);
			}

			System.out.println("Unit Type: " + unitType);

			String name = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Name");
			String state = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.StateRegion");
			String postal = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.PostalCode");
			String phone = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Phone");
			String fax = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Fax");
			String website = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Website");
			String desc = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Description");
			String stage = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Stage");
			String vendorId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.VendorId");
			String region = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Region");
			String altername = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.AlternateName");
			String suppliertype = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.SupplierType");
			String city = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.City");
			String country = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Country");
			String active = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.SupplierFillSite.Active");


			System.out.println("***state is active. get spec in specright***");

			String fieldList = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.GetSpecData.ParameterValue.fields");
			String getTypeConnection = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.GetSpecData.getTypeSpec.Account");
			String filterList = "{\""+kenvueCode+"\":\""+specRightName+"\"}";

			//String specrightId = getSpecData(context, fieldList, getTypeConnection, filterList); 
			HashMap<String, String> getReturnMap1 = getSpecData(context, fieldList, getTypeConnection, filterList);
			String jsonResponseForId = (String) getReturnMap1.get("Response");
			System.out.println("Response from get generic method: "+jsonResponseForId);
			String getResponseCode = (String) getReturnMap1.get("ResponseCode");
			System.out.println("Response code from get generic method: "+getResponseCode);

			if("200".equals(getResponseCode) || "201".equals(getResponseCode)){
				JSONObject jsonAllData = new JSONObject(jsonResponseForId);
				JSONArray dataArray = jsonAllData.getJSONArray("data");
				String specrightId = null;
				if (dataArray.length() == 0) {
					System.out.println("No records found in SpecRight");
				} else {
					JSONObject firstObject = dataArray.getJSONObject(0);
					JSONArray fieldsArray = firstObject.getJSONArray("fields");


					for (int i = 0; i < fieldsArray.length(); i++) {
						JSONObject fieldObject = fieldsArray.getJSONObject(i);
						if ("Id".equals(fieldObject.optString("field"))) {
							specrightId = fieldObject.optString("value");
							break;
						}
					}

					System.out.println("***getResponse specrightId*** " + specrightId);
				}

				if(specrightId != null){
					System.out.println("***Supplier present in Specright --Activate ***");

					JSONObject jsonContent = new JSONObject();
					jsonContent.put(name, strName);
					jsonContent.put(kenvueCode, strName);
					jsonContent.put(active, "Yes");

					String jsonString = jsonContent.toString();

					System.out.println("***jsonString***"+jsonString);


					txnObj.setAttributeValue(context, ATTRIBUTE_OUTPUT_XML, jsonString);
					String patchConnectionType = "Account/";
					//String[] patchArgsforspec = new String[]{jsonString,specrightId,accessToken,patchConnectionType};
					//String specresult = patchSpecData(context, patchArgsforspec);
					//System.out.println("Result from patchspecdata"+specresult);
					String[] patchArgs = new String[]{jsonString,specrightId,accessToken};

					Map<String, String> result = patchSupplier(context, patchArgs);
					String responseCode = result.get("responseCode");
					System.out.println(responseCode);
					String response = result.get("response"); 
					System.out.println(response);


					if("200".equals(responseCode) || "201".equals(responseCode)){
						System.out.println("***set transaction status as success***");
						String interfaceSelector = "interface[" + INTERFACE_TRUSPECRIGHTINTERFACE + "]";
						String hasInterface = doObj.getInfo(context, interfaceSelector);

						if (!"TRUE".equalsIgnoreCase(hasInterface)) {
							doObj.addBusinessInterface(context, INTERFACE_TRUSPECRIGHTINTERFACE);
							System.out.println("Added interface: " + INTERFACE_TRUSPECRIGHTINTERFACE);
						} else {
							System.out.println("Interface already present: " + INTERFACE_TRUSPECRIGHTINTERFACE);
						}
						System.out.println("Set attribute " + ATTRIBUTE_SPECRIGHT_SPEC_ID + " = " + specrightId);
						Map<String, String> attrMap = new HashMap<>();
						attrMap.put(ATTRIBUTE_INTERFACE_SPECRIGHT_ID, specrightId);
						doObj.setAttributeValues(context, attrMap);
						txnObj.setAttributeValue(context, ATTRIBUTE_ARTWORK_ID, specrightId);
						txnObj.setAttributeValue(context, ATTRIBUTE_DC_SPEC_NUMBER, strName);
						//set transaction status
						txnObj.setAttributeValue(context, ATTRIBUTE_TRANSACTION_STATUS, "SUCCESS");
						//complete txn obj
						txnObj.setState(context, "Complete");

						sendStatusEmail(context, strTxnObjId);
					}else{
						System.out.println("***error***");
						//set attribute[Transaction Error] 
						HashMap<String,String> hmAttributeMap = new HashMap<>();
						hmAttributeMap.put(ATTRIBUTE_TRANSACTION_ERROR, response);
						hmAttributeMap.put(ATTRIBUTE_TRANSACTION_STATUS, "FAILED");
						txnObj.setAttributeValues(context, hmAttributeMap);
						//txnObj.setState(context, "Complete");

						sendStatusEmail(context, strTxnObjId);
					} 


				} else {
					System.out.println("***Supplier not present in Specright --Create***");

					JSONObject jsonContent = new JSONObject();
					jsonContent.put(name, strName);
					jsonContent.put(state, strStateRegion);
					jsonContent.put(postal, strPostalCode);
					jsonContent.put(phone, strPhone);
					jsonContent.put(fax, strFax);
					jsonContent.put(website, strWebSite);
					jsonContent.put(desc, strDescription);
					jsonContent.put(stage, "Commercial");
					jsonContent.put(vendorId, strName);
					jsonContent.put(region, strRegion);
					jsonContent.put(altername, strAlternateName);
					jsonContent.put(kenvueCode, strName);
					jsonContent.put(suppliertype, "Primary");
					jsonContent.put(city, strCity);
					jsonContent.put(country, strCountry);
					jsonContent.put(active, "Yes");
					jsonContent.put("SR_Internal_External__c", externalOrNot);
					jsonContent.put("RecordTypeId", recordTypeId);

					String jsonString = jsonContent.toString();

					System.out.println("***jsonString***"+jsonString);

					//store in outputxml
					txnObj.setAttributeValue(context, ATTRIBUTE_OUTPUT_XML, jsonString);

					String[] postArgs = new String[]{jsonString,accessToken};

					Map<String, String> result = postSupplier(context, postArgs);
					String responseCode = result.get("responseCode");
					System.out.println(responseCode);
					specrightId = result.get("response"); 
					System.out.println(specrightId);

					if("200".equals(responseCode) || "201".equals(responseCode)){
						System.out.println("***set transaction status as success***");
						String interfaceSelector = "interface[" + INTERFACE_TRUSPECRIGHTINTERFACE + "]";
						String hasInterface = doObj.getInfo(context, interfaceSelector);

						if (!"TRUE".equalsIgnoreCase(hasInterface)) {
							doObj.addBusinessInterface(context, INTERFACE_TRUSPECRIGHTINTERFACE);
							System.out.println("Added interface: " + INTERFACE_TRUSPECRIGHTINTERFACE);
						} else {
							System.out.println("Interface already present: " + INTERFACE_TRUSPECRIGHTINTERFACE);
						}
						System.out.println("Set attribute " + ATTRIBUTE_SPECRIGHT_SPEC_ID + " = " + specrightId);
						Map<String, String> attrMap = new HashMap<>();
						attrMap.put(ATTRIBUTE_INTERFACE_SPECRIGHT_ID, specrightId);
						doObj.setAttributeValues(context, attrMap);
						txnObj.setAttributeValue(context, ATTRIBUTE_ARTWORK_ID, specrightId);
						txnObj.setAttributeValue(context, ATTRIBUTE_DC_SPEC_NUMBER, strName);
						//set transaction status
						txnObj.setAttributeValue(context, ATTRIBUTE_TRANSACTION_STATUS, "SUCCESS");
						//complete txn obj
						txnObj.setState(context, "Complete");

						sendStatusEmail(context, strTxnObjId);
					}else{
						System.out.println("***error***");
						//set attribute[Transaction Error] 
						HashMap<String,String> hmAttributeMap = new HashMap<>();
						hmAttributeMap.put(ATTRIBUTE_TRANSACTION_ERROR, specrightId);
						hmAttributeMap.put(ATTRIBUTE_TRANSACTION_STATUS, "FAILED");
						txnObj.setAttributeValues(context, hmAttributeMap);
						//txnObj.setState(context, "Complete");

						sendStatusEmail(context, strTxnObjId);
					} 

				} 
			} else {
				System.out.println("Error in get method");
			}
		} catch (Exception ex) {
			ex.printStackTrace();
			throw ex;
		}
	}
