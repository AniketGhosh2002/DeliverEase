public void createOrActiveSupplierDetailsToSpecRight(Context context, String[] args) throws Exception {
		System.out.println("*** Inside createOrActiveSupplierDetailsToSpecRight ***");
		//generatetoken
		String accessToken = generateToken(context, args);
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

			Map hashObjmap = doObj.getInfo(context, selectList);
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

			System.out.println("***Object info from TRU in patchSupplierDetailsToSpecRight:" +strType + " " +strName + " " +strState+ " "+strEntityType);	
			
			String sImpactedSiteList = EnoviaResourceBundle.getProperty(context, "emxFrameworkStringResource", context.getLocale(), "emxFramework.Excel.ImpactedSiteList");
			
			System.out.println("ImpactedSites " + sImpactedSiteList);
			
			StringList impactedSites = new StringList();
			if (sImpactedSiteList != null && !sImpactedSiteList.isEmpty()) {
				String[] siteArray = sImpactedSiteList.split(",");
				for (String site : siteArray) {
					impactedSites.add(site.trim());
				}
			}
			
			String unitType = null;
			String kenvueCode = null;
			String recordTypeId = null;
			
			if (impactedSites.contains(strEntityType)) {
				unitType = "Impacted Site";
				kenvueCode = "SR_Kenvue_Fill_Site_Code__c";
				recordTypeId = "012am000001rh3tAAA";
			} else {
				unitType = "Supplier";
				kenvueCode = "SR_Kenvue_Supplier_Code__c";
				recordTypeId = "012am000001rh3cAAA";
			}

			System.out.println("Unit Type: " + unitType);


			System.out.println("***state is active. get spec in specright***");

			String[] getArgs = new String[]{specRightName,kenvueCode,accessToken};

			String specrightId = getSupplier(context,getArgs); 

			System.out.println("***getResponse***"+specrightId);

			if(specrightId != null){
				System.out.println("***Supplier present in Specright --Activate ***");

				JSONObject jsonContent = new JSONObject();
				jsonContent.put("Name", strName);
				jsonContent.put(kenvueCode, strName);
				jsonContent.put("specright__Active2__c", "Yes");

				String jsonString = jsonContent.toString();

				System.out.println("***jsonString***"+jsonString);

				//store in outputxml
				txnObj.setAttributeValue(context, ATTRIBUTE_OUTPUT_XML, jsonString);

				String[] patchArgs = new String[]{jsonString,specrightId,accessToken};

				Map<String, String> result = patchSupplier(context, patchArgs);
				String responseCode = result.get("responseCode");
				String response = result.get("response"); 
				
				
				
				txnObj.setAttributeValue(context, ATTRIBUTE_ARTWORK_ID, specrightId);
				txnObj.setAttributeValue(context, ATTRIBUTE_DC_SPEC_NUMBER, strName);

				//set transaction status
				txnObj.setAttributeValue(context, ATTRIBUTE_TRANSACTION_STATUS, "SUCCESS");
				//complete txn obj
				txnObj.setState(context, "Complete");
			} else {
				System.out.println("***Supplier not present in Specright --Create***");

				JSONObject jsonContent = new JSONObject();
				jsonContent.put("Name", strName);
				jsonContent.put("BillingState", strStateRegion);
				jsonContent.put("BillingPostalCode", strPostalCode);
				jsonContent.put("Phone", strPhone);
				jsonContent.put("Fax", strFax);
				jsonContent.put("Website", strWebSite);
				jsonContent.put("Description", strDescription);
				jsonContent.put("specright__Status__c", "Commercial");
				jsonContent.put("specright__Vendor_ID__c", strName);
				jsonContent.put("SR_Region_Located__c", strRegion);
				jsonContent.put("SR_Alternate_Supplier_Name_s__c", strAlternateName);
				jsonContent.put(kenvueCode, strName);
				jsonContent.put("SR_Supplier_Type__c", "Primary");
				jsonContent.put("SR_Supplier_City__c", strCity);
				jsonContent.put("SR_Supplier_Country__c", strCountry);
				jsonContent.put("specright__Active2__c", "Yes");

				jsonContent.put("RecordTypeId", recordTypeId);

				String jsonString = jsonContent.toString();

				System.out.println("***jsonString***"+jsonString);

				//store in outputxml
				txnObj.setAttributeValue(context, ATTRIBUTE_OUTPUT_XML, jsonString);

				String[] postArgs = new String[]{jsonString,accessToken};

				Map<String, String> result = postSupplier(context, postArgs);
				String responseCode = result.get("responseCode");
				String response = result.get("response"); 
				
				
				
				txnObj.setAttributeValue(context, ATTRIBUTE_ARTWORK_ID, specrightId);
				txnObj.setAttributeValue(context, ATTRIBUTE_DC_SPEC_NUMBER, strName);

				//set transaction status
				txnObj.setAttributeValue(context, ATTRIBUTE_TRANSACTION_STATUS, "SUCCESS");
				//complete txn obj
				txnObj.setState(context, "Complete");

			} 
		} catch (Exception ex) {
			ex.printStackTrace();
			throw ex;
		}
	}
