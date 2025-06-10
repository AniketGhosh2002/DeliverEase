-------------------------------- CRON RUN DETAILS ---------------------------------
Run Started At   : Tue Jun 10 02:51:42 EDT 2025

Step 1: Reading CronRun file...
Start Date for Processing: 06/09/2025 06:29:32 AM

Step 2: Executing createOrActiveSupplierData with Start Date...

Matrix Query Language Interface, Version 3DEXPERIENCE R2021x HotFix 8 (64 bits)

Copyright (c) 1993-2020 Dassault Systemes.
All rights reserved.
****SPECRIGHT_USERNAME***api@specright.com.kenvuedev
****SPECRIGHT_PASSWORD***bQ7p@D-Y^dkN637a
****TOKEN_URL***https://test.specright.com/token
**********inside createOrActivateSupplierData**********
........Inside getBusObjInfo...sType:..Organization
........Inside getBusObjInfo...sName:..*
........Inside getBusObjInfo...sRev:..*
........Inside getBusObjInfo...sWhereClause:..state[Active].actual > '06/09/2025 06:29:32 AM' && current == Active
........Inside getBusObjInfo...busSelectables:..[id]
Supplier bus Id: 59712.34061.31704.59357

*** inside promoteTransactionObject- sTxnId : 59712.34061.30498.27308
***Object info from TRU:Active EM-Malda External Manufacturing

*** inside Active : ***
**********IT IS IN begining startTransactionProcess Trigger Program**********
****transactionEvent***CreateorActivateSupplierSite
****txDescription***SpecRight

