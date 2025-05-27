DomainObject doObj = new DomainObject(sTRUObjId);
			StringList selectList = new StringList(1);

selectList.add("attribute[" + ATTRIBUTE_REGION + "]");
Map hashObjmap = doObj.getInfo(context, selectList);
			String strRegion = (String) hashObjmap.get("attribute[" + ATTRIBUTE_REGION + "]");
