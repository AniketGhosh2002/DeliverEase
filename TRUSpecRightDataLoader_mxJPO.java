import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

import com.matrixone.apps.domain.DomainConstants;
import com.matrixone.apps.domain.DomainObject;
import com.matrixone.apps.domain.util.EnoviaResourceBundle;
import com.matrixone.apps.domain.util.FrameworkUtil;
import com.matrixone.apps.domain.util.MapList;
import com.matrixone.apps.domain.util.PropertyUtil;
import com.matrixone.apps.framework.ui.UIUtil;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

import matrix.db.JPO;
import matrix.db.BusinessInterface;
import matrix.db.Context;
import matrix.db.MatrixWriter;
import matrix.util.StringList;

import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import org.apache.commons.codec.binary.Base64;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;
import org.apache.jena.atlas.json.JSON;
import org.json.JSONArray;
import org.json.JSONObject;
import java.net.http.HttpClient;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.Arrays;
import java.util.Iterator;
import java.util.HashMap;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;

import com.matrixone.apps.domain.util.PersonUtil;

public class TRUSpecRightDataLoader_mxJPO {
	
	// Global variable declaration
	public Context ctx = null;
	BufferedWriter writer = null;
	MatrixWriter mxWriter = null;
	MatrixWriter mxWriter1 = null;
	public static String sVault = "";
	public static String acessToken=null;
	public static String inputJson=null;
	public static String SPECRIGHT_USERNAME = null;
	public static String SPECRIGHT_PASSWORD = null;
	public static String TOKEN_URL = null;
	public static final String ATTRIBUTE_TRANSACTION_STATUS = PropertyUtil.getSchemaProperty("attribute_TransactionStatus");
	public static final String ATTRIBUTE_OUTPUT_XML = PropertyUtil.getSchemaProperty("attribute_OutputXML");
	public static final String ATTRIBUTE_DC_SPEC_NUMBER = PropertyUtil.getSchemaProperty("attribute_DCSpecNumber");
	public static final String ATTRIBUTE_DC_SPEC_ID = PropertyUtil.getSchemaProperty("attribute_DCSpecID");
	public static final String ATTRIBUTE_TRANSACTION_EVENT = PropertyUtil.getSchemaProperty("attribute_TransactionEvent");
	public static final String ATTRIBUTE_INPUT_XML = PropertyUtil.getSchemaProperty("attribute_InputXML");
	public static final String ATTRIBUTE_ARTWORK_ID = PropertyUtil.getSchemaProperty("attribute_DCArtworkID");
	public static final String ATTRIBUTE_SPECRIGHT_API_TOKEN = PropertyUtil.getSchemaProperty("attribute_SpecRightAPIToken");
	public static final String ATTRIBUTE_SPECRIGHT_SPEC_NUMBER = PropertyUtil.getSchemaProperty("attribute_SpecrightObjName");
	private static final BusinessInterface TruSpecRightInterface = new BusinessInterface("TruSpecRightInterface", null);
	