*** inside CreateorActivateSupplierSite in Transaction : 
****SPECRIGHT_USERNAME***api@specright.com.kenvuedev
****SPECRIGHT_PASSWORD***bQ7p@D-Y^dkN637a
****TOKEN_URL***https://test.specright.com/token
*** Inside createOrActiveSupplierDetailsToSpecRight ***
****authType***Basic
****contentType***application/json
...............basicAuth: Basic YXBpQHNwZWNyaWdodC5jb20ua2VudnVlZGV2OmJRN3BARC1ZXmRrTjYzN2E=
{"access_token":"eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhcGlAc3BlY3JpZ2h0LmNvbS5rZW52dWVkZXYiLCJhdWQiOiJodHRwczpcL1wvbG9naW4uc3BlY3JpZ2h0LmNvbSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE3NDk1NDE5MjksImlhdCI6MTc0OTUzODMyOX0.EnBmyj4QhOdukfvFV8Skhovp5JNUDuizhyIkyhFqwp6JZUfIt7SZvrsdgZLm4_Sj8ccHbahLKYsuIosBB-lRr_VJ08ElRI_gpON1EZyfngacqiMydpg08xS0Ojlq5CD8h27CF0zjuHQWi2gQZh0sXYF9Bu8DOrZGZfT_6YuZ7ZMwZBOXg_geTVataqI_dF7NiS-GX3h8F89Vgx2E9St3XJgj618BKkO58m8QLcHAnPFul8GthFedwLjSMQD3Q4LsucpX44fIj-AdPf2hTIxwoAzHDs9Fm7c8TGQN9j4oqYc7e1_Il5bCNJYOrZhU13sKpTS3zxunw0Djr3ONMzj7yA95eE4Yxoj9GdEfu_dY-r7Y8V5bzZ6eeOtclkVse8EofZIFeGdmvqNhOcpX-GGXwIunR0lRTLVGQDZdUzNd5TmbAkB0wApa8Cj2dq4BQI3DyBolbf9gQc3tFWAbFINyek0h3SkB-IJpgaoICxegOg-jVxts2IctNkpNL4tOUXH2gEYiXC59EZ4QqdV1yu65kIF5Tw9C_OomvsW7N55vPOm3ufq1ORWdjV1RXVlXFmQuQic4Glr2h174tvdArMZY8yY76xkDT1S_r193k1z-rq8DNgEiwVDv8F5oKTW5O2K98vAW1iDMOcc7Q_tkSEaOZ1MIuVrFMq4r32NQ2YZFWjA","token_type":"bearer","expires_in":3600,"refresh_token":"eyJlbmMiOiJBMTI4R0NNIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.YqXdSDib00U3kcy4MCYPyWO-9nlEXiPweI2-DCuZLZJ75RYa87VRn3TMGBStxoVkbb6Jd1q24f5q6wegncs6eyClrAY915itR7fQdWnFLFqoUS2pI2YIbbOmO58heg6eSeMzLMoB4uUOPHYQnahHWemHp_7ufWO2lt2zCFDoX6WHxFMPZH1_dCFSdZ4wyDGnj7eS43I3Ta3s2bD3q_0GafSGTYzklxKN9iIUfUDBSiSHk92GnwdWSdzJxEPqnm91hd7P40S5HYo9ZWhjY8d37-eayp2WXe0hwnTp6-DmsLnqici-NEwPTR-Pd8TQipz3xCRjzMLkQGE5P4-mZ_R2Xtn0oXIRKSA9eTWAnPhCNmB6i61QJv2X8CDP0h1srMROS5YLCB-gEtAyAOWSQRSX17vTtsiZfbtQm9QmjTzGxpU8JRVHejHNT8AuOeAvB9V3Zkl3HdzKV2ar92uzatUMK5upFZ6xA9Psn44nhsJDR7v87oNYkM23NPOPzkG1Aex3b1cVS84IdutOOHPi9aSgyqqxLk5bPA6iDY-N3h2aUnFFeTXdnlOU7zuC9EttEMZSMRqy6o9N3Tru9GQEq4FZCnhmTO7kmTNEfZUrLascb2a3ukaCGD-QuJJi0XXuuIrbVqXn43V_51Ok-btosgrhN2VfsqIb0Vu-pPL67mVDRUo.i5KzpxQHmcUR7voA.ojLBk1zDCTLVzN7daBAbnFBdo4ddWLTaI2FB995L3Ll8DTqjiOcgYbuFESq_Lko2jFfbkPgjAqSLHPu3sQrrsp_tWQlNTGEldlXvKUKap-MD2f6SSGMVIjItJf7pVR0mt0F794B1ByFeLk8WtJfQsZtKbkKLDfuPy7OffIife9UXhfGQ.ibOVp_VpePfdRyDXaPxWZA"}
...............accessToken: eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhcGlAc3BlY3JpZ2h0LmNvbS5rZW52dWVkZXYiLCJhdWQiOiJodHRwczpcL1wvbG9naW4uc3BlY3JpZ2h0LmNvbSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE3NDk1NDE5MjksImlhdCI6MTc0OTUzODMyOX0.EnBmyj4QhOdukfvFV8Skhovp5JNUDuizhyIkyhFqwp6JZUfIt7SZvrsdgZLm4_Sj8ccHbahLKYsuIosBB-lRr_VJ08ElRI_gpON1EZyfngacqiMydpg08xS0Ojlq5CD8h27CF0zjuHQWi2gQZh0sXYF9Bu8DOrZGZfT_6YuZ7ZMwZBOXg_geTVataqI_dF7NiS-GX3h8F89Vgx2E9St3XJgj618BKkO58m8QLcHAnPFul8GthFedwLjSMQD3Q4LsucpX44fIj-AdPf2hTIxwoAzHDs9Fm7c8TGQN9j4oqYc7e1_Il5bCNJYOrZhU13sKpTS3zxunw0Djr3ONMzj7yA95eE4Yxoj9GdEfu_dY-r7Y8V5bzZ6eeOtclkVse8EofZIFeGdmvqNhOcpX-GGXwIunR0lRTLVGQDZdUzNd5TmbAkB0wApa8Cj2dq4BQI3DyBolbf9gQc3tFWAbFINyek0h3SkB-IJpgaoICxegOg-jVxts2IctNkpNL4tOUXH2gEYiXC59EZ4QqdV1yu65kIF5Tw9C_OomvsW7N55vPOm3ufq1ORWdjV1RXVlXFmQuQic4Glr2h174tvdArMZY8yY76xkDT1S_r193k1z-rq8DNgEiwVDv8F5oKTW5O2K98vAW1iDMOcc7Q_tkSEaOZ1MIuVrFMq4r32NQ2YZFWjA
accessToken: eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhcGlAc3BlY3JpZ2h0LmNvbS5rZW52dWVkZXYiLCJhdWQiOiJodHRwczpcL1wvbG9naW4uc3BlY3JpZ2h0LmNvbSIsInR5cGUiOiJhY2Nlc3NfdG9rZW4iLCJleHAiOjE3NDk1NDE5MjksImlhdCI6MTc0OTUzODMyOX0.EnBmyj4QhOdukfvFV8Skhovp5JNUDuizhyIkyhFqwp6JZUfIt7SZvrsdgZLm4_Sj8ccHbahLKYsuIosBB-lRr_VJ08ElRI_gpON1EZyfngacqiMydpg08xS0Ojlq5CD8h27CF0zjuHQWi2gQZh0sXYF9Bu8DOrZGZfT_6YuZ7ZMwZBOXg_geTVataqI_dF7NiS-GX3h8F89Vgx2E9St3XJgj618BKkO58m8QLcHAnPFul8GthFedwLjSMQD3Q4LsucpX44fIj-AdPf2hTIxwoAzHDs9Fm7c8TGQN9j4oqYc7e1_Il5bCNJYOrZhU13sKpTS3zxunw0Djr3ONMzj7yA95eE4Yxoj9GdEfu_dY-r7Y8V5bzZ6eeOtclkVse8EofZIFeGdmvqNhOcpX-GGXwIunR0lRTLVGQDZdUzNd5TmbAkB0wApa8Cj2dq4BQI3DyBolbf9gQc3tFWAbFINyek0h3SkB-IJpgaoICxegOg-jVxts2IctNkpNL4tOUXH2gEYiXC59EZ4QqdV1yu65kIF5Tw9C_OomvsW7N55vPOm3ufq1ORWdjV1RXVlXFmQuQic4Glr2h174tvdArMZY8yY76xkDT1S_r193k1z-rq8DNgEiwVDv8F5oKTW5O2K98vAW1iDMOcc7Q_tkSEaOZ1MIuVrFMq4r32NQ2YZFWjA
Spec txn Id: 59712.34061.30498.27308
Suppplier bus Id from TXN: 59712.34061.31704.59357
Suppplier bus Name from TXN: EM-Malda
Suppplier bus Event from TXN: CreateorActivateSupplierSite
***Object info from TRU in createOrActivateSupplierData:EM-Malda Active External Manufacturing
***Supplier present in Specright --Activate ***
***jsonString***{"specright__Active2__c":"Yes","Name":"EM-Malda","specright__Vendor_ID__c":"EM-Malda","SR_Kenvue_Fill_Site_Code__c":"EM-Malda"}
{"content":{"specright__Active2__c":"Yes","Name":"EM-Malda","specright__Vendor_ID__c":"EM-Malda","SR_Kenvue_Fill_Site_Code__c":"EM-Malda"}}
https://test.specright.com/v1/objects/Account/001WF00000Q2BI9YAN
200
{"success":true}
Response from get generic method: {"success":true}
Response code from get generic method: 200
***set transaction status as success***
Interface already present: TruSpecRightInterface
Set attribute Specright Obj ID = 001WF00000Q2BI9YAN
Spec txn Id in sendStatusEmail Method: 59712.34061.30498.27308
txnError------------: 
TRU bus Id in sendStatusEmail Method: 59712.34061.31704.59357
Spec Id in sendStatusEmail Method: 001WF00000Q2BI9YAN
getToMailIdfromTRU Method------: dkanung@its.jnj.com
EVENT-----CreateorActivateSupplierSite|Complete|SUCCESS

Step 3: Updating CronRun.GO with current timestamp...
Updated CronRun.GO successfully.

Script completed at: Tue Jun 10 02:52:14 EDT 2025
