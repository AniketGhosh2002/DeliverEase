	Input File : Will have name of all Supplier/Site, separate files 5-6
	Shell file : will accept the Path/Name of Input file and pass it to your JPO method
	JPO method :
		Will read the input file line by line [one name per line]


public void createOrActiveSupplierData(Context context, String[] args) throws Exception{

		System.out.println("**********inside createOrActivateSupplierData**********");
		try {

			String CRONTIME = args[0];
			String strType = TYPE_ORGANIZATION;
			String strName = DomainConstants.QUERY_WILDCARD;
			String strRev = DomainConstants.QUERY_WILDCARD;
			String whereClause = "state[Active].actual > '"+CRONTIME+"' && current == Active";
			StringList busSelects = new StringList();
			busSelects.add(DomainConstants.SELECT_ID);
			MapList resultList  = getBusObjInfo(context,strType,strName,strRev,whereClause,busSelects);
			// Iterate over MapList
			if(resultList.size() >0){
				for (int i = 0; i < resultList.size(); i++) {
					Map resultMap = (Map) resultList.get(i);
					String strObjectId = (String) resultMap.get("id");

					System.out.println("Supplier bus Id: "+strObjectId);

					String sTxnId=null;

					sTxnId = FrameworkUtil.autoName(context,"type_Transaction","", "policy_Transaction", "vault_eServiceProduction"); 
					System.out.println("\n*** inside promoteTransactionObject- sTxnId : "+sTxnId);
					DomainObject txnObject = DomainObject.newInstance(context, sTxnId);

					DomainObject dObject = new DomainObject(strObjectId);
					StringList selectList = new StringList(2);
					selectList.add(DomainConstants.SELECT_NAME);
					selectList.add(DomainConstants.SELECT_CURRENT);
					selectList.add("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");

					Map hashObjmap = dObject.getInfo(context, selectList);
					String sState = (String) hashObjmap.get(DomainConstants.SELECT_CURRENT);
					String sName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
					String strEntityType = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");

					System.out.println("***Object info from TRU:" +sState +" " +sName + " " +strEntityType);

					String event = "CreateorActivateSupplierSite";


					System.out.println("\n*** inside Active : ***");
					HashMap<String,String> hmAttributeMap = new HashMap<>();
					hmAttributeMap.put(ATTRIBUTE_TRANSACTION_EVENT, event);
					hmAttributeMap.put(ATTRIBUTE_DC_SPEC_ID, strObjectId);
					hmAttributeMap.put(ATTRIBUTE_DC_SPEC_NUMBER, sName);
					//hmAttributeMap.put("description", "SpecRight");
					txnObject.setAttributeValues(context, hmAttributeMap);
					txnObject.setDescription(context,"SpecRight");

					//promote transaction
					txnObject.promote(context);
				}
			}
		} catch(Exception ex) {
			ex.printStackTrace();
		}
	}
