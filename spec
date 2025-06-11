InputStream errorStream = con.getErrorStream();
if (errorStream != null) {
    BufferedReader in = new BufferedReader(new InputStreamReader(errorStream));
    StringBuffer errorResponse = new StringBuffer();
    while ((inputLine = in.readLine()) != null) {
        errorResponse.append(inputLine);
    }
    in.close();
    System.out.println("Error Response: " + errorResponse.toString());
    String errorJson = errorResponse.toString();

    try {
        JSONObject obj = new JSONObject(errorJson);
        if (obj.has("message")) {
            message = obj.getString("message");
        }
        returnJsonString = message;
    } catch (Exception jsonEx) {
        returnJsonString = errorJson; // fallback raw string if not valid JSON
    }

} else {
    message = "No error stream returned (HTTP " + responseCode + ")";
    System.out.println(message);
    returnJsonString = message;
}
