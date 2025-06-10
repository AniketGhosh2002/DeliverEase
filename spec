public void createOrActiveBulkSupplierData(Context context, String[] args) throws Exception {
		System.out.println("********** Inside createOrActiveSupplierBulkData (File Input) **********");
		try {
			String inputFilePath = args[0];
			System.out.println("Get path in args " + inputFilePath);
			java.io.File file = new java.io.File(inputFilePath);
			if (!file.exists()) {
				System.out.println("Input file does not exist: " + inputFilePath);
				return;
			}

			java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.FileReader(file));
			String supplierName = null;

			while ((supplierName = reader.readLine()) != null) {
				supplierName = supplierName.trim();
				if (supplierName.isEmpty()) continue;

				System.out.println("Processing supplier/site: " + supplierName);
				String strType = TYPE_ORGANIZATION;
				String strRev = DomainConstants.QUERY_WILDCARD;
				String whereClause = "current == Active";
				StringList busSelects = new StringList();
				busSelects.add(DomainConstants.SELECT_ID);
				busSelects.add(DomainConstants.SELECT_NAME);
				busSelects.add(DomainConstants.SELECT_CURRENT);
				MapList resultList  = getBusObjInfo(context,strType,supplierName,strRev,whereClause,busSelects);

				if (resultList.isEmpty()) {
					System.out.println("No active supplier found with name: " + supplierName);
					continue;
				}

				for (Object result : resultList) {
					Map<?, ?> resultMap = (Map<?, ?>) result;
					String strObjectId = (String) resultMap.get(DomainConstants.SELECT_ID);
					String sName = (String) resultMap.get(DomainConstants.SELECT_NAME);
					String sState = (String) resultMap.get(DomainConstants.SELECT_CURRENT);

					System.out.println("Supplier found: ID=" + strObjectId + ", Name=" + sName + ", State=" + sState);

					String sTxnId = FrameworkUtil.autoName(context, "type_Transaction", "", "policy_Transaction", "vault_eServiceProduction");
					DomainObject txnObject = DomainObject.newInstance(context, sTxnId);

					Map<String, String> hmAttributeMap = new HashMap<>();
					hmAttributeMap.put(ATTRIBUTE_TRANSACTION_EVENT, "CreateorActivateSupplierSite");
					hmAttributeMap.put(ATTRIBUTE_DC_SPEC_ID, strObjectId);
					hmAttributeMap.put(ATTRIBUTE_DC_SPEC_NUMBER, sName);
					txnObject.setAttributeValues(context, hmAttributeMap);
					txnObject.setDescription(context, "SpecRight");

					txnObject.promote(context);
				}
			}
			reader.close();
		} catch (Exception ex) {
			ex.printStackTrace();
			throw ex;
		}
	}
