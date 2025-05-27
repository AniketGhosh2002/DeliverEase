String sImpactedSiteList = EnoviaResourceBundle.getProperty(context, "emxFrameworkStringResource", context.getLocale(), "emxFramework.Excel.ImpactedSiteList");


emxEngineeringCentral.properties
eServiceEngineeringCentral.BusinessUnit.SupplierClassification.Distributor=Supplier: Distributor

eServiceEngineeringCentral.BusinessUnit.SupplierClassification.Manufacturer=Supplier: Manufacturer



System.out.println("ImpactedSites " + sImpactedSiteList);
			
			StringList impactedSites = new StringList();
			if (sImpactedSiteList != null && !sImpactedSiteList.isEmpty()) {
				String[] siteArray = sImpactedSiteList.split(",");
				for (String site : siteArray) {
					impactedSites.add(site.trim());
				}
			}

if (impactedSites.contains(strEntityType)) {
				unitType = "Impacted Site";
				kenvueCode = FillSiteKenvueCode;
				recordTypeId = FillSiteRecordTypeId;
			} else {
				unitType = "Supplier";
				kenvueCode = SupplierKenvueCode;
				recordTypeId = SupplierRecordTypeId;
			}
