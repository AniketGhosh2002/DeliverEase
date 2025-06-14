public void createOrActiveBulkSupplierData(Context context, String[] args) throws Exception {
		try {
			//Generate access token 
			String accessToken = generateToken(context);
			//Get parameters from the shell script
			String inputFilePath = args[0];
			String logFilePath = args[1]; 
			String errorFilePath = args[2]; 
		
			java.io.File file = new java.io.File(inputFilePath);
			java.io.File logfile = new java.io.File(logFilePath);
			java.io.File errorfile = new java.io.File(errorFilePath);
			java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.FileReader(file));
			FileWriter writefile = new FileWriter(logfile);
			FileWriter writeerrfile = new FileWriter(errorfile);
			PrintWriter printfile = new PrintWriter(writefile);
			PrintWriter printerrfile = new PrintWriter(writeerrfile);
		
			if (!file.exists()) {
				String errInfo = "Input file does not exist: " + inputFilePath;
				printerrfile.println(errInfo);
				return;
			}
		
			String supplierName = "";
			while ((supplierName = reader.readLine()) != null) {
				supplierName = supplierName.trim();
				if (supplierName.isEmpty()) continue;
 
				String strType = TYPE_ORGANIZATION;
				String strRev = DomainConstants.QUERY_WILDCARD;
				String whereClause = "current == Active";
				StringList busSelects = new StringList();
				busSelects.add(DomainConstants.SELECT_ID);
				MapList resultList = getBusObjInfo(context, strType, supplierName, strRev, whereClause, busSelects);
 
				if (resultList.isEmpty()) {
					String errInfo = "No active supplier found with name: " + supplierName;
					printerrfile.println(errInfo);
					continue;
				}
 
				for (Object result : resultList) {
					Map<?, ?> resultMap = (Map<?, ?>) result;
					String strObjectId = (String) resultMap.get(DomainConstants.SELECT_ID);
					if(UIUtil.isNotNullAndNotEmpty(strObjectId)){
						//Create Domain object
						DomainObject doObj = new DomainObject(strObjectId);
						StringList selectList = new StringList(4);
						selectList.add(DomainConstants.SELECT_NAME);
						selectList.add(DomainConstants.SELECT_DESCRIPTION);
						selectList.add("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");
						selectList.add("attribute[" + ATTRIBUTE_REGION + "]");
						selectList.add("attribute[" + ATTRIBUTE_INTERFACE_SPECRIGHT_ID + "]");
						String interfaceSelector = "interface[" + INTERFACE_TRUSPECRIGHTINTERFACE + "]";
						String hasInterface = doObj.getInfo(context, interfaceSelector);
						//Get fieldlist from properties for POST method
						String fieldList = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Common.FieldList");
						StringList attributeList = new StringList();
						if (UIUtil.isNotNullAndNotEmpty(fieldList)) {
							String[] fieldArray = fieldList.split(",");
							for (String fields : fieldArray) {
								String key = fields.trim();
								attributeList.add(key);
								String getAttr = PropertyUtil.getSchemaProperty("attribute_" + key);
								selectList.add("attribute[" + getAttr + "]");
							}
						}
						Map<?, ?> hashObjmap = doObj.getInfo(context, selectList);
						String strName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
						String strDescription = (String) hashObjmap.get(DomainConstants.SELECT_DESCRIPTION);
						String strEntityType = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");
						String strRegion = (String) hashObjmap.get("attribute[" + ATTRIBUTE_REGION + "]");
						//Check Region has Global value
						String globalRegion = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Region.Global");
						if(strRegion.contains(globalRegion)){
							strRegion = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Region.All");
						}
						//Set variable as key and value to match with properties entry
						Map<String, String> valueMap = new HashMap<>();
						valueMap.put("Name", strName);
						valueMap.put("Description", strDescription);
						valueMap.put("Region", strRegion);
						//Get Supplier/Impacted Site from properties to check the Entity Type
						String sImpactedSiteList = EnoviaResourceBundle.getProperty(context, "emxFrameworkStringResource", context.getLocale(), "emxFramework.Excel.ImpactedSiteList");
						String supplierDist = EnoviaResourceBundle.getProperty(context, "emxEngineeringCentral",context.getLocale(),"eServiceEngineeringCentral.BusinessUnit.SupplierClassification.Distributor");
						String supplierManu = EnoviaResourceBundle.getProperty(context, "emxEngineeringCentral", context.getLocale(),"eServiceEngineeringCentral.BusinessUnit.SupplierClassification.Manufacturer");
						StringList impactedSites = new StringList();
						if (UIUtil.isNotNullAndNotEmpty(sImpactedSiteList)) {
							String[] siteArray = sImpactedSiteList.split(",");
							for (String site : siteArray) {
								impactedSites.add(site.trim());
							}
						}
						StringList supplierTypes = new StringList();
						if (UIUtil.isNotNullAndNotEmpty(supplierDist)) {
							supplierTypes.add(supplierDist.trim());
						}
						if (UIUtil.isNotNullAndNotEmpty(supplierManu)) {
							supplierTypes.add(supplierManu.trim());
						}
						String kenvueCode = "";
						String recordTypeId = "";
						//Set InternalExternal field as External initially
						String internalExternal = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.External");
						if (impactedSites.contains(strEntityType)) {
							if(!strEntityType.contains(internalExternal)){
								//Change InternalExternal field to Internal
								internalExternal =  EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Internal");
							}
							kenvueCode = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.ImpactedSite.Fields");
							recordTypeId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.FillSite.RecordTypeId");
						} else if (supplierTypes.contains(strEntityType)) {
							kenvueCode = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Supplier.Fields");
							recordTypeId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.Supplier.RecordTypeId");
						}
						valueMap.put("InternalExternal", internalExternal);
						valueMap.put("RecordType", recordTypeId);
					
						String specrightId ="";
						//Use GET generic method to check if the Supplier/Site present in SpecRight
						String getFieldList = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.GetSpecData.ParameterValue.fields");
						String getTypeConnection = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.GetSpecData.getTypeSpec.Account");
						String filterList = "{\""+kenvueCode+"\":\""+strName+"\"}";
						HashMap<String, String> getReturnMap1 = getSpecData(context, getFieldList, getTypeConnection, filterList);
						String getResponse = (String) getReturnMap1.get("Response");
						String getResponseUrl = (String) getReturnMap1.get("ResponseUrl");
						String getResponseCode = (String) getReturnMap1.get("ResponseCode");
						//Do POST or PATCH if GET response code is success
						if("200".equals(getResponseCode) || "201".equals(getResponseCode)){
							JSONObject jsonAllData = new JSONObject(getResponse);
							JSONArray dataArray = jsonAllData.getJSONArray("data");
							if (dataArray.length() != 0) {
								JSONObject firstObject = dataArray.getJSONObject(0);
								JSONArray fieldsArray = firstObject.getJSONArray("fields");
								for (int i = 0; i < fieldsArray.length(); i++) {
									JSONObject fieldObject = fieldsArray.getJSONObject(i);
									if ("Id".equals(fieldObject.optString("field"))) {
										specrightId = fieldObject.optString("value");
										break;
									}
								}
							}
							//Do PATCH if SpecRight Id is present for the Supplier/Site
							if(UIUtil.isNotNullAndNotEmpty(specrightId)){
								//Get field list for PATCH method
								String patchFieldList = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.PatchNameEntity.FieldList");
								StringList patchAttributeList = new StringList();
								if (UIUtil.isNotNullAndNotEmpty(patchFieldList)) {
									String[] patchFieldArray = patchFieldList.split(",");
									for (String fields : patchFieldArray) {
										String key = fields.trim();
										patchAttributeList.add(key);
									}
								}
							
								JSONObject jsonContent = new JSONObject();
								for(int i=0; i<patchAttributeList.size(); i++){
									String patchAttributeName = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite."+patchAttributeList.get(i));
									String patchValue = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Value."+patchAttributeList.get(i));
									String patchAttributeValue = valueMap.get(patchValue);
									if (UIUtil.isNotNullAndNotEmpty(patchAttributeValue)) {
										patchValue = patchAttributeValue;
									}
									jsonContent.put(patchAttributeName, patchValue);
								}
								jsonContent.put(kenvueCode, strName);
							
								String jsonString = jsonContent.toString();
								String patchConnectionType = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader", context.getLocale(), "TRUSpecRightDataLoader.SpecRight.PatchType.Account");
								String[] patchArgsforspec = new String[]{jsonString,specrightId,accessToken,patchConnectionType};
								HashMap<String, String> patchReturnMap1 = patchSpecData(context, patchArgsforspec);
								String patchResponse = (String) patchReturnMap1.get("Response");
								String patchResponseUrl = (String) patchReturnMap1.get("ResponseUrl");							
								String patchResponseCode = (String) patchReturnMap1.get("ResponseCode");

								if("200".equals(patchResponseCode) || "201".equals(patchResponseCode)){
									//Check Interface is present in TRU
									if (!"TRUE".equalsIgnoreCase(hasInterface)) {
										doObj.addBusinessInterface(context, INTERFACE_TRUSPECRIGHTINTERFACE);
									}
									//Set SpecRight Id into the Interface
									Map<String, String> attrMap = new HashMap<>();
									attrMap.put(ATTRIBUTE_INTERFACE_SPECRIGHT_ID, specrightId);
									doObj.setAttributeValues(context, attrMap);
									String infoObj = strObjectId+" ~ "+strName+" ~ Success";
									printfile.println(infoObj);
								} else {
									String infoObj = strObjectId+" ~ "+strName+" ~ Failure";
									printfile.println(infoObj);
									String errInfo = strObjectId+" ~ "+strName+" ~ Patch response code: "+patchResponseCode+" URL: "+patchResponseUrl+" response: "+patchResponse;
									printerrfile.println(errInfo);
								} 
								//Do POST if SpecRight Id is not present for the Supplier/Site
							} else {								
								//Get other field list which are not present in TRU but present in SpecRight
								String otherFieldList = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Other.FieldList");
								StringList otherAttributeList = new StringList();
								if (UIUtil.isNotNullAndNotEmpty(otherFieldList)) {
									String[] otherFieldArray = otherFieldList.split(",");
									for (String fields : otherFieldArray) {
										String key = fields.trim();
										otherAttributeList.add(key);
									}
								}
								JSONObject jsonContent = new JSONObject();
								for(int i=0; i<attributeList.size(); i++){
									String attributeName = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite."+attributeList.get(i));
									String setAttr = PropertyUtil.getSchemaProperty("attribute_" + attributeList.get(i));
									String attributeValue = (String) hashObjmap.get("attribute[" + setAttr + "]");
									jsonContent.put(attributeName, attributeValue);
								}
								for(int i=0; i<otherAttributeList.size(); i++){
									String otherAttributeName = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite."+otherAttributeList.get(i));
									String otherValue = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Value."+otherAttributeList.get(i));
									String otherAttributeValue = valueMap.get(otherValue);
									if (UIUtil.isNotNullAndNotEmpty(otherAttributeValue)) {
									otherValue = otherAttributeValue;
									}
									jsonContent.put(otherAttributeName, otherValue);
								}
								jsonContent.put(kenvueCode, strName);

								String jsonString = jsonContent.toString();
								String postConnectionType = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader", context.getLocale(), "TRUSpecRightDataLoader.SpecRight.PatchType.Account");
								String[] postArgsforspec = new String[]{jsonString,accessToken,postConnectionType};
								HashMap<String, String> postReturnMap1 = postSpecData(context, postArgsforspec);
								String postResponse = (String) postReturnMap1.get("Response");
								String postResponseUrl = (String) postReturnMap1.get("ResponseUrl");
								String postResponseCode = (String) postReturnMap1.get("ResponseCode");

								if("200".equals(postResponseCode) || "201".equals(postResponseCode)){
									//Get SpecRight Id from the response
									JSONObject postResponseId = new JSONObject(postResponse);
									specrightId = postResponseId.optString("data");
									//Check Interface is present in TRU
									if (!"TRUE".equalsIgnoreCase(hasInterface)) {
										doObj.addBusinessInterface(context, INTERFACE_TRUSPECRIGHTINTERFACE);
									}
									//Set SpecRight Id into the Interface
									Map<String, String> attrMap = new HashMap<>();
									attrMap.put(ATTRIBUTE_INTERFACE_SPECRIGHT_ID, specrightId);
									doObj.setAttributeValues(context, attrMap);
									String infoObj = strObjectId+" ~ "+strName+" ~ Success";
									printfile.println(infoObj);
								}else{
									String infoObj = strObjectId+" ~ "+strName+" ~ Failure";
									printfile.println(infoObj);
									String errInfo = strObjectId+" ~ "+strName+" ~ Post response code: "+postResponseCode+" URL: "+postResponseUrl+" response: "+postResponse;
									printerrfile.println(errInfo);
								} 
							} 
						} else {
							String errInfo = strObjectId+" ~ "+strName+" ~ Get response code: "+getResponseCode+" URL: "+getResponseUrl+" response: "+getResponse;
							printerrfile.println(errInfo);
						}
					} else {
						String errInfo = "Not getting Object ID from TRU";
						printerrfile.println(errInfo);
					}
				}
			}
			printfile.close();
			printerrfile.close();
		} catch (Exception ex) {
			ex.printStackTrace();
			throw ex;
		}
	}