	public TRUSpecRightDataLoader_mxJPO (Context context, String[] args) throws Exception {
		// Added check to throw an exception if the context is null
		if(context == null)
			throw new Exception("Inside TRUSpecRightDataLoader constructor, the context is null");
		writer = new BufferedWriter(new MatrixWriter(context));
		mxWriter = new MatrixWriter(context);
		ctx = context;
		sVault = PropertyUtil.getSchemaProperty(ctx, "vault_eServiceProduction");
		SPECRIGHT_USERNAME = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
				context.getLocale(), "TRUSpecRightDataLoader.SpecRight.UserName");
		System.out.println("****SPECRIGHT_USERNAME***"+SPECRIGHT_USERNAME);
		SPECRIGHT_PASSWORD = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
				context.getLocale(), "TRUSpecRightDataLoader.SpecRight.Password");
		System.out.println("****SPECRIGHT_PASSWORD***"+SPECRIGHT_PASSWORD);
		TOKEN_URL = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
				context.getLocale(), "TRUSpecRightDataLoader.SpecRight.AcessTokenUrl");
		System.out.println("****TOKEN_URL***"+TOKEN_URL);
	}
	public TRUSpecRightDataLoader_mxJPO () throws Exception {
	}
	
	/**
	 * @author : Pramit Mitra (pmitra01)
	 * @purpose : Method to determine if a specification is created from SpecRight (AATL-).
	 * @return : true (if created from SpecRight) or false
	 */
	public boolean isSpecRightSpec(Context context, String sSpecId) throws Exception
	{
		boolean retFlag = false;
		
		try
		{
			if(context != null)
			{
				DomainObject doSpec = new DomainObject(sSpecId);
				
				if(doSpec != null)
				{
					String sSpecRightNum = doSpec.getInfo(context,"attribute[" + ATTRIBUTE_SPECRIGHT_SPEC_NUMBER + "]");
					
					if(UIUtil.isNotNullAndNotEmpty(sSpecRightNum))
					{
						retFlag = true;
					}
				}
			}
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			return retFlag;
		}
	}
	/**
	 * @author : Pramit Mitra (pmitra01)
	 * @purpose : Method to determine if a specification created (or not created) from SpecRight can be revised/copied/edited from the UI (AATL-).
	 * @param : MODE (within map) = REVISE/COPY/EDIT
	 * @return : true (if allowed) or false
	 */
	public boolean canModifySpecRightSpec(Context context, String[]args) throws Exception
	{
		HashMap programMap = (HashMap)JPO.unpackArgs(args);
		boolean retFlag = false;
		
		try
		{
			String sSpecId = (String)programMap.get("SPEC_ID");
			String sMode = (String)programMap.get("MODE");
			String sSpecRight = "NonSpecRight";
			
			if(isSpecRightSpec(context,sSpecId))
			{
				sSpecRight = "SpecRight";
			}
			
			String sSpecType = new DomainObject(sSpecId).getInfo(context,DomainConstants.SELECT_TYPE);
			String sPropKey = "TRUSpecRightDataLoader." + sSpecRight + "." + sSpecType.replaceAll(" ","") + "." + sMode + ".PermittedRoles";
			String sPermittedRoles = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader", context.getLocale(), sPropKey);
			
			System.out.println("---canModifySpecRightSpec----sPropKey---"+sPropKey);
			System.out.println("---canModifySpecRightSpec----sPermittedRoles---"+sPermittedRoles);
			
			if(!sPropKey.equals(sPermittedRoles))
			{
				StringList slPermittedRoles = FrameworkUtil.split(sPermittedRoles, ",");
				System.out.println("---canModifySpecRightSpec----slPermittedRoles---"+slPermittedRoles);
				
				if(slPermittedRoles != null)
				{
					Iterator itr = slPermittedRoles.iterator();
					
					while(itr.hasNext())
					{
						String sRole = (String)itr.next();
						
						if(PersonUtil.hasAssignment(context, sRole))
						{
							retFlag = true;
							break;
						}
					}
				}
			}
			else
			{
				retFlag = true;
			}
			System.out.println("---canModifySpecRightSpec----retFlag---"+retFlag);
		}
		catch(Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			return retFlag;
		}
	}
	public void processSpecRightData(Context context, String[] args) throws Exception {
		
		acessToken = generateToken(context, args);
		inputJson = getSpecData(context, acessToken);
		readaAndSplitInputJson(context, inputJson);
	}
	public String generateToken(Context context, String[] args) throws Exception {
		URL url;
		OutputStream stream;
		OutputStreamWriter oStreamWrt;
		String jsonBodyKey = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
				context.getLocale(), "TRUSpecRightDataLoader.SpecRight.AcessToken.ParameterKey");
		String jsonBodyValue = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
				context.getLocale(), "TRUSpecRightDataLoader.SpecRight.AcessToken.ParameterValue");
		JSONObject json = new JSONObject();
		json.put(jsonBodyKey, jsonBodyValue);
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);
		String auth = SPECRIGHT_USERNAME + ":" + SPECRIGHT_PASSWORD;
		byte[] encodedAuth = Base64.encodeBase64(auth.getBytes());
		String authType = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",
				context.getLocale(), "TRUSpecRightDataLoader.SpecRight.AcessToken.AuthType");
		System.out.println("****authType***"+authType);
		
		String contentType = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.AcessToken.ContentType");
		System.out.println("****contentType***"+contentType);
		
		String basicAuth  = authType+" "+new String(encodedAuth);
		System.out.println("...............basicAuth: "+basicAuth);
		int responseCode = 0;
		int retryCount = 0;
		while (responseCode != 200 && retryCount < 3) {
			try {
				url = new URL(TOKEN_URL);
				HttpsURLConnection https = (HttpsURLConnection)url.openConnection();
				https.setRequestMethod("POST");
				https.setDoOutput(true);
				https.setRequestProperty("Content-Type", contentType);
				https.setRequestProperty("Authorization", basicAuth);
				https.setConnectTimeout(60000);

				stream = https.getOutputStream();
				stream.write(out);
				// Flush the stream to ensure all data is sent
				stream.flush();

				responseCode = https.getResponseCode();
				StringBuilder response = new StringBuilder();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(https.getInputStream()));
					String inputLine;
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
					JSONObject jo = new JSONObject(response.toString());
					acessToken = jo.getString("access_token");
					System.out.println("...............accessToken: "+acessToken);
				} else {
					System.out.println("...............responseCode: "+responseCode);
					System.out.println("...............response: "+response);
				}
			}catch (Exception e) {
				e.printStackTrace();
			}
			retryCount++;
		}
		return acessToken;

	}
	public String getSpecData(Context context, String acessToken2) throws Exception {
		URL url;
		String inputLine = null;
		String fieldKey = "fields";
		String fieldList = "Id,Name,specright__Status__c";
		System.out.println(fieldList);
		String filterKey = "filter";
		String inputJson = null;
		String filterList = "{\"SR_State__c\":\"Unpublished\"},{\"IsDeleted\":\"false\"}}";
		//URL obj = new URL("{{host}}/objects/specright__Specification__c?");
		int responseCode = 0;
		int retryCount = 0;
		while (responseCode != 200 && retryCount < 3) {
			try {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/objects/specright__Specification__c?").addParameter(fieldKey, "FIELDS(ALL)").addParameter(filterKey, filterList);
				System.out.println(uri.toString());
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestMethod("GET");
				//String accessToken = generateToken(context, acessToken2);
				String auth = "Bearer " + acessToken2;
				//con.setDoOutput(true);
				con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
				con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
				con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
				con.setRequestProperty("Authorization", auth);

				responseCode = con.getResponseCode();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
					inputJson = response.toString();
				} else {

				}
			}catch (Exception e) {
				e.printStackTrace();
			}
			retryCount++;
		}
		System.out.println("**********IT IS IN GET SPEC DATA METHOD**********");
		return inputJson;
	}
	public String readaAndSplitInputJson(Context context, String inputJson2) throws Exception {
		String truObjId=null;
		String sTxnId=null;
		String truObjCurrent=null;
		System.out.println("**********IT IS IN READ AND SPLIT DATA METHOD at Begining**********");
		HashMap<String, String> hmAttrMap = new HashMap<String, String>();
		HashMap<String,String> txAttributeMap = new HashMap<String, String>();
		System.out.println("*****--------------****** " +inputJson2);
		JSONObject jsonObj = new JSONObject(inputJson2.toString());
		System.out.println("*****--------------****** ");
		JSONArray ja_data = jsonObj.getJSONArray("data");
		int ja_data_length = ja_data.length();
		
		System.out.println("*****inputJson2****** " +inputJson2);
		System.out.println("*****hmAttrMap****** " +hmAttrMap);
		System.out.println("******txAttributeMap******** " +txAttributeMap);
		System.out.println("********ja_data_length********** " +ja_data_length);
		
		
		try {
		System.out.println("**********IT IS IN READ AND SPLIT DATA METHOD at TRY BLOCK**********");
		for(int i=0; i<ja_data_length; i++) 
		{
			JSONObject jObj = ja_data.getJSONObject(i);
			System.out.println("**********IT IS IN READ AND SPLIT DATA METHOD at FOR LOOP**********");
			sTxnId = FrameworkUtil.autoName(context,"type_Transaction","", "policy_Transaction", "vault_eServiceProduction"); 
			System.out.println("\n*** inside createSpecConcerto- sTxnId : "+sTxnId);
			DomainObject doTxn = DomainObject.newInstance(context, sTxnId);
			//txAttributeMap.put(ATTRIBUTE_INPUT_XML, jObj.toString());
			doTxn.addBusinessInterface(context, TruSpecRightInterface);
			doTxn.setAttributeValue(context, ATTRIBUTE_INPUT_XML, jObj.toString());
			doTxn.setAttributeValue(context, ATTRIBUTE_SPECRIGHT_API_TOKEN, acessToken);
			doTxn.setDescription("SpecRightAPI");
			doTxn.promote(context);
			
		}
		}catch(Exception ex) {
			ex.printStackTrace();
			System.out.println("**********IT IS IN READ AND SPLIT DATA METHOD at Catch BLOCK**********");
		}
		System.out.println("**********IT IS IN READ AND SPLIT DATA METHOD at the END**********");
		return null;

	}
	public String createSpec(Context context, HashMap<String, String> hmAttrMap, String sTxnId) {
		String sPolicy = "";
		String sStage = "";
		//Added For Story AATL-22185 - START
		String sStageDevelopment = "";
		String sStageCommercial = "";
		//Added For Story AATL-22185 - END
		String sTemplate = "";
		String  sDesignResp = "";
		String  sExpiration = "";
		String sChangeTmptOID = "";
		String sCOID = "";
		String strSpecId = "";
		try {
			String specRightOwnerId = hmAttrMap.get("attribute[Owner]");
			String truOwnerId = validateOwner(context,specRightOwnerId);
		}catch(Exception ex) {
			ex.printStackTrace();
		}
		
		return null;
	}
	public String validateOwner(Context context, String specRightOwnerId) {
		String ownerEmail = getOwnerDetails(context,specRightOwnerId);
		String ownerId = getBusObjectId(context,jnjBomConstants_mxJPO.TYPE_PERSON, null, DomainConstants.QUERY_WILDCARD,"attribute["+jnjBomConstants_mxJPO.ATTRIBUTE_EMAIL_ADDRESS+"]=="+ownerEmail+" && current==Active");
		return ownerId;
		
	}
	public String getOwnerDetails(Context context, String specRightOwnerId) {
		String ownerEmail=null;
		URL url;
		String inputLine = null;
		String fieldKey = "fields";
		String fieldList = "Email";
		System.out.println(fieldList);
		HashMap<String, String> hmOwnerMap = new HashMap<String, String>();
		int responseCode = 0;
		int retryCount = 0;
		while (responseCode != 200 && retryCount < 3) {
			try {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/objects/User/"+specRightOwnerId).addParameter(fieldKey, fieldList);
				System.out.println(uri.toString());
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestMethod("GET");
				//String accessToken = generateToken(context, acessToken2);
				String auth = "Bearer " + acessToken;
				//con.setDoOutput(true);
				con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
				con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
				con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
				con.setRequestProperty("Authorization", auth);

				responseCode = con.getResponseCode();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
					JSONObject jsonObj = new JSONObject(response.toString());
					JSONArray ja_data = jsonObj.getJSONArray("data");
					for(int i=0; i<ja_data.length(); i++) 
					{
						JSONObject jObj = ja_data.getJSONObject(i);
						JSONArray fieldArray = jsonObj.getJSONArray("fields");
						for(int j=0; i<fieldArray.length(); j++) 
						{
							JSONObject fieldObj = fieldArray.getJSONObject(i);
							String field = fieldObj.getString("field");
							String fieldValue = fieldObj.getString("value");
							hmOwnerMap.put(fieldKey, fieldValue);
					}
					}
					ownerEmail = hmOwnerMap.get("Email");
				} else {

				}
			}catch (Exception e) {
				e.printStackTrace();
			}
			retryCount++;
		}
		return specRightOwnerId;
		
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
	public String patchSpecData(Context context, String[] args) throws IOException {
		URL url;
		OutputStream stream;
		String inputLine = null;
		//String specRightId="a1mWF000000tJd7YAE";
		String specRightId="a1mWF000001eHCrYAM";
		int responseCode = 0;
		int retryCount = 0;
		
		String jsonString = args[0];
		JSONObject jsonobject = new JSONObject(jsonString);
		String state = jsonobject.optString("SR_State__c");
		String effectiveDate = jsonobject.optString("SR_TRU_Record_Effective_Date__c");
		String access1 = jsonobject.optString("accessToken");
		
		
		JSONObject jsonContent = new JSONObject();
		jsonContent.put("specright__Status__c", "");
		jsonContent.put("SR_Region_s__c", "EMEA");
		jsonContent.put("SR_Language__c", "English");
		jsonContent.put("SR_State__c", state);
		
		if("Effective".equalsIgnoreCase(state)){
			jsonContent.put("SR_TRU_Record_Effective_Date__c", effectiveDate);
		}
		
		JSONObject json = new JSONObject();
		json.put("content", jsonContent);
		System.out.println(json.toString());
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);
		try {
			//String accessToken = generateToken(context, args);
			while (responseCode != 200 && retryCount <= 3) {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/objects/specright__Specification__c/a1mWF000001eHCrYAM");
				System.out.println(uri.toString());
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestProperty("X-HTTP-Method-Override", "PATCH");
				con.setRequestMethod("POST");
				String auth = "Bearer " + access1;
				con.setDoOutput(true);
				con.setRequestProperty("Content-Type", "application/json");
				con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
				con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
				con.setRequestProperty("Authorization", auth);
				con.setConnectTimeout(60000);
				stream = con.getOutputStream();
				stream.write(out);
				// Flush the stream to ensure all data is sent
				stream.flush();

				responseCode = con.getResponseCode();
				System.out.println(responseCode);
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
				} else {

				}
				retryCount++;
			}
		}catch (Exception e) {
			e.printStackTrace();
		}

		return inputLine;

	}
	public String getSupplierData(Context context, String[] args) throws Exception {
		URL url;
		String inputLine = null;
		String fieldKey = "fields";
		String fieldList = "Id,Name,specright__Status__c";
		System.out.println(fieldList);
		String filterKey = "filter";
		String filterList = "{\"SR_State__c\":\"Unpublished\"},{\"IsDeleted\":\"false\"}}";
		//URL obj = new URL("{{host}}/objects/specright__Specification__c?");
		int responseCode = 0;
		int retryCount = 0;
		while (responseCode != 200 && retryCount <= 3) {
			try {
				URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers?").addParameter(fieldKey, "Id,Name");
				System.out.println(uri.toString());
				url = uri.build().toURL();
				HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
				con.setRequestMethod("GET");
				String accessToken = generateToken(context, args);
				String auth = "Bearer " + accessToken;
				//con.setDoOutput(true);
				con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
				con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
				con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
				con.setRequestProperty("Authorization", auth);

				responseCode = con.getResponseCode();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
							new InputStreamReader(con.getInputStream()));
					StringBuffer response = new StringBuffer();
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					System.out.println(response.toString());
				} else {

				}
			}catch (Exception e) {
				e.printStackTrace();
			}
			retryCount++;
		}
		return inputLine;
	}
	
