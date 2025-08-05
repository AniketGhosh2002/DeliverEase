public void createOrActiveSupplierData(Context context, String[] args) throws Exception{
		FileWriter logWriter = null;

		try {
			logWriter = generateLogWriter();
			logWriter.write("Execution started at " + new Date());
			logWriter.write(System.lineSeparator());
			logWriter.write(System.lineSeparator());
			
			//Generate access token 
			String accessToken = generateToken(context);
			if(UIUtil.isNotNullAndNotEmpty(accessToken)){
        		//Get parameter from the shell script
        		String cronTime = args[0];
        		String whereClause = "state[Active].actual > '"+cronTime+"' && " + DomainConstants.SELECT_CURRENT + " == Active";
        		StringList busSelects = new StringList();
        		busSelects.add(DomainConstants.SELECT_ID);
        		MapList resultList  = getBusObjInfo(context,TYPE_ORGANIZATION,DomainConstants.QUERY_WILDCARD,DomainConstants.QUERY_WILDCARD,whereClause,busSelects);
	  	}
    }catch(){
    }
    }
