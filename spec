import com.matrixone.apps.domain.util.ContextUtil;
import com.matrixone.apps.domain.util.MqlUtil;

import matrix.db.Context;
import matrix.db.JPO;

public class jnjTRUDocumentExpiry
{
	private static String PASSPORTURL = "";
	private static String SERVICEURL  = "";
	private static String USER        = "";
	private static String PASSWORD    = "";
	private static String ROLE        = "";
	private static String PATH        = "";
	
	private static Context context    = null;

	public static void main(String [] args)
	{
		try
		{
			if(args != null && args.length > 5)
			{
				PASSPORTURL = args[0];
				SERVICEURL  = args[1];
				USER        = args[2];
				PASSWORD    = args[3];
				ROLE        = args[4];
				PATH        = args[5];
				
				System.setProperty("bypass.cert", "true");
				context = getEnoviaConnection();
				
				if(context == null)
				{
					return;
				}
				
				try
				{
					String [] paramArgs = new String[1];
					paramArgs[0] = PATH;
					JPO.invoke(context, "ENODCLEffectivityTrigger", null, "autoPromoteDocumentToObsoleteOrInactive", paramArgs, Object.class);
				}
				catch(Exception exp)
				{
					exp.printStackTrace();
					System.out.println("The Above Transaction Has Been Rolled back");
				}
			}
		}
		catch(Exception e)
		{
			e.printStackTrace();
			
			try
			{
				context.close();
			}
			catch(Exception ex)
			{
				ex.printStackTrace();
			}
		}
		finally
		{
			try
			{
				context.close();
			}
			catch(Exception ex)
			{
				ex.printStackTrace();
			}
		}
	}

	private static Context getEnoviaConnection()
	{
		try
		{
			if(context != null && context.isConnected())
			{
				return context;
			}
			
			context = Util.connect( SERVICEURL, PASSPORTURL, USER, PASSWORD, ROLE, "", true);
		}
		catch(Exception e)
		{
			System.out.println("Exception in Setting ENOVIA Context");
			e.printStackTrace();
		}
		finally
		{
			return context;
		}
	}
}
