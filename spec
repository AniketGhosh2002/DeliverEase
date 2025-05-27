DomainObject parentObj = new DomainObject(strSpecId);

			DomainObject doChar= (DomainObject) DomainObject.newInstance(context);
			DomainRelationship dr = doChar.createAndConnect(context,strType,relationshipName, parentObj, true);
			StringList relSelects = new StringList(3);
			relSelects.add(DomainRelationship.SELECT_TO_ID);
			relSelects.add(DomainRelationship.SELECT_FROM_ID);
			relSelects.add(DomainRelationship.SELECT_ID);
			Hashtable relData = dr.getRelationshipData(context, relSelects);
			StringList SLtmp =  (StringList) relData.get(DomainRelationship.SELECT_TO_ID);
			String objID = (String)SLtmp.get(0);
			DomainObject newObj = new DomainObject(objID);
			//SLtmp = (StringList) relData.get(DomainRelationship.SELECT_ID);
			//String sRelId = (String)SLtmp.get(0);

			//Modification by TCS for fix TRU-22934 ends 8/19/2016
			//DomainRelationship.setAttributeValues(context,sRelId,hmRelAttrMap);
			newObj.setAttributeValues(context, hmTableAttrMap);
