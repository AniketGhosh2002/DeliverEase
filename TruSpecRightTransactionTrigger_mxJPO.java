import org.json.JSONArray;
import org.json.JSONObject;

import java.util.*;

import matrix.db.Context;
import matrix.db.JPO;
import matrix.util.StringList;

import com.matrixone.apps.domain.DomainConstants;
import com.matrixone.apps.domain.DomainObject;
import com.matrixone.apps.domain.util.*;

public class TruSpecRightTransactionTrigger_mxJPO{
	//Global Variables
	public static final String ATTRIBUTE_TRANSACTION_STATUS = PropertyUtil.getSchemaProperty("attribute_TransactionStatus");
	public static final String ATTRIBUTE_OUTPUT_XML = PropertyUtil.getSchemaProperty("attribute_OutputXML");
	public static final String ATTRIBUTE_DC_SPEC_NUMBER = PropertyUtil.getSchemaProperty("attribute_DCSpecNumber");
	public static final String ATTRIBUTE_DC_SPEC_ID = PropertyUtil.getSchemaProperty("attribute_DCSpecID");
	public static final String ATTRIBUTE_TRANSACTION_EVENT = PropertyUtil.getSchemaProperty("attribute_TransactionEvent");
	public static final String ATTRIBUTE_INPUT_XML	= PropertyUtil.getSchemaProperty("attribute_InputXML");
	public static final String ATTRIBUTE_ARTWORK_ID	= PropertyUtil.getSchemaProperty("attribute_DCArtworkID");
	public static String EACH_INPUT_JSON = null;
	public static String sVault ="";

