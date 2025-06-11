this is from my properties file 
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Other.FieldList=Name,VendorId,KenvueCode,Description,Stage,SupplierType,Active,InternalExternal,RecordType
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Name=Name
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.StateRegion=BillingState
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.PostalCode=BillingPostalCode
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.OrganizationPhoneNumber=Phone
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.OrganizationFaxNumber=Fax
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.WebSite=Website
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.DESCRIPTION=Description
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.STAGE=specright__Status__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.VendorId=specright__Vendor_ID__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Region=SR_Region_Located__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.AlternateName=SR_Alternate_Supplier_Name_s__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.SUPPLIERTYPE=SR_Supplier_Type__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.City=SR_Supplier_City__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Country=SR_Supplier_Country__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.Active=specright__Active2__c
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.RecordType=RecordTypeId
TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.InternalExternal=SR_Internal_External__c
TRUSpecRightDataLoader.SpecRight.Tag.Supplier.RECORDTYPEID=012am000001rh3cAAA
TRUSpecRightDataLoader.SpecRight.Tag.FillSite.RECORDTYPEID=012am000001rh3tAAA



this is my code now 

String name = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.NAME");
			String desc = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.DESCRIPTION");
			String stage = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.STAGE");
			String vendorId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.VENDOR_ID");
			String suppliertype = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.SUPPLIERTYPE");
			String active = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.ACTIVE");
			String internalExternal = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.INTERNAL_EXTERNAL");
			String recordType = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.RECORDTYPE");




DomainObject doObj = new DomainObject(sTRUObjId);
			StringList selectList = new StringList(4);
			selectList.add(DomainConstants.SELECT_NAME);
			selectList.add(DomainConstants.SELECT_CURRENT);
			selectList.add(DomainConstants.SELECT_DESCRIPTION);
			selectList.add("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");


Map<?, ?> hashObjmap = doObj.getInfo(context, selectList);
			String strName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
			String strState = (String) hashObjmap.get(DomainConstants.SELECT_CURRENT);
			String strDescription = (String) hashObjmap.get(DomainConstants.SELECT_DESCRIPTION);
			String strEntityType = (String) hashObjmap.get("attribute[" + ATTRIBUTE_ENTITY_TYPE + "]");
			String externalOrNot = "External";

String kenvueCode = "";
			String recordTypeId = "";

			if (impactedSites.contains(strEntityType)) {
				if(!strEntityType.contains("External")){
					externalOrNot = "Internal";
				}
				kenvueCode = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.ImpactedSite.Fields");
				recordTypeId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.FillSite.RECORDTYPEID");
			} else if (supplierTypes.contains(strEntityType)) {
				kenvueCode = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Supplier.Fields");
				recordTypeId = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.Supplier.RECORDTYPEID");
			}

jsonContent.put(name, strName);
					jsonContent.put(vendorId, strName);
					jsonContent.put(kenvueCode, strName);
					jsonContent.put(desc, strDescription);
					jsonContent.put(stage, "Commercial");
					jsonContent.put(suppliertype, "Primary");
					jsonContent.put(active, "Yes");
					jsonContent.put(internalExternal, externalOrNot);
					jsonContent.put(recordType, recordTypeId);

I want it to have a map with key value so that i can put in json using a loop
