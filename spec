public static final String STATE_REGION = PropertyUtil.getSchemaProperty("attribute_StateRegion");

String fieldList = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Tag.SupplierFillSite.FieldList");
			StringList attributeList = new StringList();
			if (fieldList != null && !fieldList.isEmpty()) {
				String[] siteArray = fieldList.split(",");
				for (String site : siteArray) {
					attributeList.add(site.trim());
				}
			}
			for(int i=0; i<attributeList.size(); i++){
				System.out.println(attributeList.get(i));
				selectList.add("attribute[" + attributeList.get(i) + "]");
			}
			
			
			
but it not work as 
selectList.add("attribute[" + STATE_REGION + "]");
