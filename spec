public void sendEmail (String sFromMailId , String sToMailId, String sCCMailId, String sMailSubject, String sMailBody) throws Exception {
		boolean sSendMail = true;
		//compose the message  
		try {

			//Get the session object  
			Properties properties = System.getProperties();
			properties.setProperty("mail.smtp.host", strSmtpHost);
			Session session = Session.getDefaultInstance(properties);  
			MimeMessage message = new MimeMessage(session);

			message.setFrom(new InternetAddress(sFromMailId));
			message.setSubject(sMailSubject);
			if (null != sToMailId && !"".equals(sToMailId))
			{
				InternetAddress aInternetAddress[] = InternetAddress.parse(sToMailId.trim());
				message.setRecipients(Message.RecipientType.TO, aInternetAddress);
				if(null!=sCCMailId && !"".equals(sCCMailId))
				{
					InternetAddress aInternetAddressCC[] = InternetAddress.parse(sCCMailId.trim());
					message.setRecipients(Message.RecipientType.CC, aInternetAddressCC);
				}
			}
			message.setContent(sMailBody.replaceAll("\n", "<br />"),"text/html");  

			if(sSendMail)
				javax.mail.Transport.send(message);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
