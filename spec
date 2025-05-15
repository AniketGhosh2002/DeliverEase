String entityType = "attribute\[Entity Type\]"
		
		String getEntityTypeQuery = "print bus $1 select $2;
		String getEntityType = MqlUtil.mqlCommand(context,getEntityTypeQuery, sTRUObjId, entityType);



and i need to separate unitType based on the which entityType is that like for 

  Impacted Site ------>
Other,Internal Manufacturing,Co-packers,Laboratory,External Manufacturing,External Packaging,Distribution Center,Company,R&D,Marketing Company,Business Location
 
Supplier  --------->
Supplier: Distributor
Supplier: Manufacturer
