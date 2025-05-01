Impacted Site and/or Supplier is activated in TRU	A manufacturing site, marketing company, business unit or a supplier/distributor is activated in TRU	"- TRU sends back feed to SpecRight.
- TRU sends creates/updates supplier in SpecRight."	TRU sends site/supplier name, status (Active), other required fields & "Success"/"Published" flag back to SpecRight.			As the TRU system owner, I want TRU to be integrated with SpecRight to send back response when any supplier or site is activated, updated or deactivated.	"1. Supplier/Site activated in TRU

2. Supplier/SIte updated in TRU

3. Supplier/SIte deactivated in TRU"
Impacted Site (and/or Supplier) is deactivated in TRU	A manufacturing site, marketing company, business unit or a supplier/distributor is deactivated in TRU	"- TRU sends back feed to SpecRight.
- TRU marks supplier as Inactive in SpecRight."	TRU sends site/supplier status (Inactive) & "Success"/"Published" flag back to SpecRight.				




{
	"content": {
		"Name": "SupplierTest04"
	}
}


{
    "data": "001WF00000MFLlqYAH",
    "success": true
}

System Error: #5000002: Compile error:
/usr/tmp/1069820/TruSpecRightTransactionTrigger_mxJPOe8661e0b0100000146.java:139: error: cannot find symbol
                                                        String patchResponse = patchCall.patchSupplierData(context, patchArgs);
                                                                                        ^
  symbol:   method patchSupplierData(matrix.db.Context,java.lang.String[])
  location: variable patchCall of type TRUSpecRightDataLoader_mxJPO3e650e6c0100000249
Note: Some input files use or override a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
Note: /usr/tmp/1069820/TruSpecRightTransactionTrigger_mxJPOe8661e0b0100000146.java uses unchecked or unsafe operations.
Note: Recompile with -Xlint:unchecked for details.



JSONObject json = new JSONObject();
		json.put("content", jsonContent);
		System.out.println(json.toString());
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);