	public TruSpecRightTransactionTrigger_mxJPO () throws Exception {

	}
	public String  getBusObjectId(Context context,String sType, String sName, String sRev,String sWhereClause)
	{
		sVault=PropertyUtil.getSchemaProperty(context, "vault_eServiceProduction");
		if (sWhereClause.equals("") || sWhereClause.trim().length() == 0)
		{
			sWhereClause = null;
		}

		String sBusType                     = "";
		String sBusName                     = "";
		String sBusRev                      = "";
		String sBusId                       = "";

		MapList busObjList                  = null;

		try
		{
			StringList busSelects = new StringList();
			busSelects.add(DomainObject.SELECT_ID);

			busObjList  =   DomainObject.findObjects(context, sType, sName, sRev, null, sVault, sWhereClause, true, busSelects);
			int iSize = busObjList.size();
			//for(int iLoop = 0; iLoop < iSize; iLoop++) {
			if (iSize > 0) {
				Map busMap          = (Map)busObjList.get(iSize - 1);
				sBusId              = (String)busMap.get(DomainObject.SELECT_ID);
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
			sBusId  = "";
		}

		return sBusId;
	}
	public void startTransactionProcess(Context context, String[] args) throws Exception {
		System.out.println("**********IT IS IN begining startTransactionProcess Trigger Program**********");
		String truObjId=null;
		String sTxnId=args[0];
		String truObjCurrent=null;
		String truTemplateId=null;
		String truTemplateName=null;
		String truTemplateRev=null;
		String fieldValue=null;
		DomainObject txnObject = DomainObject.newInstance(context, sTxnId);
		String txnName = args[1];
		StringList objSelectList = new StringList();
		objSelectList.add(DomainConstants.SELECT_DESCRIPTION);
		objSelectList.add("attribute[" + ATTRIBUTE_INPUT_XML + "]");
		objSelectList.add("attribute[" + ATTRIBUTE_TRANSACTION_EVENT + "]");
		Map hashObjmap = txnObject.getInfo(context, objSelectList);
		String txDescription = (String) hashObjmap.get(DomainConstants.SELECT_DESCRIPTION);
		EACH_INPUT_JSON = (String) hashObjmap.get("attribute[" + ATTRIBUTE_INPUT_XML + "]");
		String transactionEvent = (String) hashObjmap.get("attribute[" + ATTRIBUTE_TRANSACTION_EVENT + "]");
		System.out.println("****transactionEvent***"+transactionEvent);
		try {
			if(txDescription!=null || !"".equals(txDescription) && "SpecRightAPI".equals(txDescription)) {
				if("".equals(transactionEvent) || transactionEvent == null) {
					HashMap<String, String> hmJsonFieldMap = new HashMap<String, String>();
					HashMap<String,String> txAttributeMap = new HashMap<String, String>();
					JSONObject jsonObj = new JSONObject(EACH_INPUT_JSON);
					JSONArray fieldArray = jsonObj.getJSONArray("fields");
					int fieldArray_length = fieldArray.length();
					for(int i=0; i<fieldArray_length; i++) 
					{
						System.out.println("****Inside statTransaction for index"+i);
						JSONObject fieldObj = fieldArray.getJSONObject(i);
						String field = fieldObj.getString("field");
						System.out.println("****Inside statTransaction for field"+field);
						if(!"IsDeleted".equals(field)) {
						fieldValue = fieldObj.getString("value");
						}
						String truAttr = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
								context.getLocale(), "TRUSpecRightDataLoader.SpecRight.ActualAttribute."+field);
						if("Id".equals(field)) {
							txAttributeMap.put(ATTRIBUTE_ARTWORK_ID, fieldValue);
						}
						txnObject.setAttributeValues(context, txAttributeMap);
						hmJsonFieldMap.put(field, fieldValue);
					}
					if(hmJsonFieldMap.get("SR_TRU_Record_ID__c") == null) {
						txnObject.setAttributeValue(context, ATTRIBUTE_TRANSACTION_EVENT, "Create");
						//call create
						System.out.println("****Inside Create If block***");
						String[] strArgs = JPO.packArgs(hmJsonFieldMap);
						TRUSpecRightDataLoader_mxJPO productDataToCreate = new TRUSpecRightDataLoader_mxJPO(context,strArgs);
						truObjId = productDataToCreate.createSpec(context,hmJsonFieldMap,sTxnId);
					} else {
						String truObjName=hmJsonFieldMap.get("SR_TRU_Record_ID__c");
						String truObjRev=hmJsonFieldMap.get("SR_TRU_Record_Revision__c");
						System.out.println("****Inside Else block 115***");
						truObjId = getBusObjectId(context,jnjBomConstants_mxJPO.TYPE_PACKAGING_COMPONENT, truObjName, DomainConstants.QUERY_WILDCARD,"revision =="+truObjRev);
						if(truObjId!=null) {
							DomainObject domTruObj = DomainObject.newInstance(context, truObjId);
							truObjCurrent = domTruObj.getInfo(context, DomainConstants.SELECT_CURRENT);
							StringList truTemplateInfo = new StringList();
							truTemplateInfo.add(DomainConstants.SELECT_ID);
							truTemplateInfo.add(DomainConstants.SELECT_NAME);
							truTemplateInfo.add(DomainConstants.SELECT_REVISION);
							MapList mlList = domTruObj.getRelatedObjects(context,jnjBomConstants_mxJPO.RELATIONSHIP_TEMPLATE,jnjBomConstants_mxJPO.TYPE_TEMPLATE,truTemplateInfo,null,false,true,(short) 1,null,null);
							for (int iMapLoop = 0; iMapLoop < mlList.size(); iMapLoop++) {
								Map mlMap = (Map)mlList.get(iMapLoop);
								truTemplateId=(String) mlMap.get(DomainConstants.SELECT_ID);
								truTemplateName=(String) mlMap.get(DomainConstants.SELECT_NAME);
								truTemplateRev=(String) mlMap.get(DomainConstants.SELECT_REVISION);
							}
							String truTemplateLatestId = getBusObjectId(context,jnjBomConstants_mxJPO.TYPE_TEMPLATE, truTemplateName, DomainConstants.QUERY_WILDCARD,"current == Effective && revision == last");
							String specRightTemplate =hmJsonFieldMap.get("SR_TRU_Record_Template__c");
							if(truTemplateName.equals(specRightTemplate) && truTemplateLatestId.equals(truTemplateId)) {
								if("Draft".equals(truObjCurrent)) {
									//call Update
									System.out.println("***************Inside UPDATE If block***********");
 									txnObject.setAttributeValue(context, ATTRIBUTE_TRANSACTION_EVENT, "Edit");

									// Correct way to call the method
									HashMap updateMap = new HashMap();
									updateMap.put("inputJSON", hmJsonFieldMap); // Ensure hmJsonFieldMap is properly initialized
									updateMap.put("strTransactionId", sTxnId);  // Ensure sTxnId is not null
									updateMap.put("strTRUId", truObjId);       // Ensure trueObjId is not null

									// Pack the arguments correctly
									String[] strUpdateArgs = JPO.packArgs(updateMap);
									 
									// Call the method
									TRUSpecRightDataLoader_mxJPO productDataToUpdate = new TRUSpecRightDataLoader_mxJPO();
									String result = productDataToUpdate.updateTruSpec(context, strUpdateArgs);
									
								}else if("Effective".equals(truObjCurrent)) {
									//call Revise 
									txnObject.setAttributeValue(context, ATTRIBUTE_TRANSACTION_EVENT, "Revise");
								} else {
									//Error
								}
							}
						}else {
							//Error
						}
					}
				}else {
					if("Effective".equals(transactionEvent)) {
						TRUSpecRightDataLoader_mxJPO sendEffectiveState = new TRUSpecRightDataLoader_mxJPO(context,args);
						sendEffectiveState.updateStateToEffectiveInSpecRight(context,args,sTxnId);
					} else if("Obsolete".equals(transactionEvent)) {
						TRUSpecRightDataLoader_mxJPO sendObsoleteState = new TRUSpecRightDataLoader_mxJPO(context,args);
						sendObsoleteState.updateStateToObsoleteInSpecRight(context,args,sTxnId); 
					} else if("Rejection".equals(transactionEvent)) {
						
					} else if("Delete".equals(transactionEvent)) {
						
					}
				}
			}
		}catch(Exception ex) {
			ex.printStackTrace();
		}
	}
}