/* 	public String updateTruSpec(Context context, String[] args) throws IOException {
		try {
			// Unpack the arguments
			HashMap programMap = JPO.unpackArgs(args);
			HashMap requestMap = (HashMap)programMap.get("requestMap");
			HashMap paramMap = (HashMap)programMap.get("paramMap");
			
			// Extract values from maps
			String inputJSON = (String)paramMap.get("inputJSON");
			String strTransactionId = (String)paramMap.get("strTransactionId");
			String strTRUId = (String)requestMap.get("strTRUId");
	 
			// Print the extracted values
			System.out.println("--- Extracted Values ---");
			System.out.println("strTransactionId: " + strTransactionId);
			System.out.println("strTRUId: " + strTRUId);
			System.out.println("inputJSON: " + inputJSON);
	 
			// Parse and iterate through inputJSON if it exists
			if (inputJSON != null && !inputJSON.isEmpty()) {
				try {
					System.out.println("\n--- Parsing inputJSON ---");
					JSONObject jsonObject = new JSONObject(inputJSON);
					
					// Print all key-value pairs in the JSON
					Iterator<String> keys = jsonObject.keys();
					while (keys.hasNext()) {
						String key = keys.next();
						Object value = jsonObject.get(key);
						System.out.println(key + ": " + value);
					}
				} catch (Exception jsonEx) {
					System.out.println("Error parsing inputJSON: " + jsonEx.getMessage());
					jsonEx.printStackTrace();
				}
			} else {
				System.out.println("inputJSON is null or empty");
			}
	 
			// TODO: Add your business logic here to update TRU Spec
			
			return "Success"; // Return appropriate response
	 
		} catch (Exception e) {
			System.out.println("Error in updateTruSpec: " + e.getMessage());
			e.printStackTrace();
			return "Error: " + e.getMessage();
		}
	} */
	
	
	
		public String updateTruSpec(Context context, String[] args) throws Exception {
			try {
				// Validate input arguments

		 
				// Unpack the arguments properly
				HashMap programMap = JPO.unpackArgs(args);
				if (programMap == null) {
					throw new IllegalArgumentException("Failed to unpack arguments");
				}
		 
		 
				// Extract values with null checks
				Map inputJSON = (Map)programMap.get("inputJSON");
				String strTransactionId = (String)programMap.get("strTransactionId");
				String strTRUId = (String)programMap.get("strTRUId");
				

				// Log extracted values
				System.out.println("--- Extracted Values ---");
				System.out.println("Transaction ID: " + strTransactionId);
				System.out.println("TRU ID: " + strTRUId);
				System.out.println("Input JSON: " + inputJSON);
		 
				// Process the inputJSON if present
				if (inputJSON != null && !inputJSON.isEmpty()) {
					try {
						System.out.println("\n--- Parsing inputJSON ---");
						JSONObject jsonObject = new JSONObject(inputJSON);
						
						// Print all key-value pairs in the JSON
						Iterator<String> keys = jsonObject.keys();
						while (keys.hasNext()) {
							String key = keys.next();
							Object value = jsonObject.get(key);
							System.out.println(key + ": " + value);
						}
					} catch (Exception e) {
						System.out.println("Error processing inputJSON: " + e.getMessage());
					}
				}
				HashMap<String, String> hmJsonFieldMap = new HashMap<String, String>();
				HashMap<String,String> truAttributeMap = new HashMap<String, String>();
				JSONObject jsonObj = new JSONObject(inputJSON);
				JSONArray fieldArray = jsonObj.getJSONArray("fields");
				int fieldArray_length = fieldArray.length();
				for(int i=0; i<fieldArray_length; i++) 
				{
					JSONObject fieldObj = fieldArray.getJSONObject(i);
					String field = fieldObj.getString("field");
					String fieldValue = fieldObj.getString("value");
					String truAttr = EnoviaResourceBundle.getProperty(context, "TRUSpecRightDataLoader",context.getLocale(), "TRUSpecRightDataLoader.SpecRight.ActualAttribute."+field);
					
					DomainObject doBusObject = new DomainObject(strTRUId);
					doBusObject.setAttributeValues(context, truAttributeMap);
					hmJsonFieldMap.put(truAttr, fieldValue);
				}
				
		 
				return "Success"; // Or return appropriate response
		 
			} catch (Exception e) {
				System.out.println("Error in updateTruSpec: " + e.getMessage());
				e.printStackTrace();
				throw e; // Re-throw to see the error in the client
			}
		}
		 
	
	/**
	 * This method is called during promotion of the transaction object. It will set the event as effective/obsolete/reject/delete
	 *
	 * @param context  - Enovia context
	 * @param strObjId - Object Id for which status to be sent back
	 *
	 * @return void
	 * @throws none
	 * @author TCS()
	 *
	 */
	 public void promoteTransactionObject(Context context, String[] args) throws Exception{
		System.out.println("\n*** inside promoteTransactionObject***");

		String strTxnId1 = args[0];
		//String strTxnId1 = "";
		System.out.println("Spec bus Id: "+strTxnId1);
		
		/* String sTxnEvent = args[1];
		System.out.println("Spec txn event: "+sTxnEvent); */
		
		String sSignature = args[1];
		System.out.println("Spec txn sSignature: "+sSignature);
		
		/* if ("Effective".equalsIgnoreCase(sSignature)) {	
			//set event
			txnObject.setAttributeValue(context, ATTRIBUTE_TRANSACTION_EVENT, "Effective");
			//promote transaction
			txnObject.promote(context);
		}else if("Obsolete".equals(sSignature)) {
			//set event
			txnObject.setAttributeValue(context, ATTRIBUTE_TRANSACTION_EVENT, "Obsolete");
			//promote transaction
			txnObject.promote(context);			
		} else if("Rejection".equals(sSignature)) {
			
		} else if("Delete".equals(sSignature)) {
			
		}	 */

	}
	
	
	/**
	 * This method updates the state details in SpecRight when spec is promoted to Effective in TRU
	 *
	 * @param context  - Enovia context
	 * @param strObjId - Object Id for which status to be sent back
	 *
	 * @return void
	 * @throws none
	 * @author TCS()
	 *
	 */
	 public void updateStateToEffectiveInSpecRight(Context context, String[] args, String strTxnId) throws Exception{
		System.out.println("\n*** inside updateStateToEffectiveInSpecRight***");
		//generatetoken
		String accessToken = generateToken(context, args);
		System.out.println("accessToken: "+accessToken);
		
		String strObjId = strTxnId;
		System.out.println("Spec bus Id: "+strObjId);
		
		DomainObject doObj = new DomainObject(strObjId);
		StringList selectList = new StringList(5);
		selectList.add(DomainConstants.SELECT_TYPE);
		selectList.add(DomainConstants.SELECT_NAME);
		selectList.add(DomainConstants.SELECT_REVISION);
		selectList.add(DomainConstants.SELECT_CURRENT);
		selectList.add("attribute[Effective Date]");

		Map hashObjmap = doObj.getInfo(context, selectList);
		String strType = (String) hashObjmap.get(DomainConstants.SELECT_TYPE);
		String strName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
		String strRevision = (String) hashObjmap.get(DomainConstants.SELECT_REVISION);
		String strState = (String) hashObjmap.get(DomainConstants.SELECT_CURRENT);
		String strEffectiveDate = (String) hashObjmap.get("attribute[Effective Date]");
		
		System.out.println("***Object info from TRU:" +strType + " " +strName + " " +strRevision + " " +strState +" "+strEffectiveDate);
		
		String input = strEffectiveDate;
		DateTimeFormatter inputFormatter = DateTimeFormatter.ofPattern("M/d/yyyy h:mm:ss a");
		LocalDateTime localDateTime = LocalDateTime.parse(input, inputFormatter);
		ZonedDateTime zonedDateTime = localDateTime.atZone(ZoneId.of("UTC"));
		DateTimeFormatter outputFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSSZ");

	    String formatted = zonedDateTime.format(outputFormatter);
	    System.out.println(formatted); 

		//check if current is effective in TRU
		if("Effective".equalsIgnoreCase(strState))	{	
			System.out.println("***state is effective. patch update in specright***");

				JSONObject jsonContent = new JSONObject();
				jsonContent.put("SR_State__c", "Effective");
				jsonContent.put("SR_TRU_Record_Effective_Date__c",formatted); //Effective date
				jsonContent.put("accessToken",accessToken); 
				
				
				String jsonString = jsonContent.toString();
				String[] patchArgs = new String[]{jsonString};
				
				patchSpecData(context,patchArgs); 
				
		   } else{
				System.out.println("***State not effective in TRU***");
		} 
	}
	
	/**
	 * This method updates the state details in SpecRight when spec is promoted to Obsolete in TRU
	 *
	 * @param context  - Enovia context
	 * @param strObjId - Object Id for which status to be sent back
	 *
	 * @return void
	 * @throws none
	 * @author TCS()
	 *
	 */
	 public void updateStateToObsoleteInSpecRight(Context context, String[] args, String strTxnId) throws Exception{
		System.out.println("\n*** inside updateStateToObsoleteInSpecRight***");
		//generatetoken
		String accessToken = generateToken(context, args);
		System.out.println("accessToken: "+accessToken);
		
		String strObjId = strTxnId;
		System.out.println("Spec bus Id: "+strObjId);
		
		DomainObject doObj = new DomainObject(strObjId);
		StringList selectList = new StringList(4);
		selectList.add(DomainConstants.SELECT_TYPE);
		selectList.add(DomainConstants.SELECT_NAME);
		selectList.add(DomainConstants.SELECT_REVISION);
		selectList.add(DomainConstants.SELECT_CURRENT);

		Map hashObjmap = doObj.getInfo(context, selectList);
		String strType = (String) hashObjmap.get(DomainConstants.SELECT_TYPE);
		String strName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
		String strRevision = (String) hashObjmap.get(DomainConstants.SELECT_REVISION);
		String strState = (String) hashObjmap.get(DomainConstants.SELECT_CURRENT);
		
		System.out.println("***Object info from TRU:" +strType + " " +strName + " " +strRevision + " " +strState);
		

		//check if current is obsolete in TRU
		if("Obsolete".equalsIgnoreCase(strState))	{	
			System.out.println("***state is obsolete. patch update in specright***");

				JSONObject jsonContent = new JSONObject();
				jsonContent.put("SR_State__c", "Obsolete");
				jsonContent.put("accessToken",accessToken); 
				
				
				String jsonString = jsonContent.toString();
				String[] patchArgs = new String[]{jsonString};
				
				patchSpecData(context,patchArgs); 
		} else{
				System.out.println("***State not obsolete in TRU***");
		}
	}
	
	
	
	public String refreshToken(Context context, String sTxnId) throws Exception {
		URL url;
		OutputStream stream;
		OutputStreamWriter oStreamWrt;
		String refreshToken = DomainConstants.EMPTY_STRING;
		String strAcessToken = DomainConstants.EMPTY_STRING;
		if(UIUtil.isNotNullAndNotEmpty(sTxnId)) {
		DomainObject doObj = new DomainObject(sTxnId);
		String strToken = doObj.getAttributeValue(context, "ATTRIBUTE_SPECRIGHT_API_TOKEN");
		if(UIUtil.isNotNullAndNotEmpty(strToken)) {
		System.out.println("---sAttributeAPIToken **" + strToken);

		System.out.println("---AttributeValue **" + strToken);
		
		JSONObject json = new JSONObject();
		json.put("grant_type", "refresh_token");
		json.put("refresh_token", strToken);
		byte[] out = json.toString().trim().getBytes(StandardCharsets.UTF_8);
		String tokenUrl = "https://test.specright.com/token";
		int responseCode = 0;
		int retryCount = 0;
		
		while (responseCode != 200 && retryCount <= 3) {
			try {
				url = new URL(tokenUrl);
				HttpsURLConnection https = (HttpsURLConnection)url.openConnection();
				https.setRequestMethod("POST");
				https.setDoOutput(true);
				https.setRequestProperty("Content-Type", "application/json");
				https.setConnectTimeout(60000);

				stream = https.getOutputStream();
				stream.write(out);
				// Flush the stream to ensure all data is sent
				stream.flush();

				responseCode = https.getResponseCode();
				StringBuilder response = new StringBuilder();
				if(responseCode==200) {
					BufferedReader in = new BufferedReader(
					new InputStreamReader(https.getInputStream()));
					String inputLine;
					while ((inputLine = in.readLine()) != null) {
						response.append(inputLine);
					}
					in.close();
					//System.out.println(response.toString());
					JSONObject jo = new JSONObject(response.toString());
					strAcessToken = jo.getString("access_token");
					System.out.println("...............accessToken..."+strAcessToken);
					refreshToken = jo.getString("refresh_token");
					System.out.println("...............refreshToken..."+refreshToken);
				} else {

				}
			}catch (Exception e) {
				e.printStackTrace();
			}
			retryCount++;
		}
			
		}

		}

		return strAcessToken;

	}
	
	/**
	 * If specright spec is rejected by approver in TRU , 
	 * this method will demote the state back to draft in TRU and specright
	 *
	 * @param context  - Enovia context
	 * @param strObjId - Object Id for which status to be sent back
	 *
	 * @return void
	 * @throws none
	 * @author TCS()
	 *
	 */
	 public void demoteSpecStateOnReject(Context context, String[] args) throws Exception{
		System.out.println("\n*** inside demoteSpecStateOnReject***");
		//generatetoken
		String accessToken = generateToken(context, args);
		System.out.println("accessToken: "+accessToken);
		
		String strTxnId = args[0];
		//String strTxnId = "59712.34061.48640.52216";
		System.out.println("Spec bus Id: "+strTxnId); 

		
		DomainObject doObj = new DomainObject(strTxnId);
		StringList selectList = new StringList(3);
		selectList.add(DomainConstants.SELECT_TYPE);
		selectList.add(DomainConstants.SELECT_NAME);
		selectList.add(DomainConstants.SELECT_REVISION);
		selectList.add(DomainConstants.SELECT_CURRENT);

		Map hashObjmap = doObj.getInfo(context, selectList);
		String strType = (String) hashObjmap.get(DomainConstants.SELECT_TYPE);
		String strName = (String) hashObjmap.get(DomainConstants.SELECT_NAME);
		String strRevision = (String) hashObjmap.get(DomainConstants.SELECT_REVISION);
		String strState = (String) hashObjmap.get(DomainConstants.SELECT_CURRENT);
		
		System.out.println("***Object info from TRU:" +strType + " " +strName + " " +strRevision + " " +strState);
		
		String strRouteStatus="";
		
		StringList slSelRel = new StringList();
		slSelRel.add("attribute[Route Status]");
		
		StringList slSelBus = new StringList();
		slSelBus.add(DomainConstants.SELECT_NAME); 
		slSelBus.add(DomainConstants.SELECT_ID); 
		
		MapList mlConnectedObjectList = doObj.getRelatedObjects(context,
				"Object Route", "Route", slSelBus,
				slSelRel, false, true, (short) 1, null, null);
		
		System.out.println("......mlConnectedObjectList......."+mlConnectedObjectList);
		int iMapListSize1 = mlConnectedObjectList.size();
		
		for (int iLoop1 = 0; iLoop1 < iMapListSize1; iLoop1++) {
			Map mEachObjectMap = (Map) mlConnectedObjectList.get(iLoop1);
			String strRouteId = (String) mEachObjectMap.get(DomainConstants.SELECT_ID);
			
			DomainObject routeObj = new DomainObject(strRouteId);
			
			strRouteStatus = routeObj.getInfo(context,"attribute[Route Status]");
		
			System.out.println("......strRouteStatus......."+strRouteStatus);
		}	
		
		//check if spec is rejected by approver in TRU
		if("Stopped".equalsIgnoreCase(strRouteStatus)){
		System.out.println("***route is rejected. patch update in specright***");

				JSONObject jsonContent = new JSONObject();
				jsonContent.put("SR_State__c", "Draft");
				jsonContent.put("accessToken",accessToken); 
				
				
				String jsonString = jsonContent.toString();
				String[] patchArgs = new String[]{jsonString};
				
				patchSpecData(context,patchArgs); 
		} else{
				System.out.println("***State not obsolete in TRU***");
		}
		
	}
		// Post method for Supplier
	
		public String postSupplierData(Context context, String[] args) throws Exception {
			URL url;
			StringBuilder response = new StringBuilder();
			String inputLine = null;
			String fieldKey = "fields";
			String fieldList = "Name";
			System.out.println(fieldList);
			String strObjName = args[0];
			int responseCode = 0;
			int retryCount = 0;
			while (responseCode != 200 && retryCount <= 3) {
				try {
					URIBuilder uri = new URIBuilder("https://test.specright.com/v1/suppliers");
					System.out.println(uri.toString());
					url = uri.build().toURL();
					HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
					con.setRequestMethod("POST");
					con.setDoOutput(true);
					
					String accessToken = generateToken(context, args);
					String auth = "Bearer " + accessToken;
					//con.setDoOutput(true);
					con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
					con.setRequestProperty("x-user-id", "api@specright.com.kenvuedev");
					con.setRequestProperty("x-api-key", "he6rFkRDeEvrwAg9Dl70d3Fox0aNfmB82EwHQdzI");
					con.setRequestProperty("Authorization", auth);
					
					String jsonInputString = "{\"Name\": \"" + strObjName + "\"}";
					
					try (OutputStream outStream = con.getOutputStream()) {
		                byte[] input = jsonInputString.getBytes("utf-8");
		                outStream.write(input, 0, input.length);
		            }
					
					responseCode = con.getResponseCode();
					if(responseCode==200) {
						BufferedReader in = new BufferedReader(
								new InputStreamReader(con.getInputStream()));
						//StringBuffer response = new StringBuffer();
						while ((inputLine = in.readLine()) != null) {
							response.append(inputLine);
						}
						in.close();
						System.out.println(response.toString());
					} else {
						System.out.println("...............responseCode: "+responseCode);
						System.out.println("...............response: "+response);
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
			return inputLine;
		}
		
}