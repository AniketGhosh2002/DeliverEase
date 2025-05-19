#!/bin/bash
###############################################################################
#     Script to Run  Spec Report Generator                                    #
#     Data:   10 Jan 2019                                                     #
#     Author : TCS                                                            #   
#     Notes:                                                                  #
###############################################################################


###############################################################################
#    Step 1 : Run the JPO and then generate the report
###############################################################################

VDATE=`date +%Y-\%m-\%d_\%H.\%M`
cronStartDate=`date`
FileDynamics=`date +%m\%d\%Y`

# get the directory the script file resides
BASEDIR=$(dirname "$0")

# write the script start date time stamp 
echo "------------------------------------ CRON DETAILS -------------------------------------"
echo "Run Start At   : $cronStartDate "
#echo "Base Folder At : $BASEDIR "

#------------------------------------------------------------------------------
#    Step 1A : Read the config file entries for MQL connection
#------------------------------------------------------------------------------

export Switch=`grep -w SWITCH $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`

if [ $Switch == 'On' ]; then
	export BootStrap=`grep -w BOOTSTRAP $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export mqlUser=`grep -w MQLUSER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export mqlPwd=`$BootStrap -t -c "execute program PwdMgr -method getPwd '$mqlUser';"`
	export FilePath=`grep -w FILEPATH $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	startDate=`cat $BASEDIR/../Config/PrismaRun.GO`
	export endDate="NODATA"
	export RELFILEPATH=`grep -w RELFILEPATH $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export RELFILENAME=`grep -w RELFILENAME $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export OBSFILENAME=`grep -w OBSFILENAME $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export TEMPLATEDATAEXTRACTFILE=`grep -w TEMPLATEDATAEXTRACTFILE $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export SPECTEMPLATEDATAFILE=`grep -w SPECTEMPLATEDATAFILE $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export SPECMASTERDATAFILE=`grep -w SPECMASTERDATAFILE $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export BULKEXTRACTPATH=`grep -w BULKEXTRACTPATH $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export MEPFILENAME=`grep -w MEPFILENAME $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export MEPRELFILENAME=`grep -w MEPRELFILENAME $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export adminNOXML=`grep -w ADMIN_RUN_NOXML $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export mqlPwd=`$BootStrap -t -c "execute program PwdMgr -method getPwd '$mqlUser';"`
	export TemplateSectionExclusionList=`grep -w PRISMASTRINGRESOURCE.FILE.SPECTEMPLATEDATA.TABLESECTIONEXCLUSIONLIST $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export TemplateExclusionList=`grep -w PRISMASTRINGRESOURCE.TEMPLATE.EXCLUSIONLIST $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export ParentType=`grep -w PRISMASTRINGRESOURCE.DATAELIGIBLE.PARENTTYPE $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export EBOMHeader=`grep -w PRISMASTRINGRESOURCE.EBOMRELDATA.HEADER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export OBSHeader=`grep -w PRISMASTRINGRESOURCE.OBSOLETEDATA.HEADER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export MEPHeader=`grep -w PRISMASTRINGRESOURCE.MEPDATA.HEADER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export MEPDistHeader=`grep -w PRISMASTRINGRESOURCE.MEPDISTRIBUTORDATA.HEADER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export TVVLink=`grep -w PRISMASTRINGRESOURCE.TVVLINK $BASEDIR/../Config/PrismaStringResource.config | awk -F"=" '{print $2"="$3"="}'`
	export TemplateDataHeader=`grep -w PRISMASTRINGRESOURCE.FILE.SPECTEMPLATEDATA.HEADER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export MasterDataHeader=`grep -w PRISMASTRINGRESOURCE.FILE.SPECMASTERDATA.HEADER $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export PRISMAELIGIBLETYPE=`grep -w PRISMA.ELIGIBLE.TYPE $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export ScriptFailMsgSubject=`grep -w SCRIPTFAIL_SUB $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export ScriptFailMsgBody=`grep -w SCRIPTFAIL_BODY $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export FilesMissingMsgSubject=`grep -w FILEMISSING_SUB $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export FilesMissingMsgBody=`grep -w FILEMISSING_BODY $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	export MsgList=`grep -w TEMP_EMAIL_TO_LIST $BASEDIR/../Config/PrismaStringResource.config | cut -d "=" -f2`
	#------------------------------------------------------------------------------
	#    Step 1 : Call the JPO file
	#------------------------------------------------------------------------------

	echo "Starting GenerateTruPrismaSpecReport.sh at $cronStartDate"
	echo "=======================================Total Objects Extracted=======================================" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
	echo "Starting GenerateTruPrismaSpecReport.sh at $cronStartDate" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
	
	if [[ -z "$startDate" ]]; then
		echo "Either PrismaRun.GO is not present or blank.Hence,files are not extracted.\nPlease update PrismaRun.GO with extract start date in mm/dd/yyyy format." >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
		echo -e "Either PrismaRun.GO is not present or blank.Hence,files are not extracted.\nPlease update PrismaRun.GO with extract start date in mm/dd/yyyy format." | mail -s "PRISMA EXTRACTION FAILURE" "$MsgList"
	else
	export RUNTYPE="DELTA"
		if [ "$adminNOXML" == "YES" ]; then
		echo "0. ExtractTemplateReport.sh is not running" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
		else
		sh ExtractTemplateReport.sh "Config/PrismaStringResource.config"
		returnCode=$?
		echo "0. ExtractTemplateReport.sh is running" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
		echo 'Error Code from the script run is '$returnCode >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
		fi 
		
		if [ $adminNOXML == 'YES' ]
		then
				echo "1. Program jnjTruToPrismaReportGenerator is invoked" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				echo "$FilePath"
				mv $BASEDIR/../Output/*.txt $BASEDIR/../Archive/
				$BootStrap -c "verb on; set context user  $mqlUser pass $mqlPwd ; exec prog jnjTruToPrismaReportGenerator -method generateTrutoPrismaReport \"$FilePath\"  $startDate $endDate \"$RUNTYPE\" \"$RELFILEPATH\" \"$RELFILENAME\" \"$OBSFILENAME\" \"$SPECTEMPLATEDATAFILE\" \"$SPECMASTERDATAFILE\" \"$TEMPLATEDATAEXTRACTFILE\" \"$BULKEXTRACTPATH\" \"$MEPFILENAME\" \"$MEPRELFILENAME\" \"$TemplateSectionExclusionList\" \"$TemplateExclusionList\" \"$ParentType\" \"$EBOMHeader\" \"$OBSHeader\" \"$MEPHeader\" \"$MEPDistHeader\" \"$TVVLink\" \"$TemplateDataHeader\" \"$MasterDataHeader\" \"$PRISMAELIGIBLETYPE\"; quit;"
				returnCode=$?
				echo '\n\n\n\t\t\tError Code from the script run is '$returnCode
				echo 'Error Code from the script run is '$returnCode>>$BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				
				echo "=======================================Total Objects Extracted=======================================" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				echo "=====================================================================================================" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				cd $BASEDIR/../Output/
				for filename in *.txt; do
				echo "$filename Count is :" $(( $(wc -l < $filename) -1 ))>> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				done
				cd $BASEDIR
				if [ $returnCode == 0 ]; then
					cd $BASEDIR/../Scripts
					sh ./uploadmbox.sh "Config/PrismaStringResource.config"
					echo "2. uploadmbox.sh is running." >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				else
					echo "2. Script Run Failed. Mail sent." >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
					echo -e "$ScriptFailMsgBody" | mail -s "$ScriptFailMsgSubject" "$MsgList"

				fi
		else
			if [ $returnCode == 0 ];then
			#######
						echo "1. Program jnjTruToPrismaReportGenerator is invoked" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				echo "$FilePath"
				mv $BASEDIR/../Output/*.txt $BASEDIR/../Archive/
				$BootStrap -c "verb on; set context user  $mqlUser pass $mqlPwd ; exec prog jnjTruToPrismaReportGenerator -method generateTrutoPrismaReport \"$FilePath\"  $startDate $endDate \"$RUNTYPE\" \"$RELFILEPATH\" \"$RELFILENAME\" \"$OBSFILENAME\" \"$SPECTEMPLATEDATAFILE\" \"$SPECMASTERDATAFILE\" \"$TEMPLATEDATAEXTRACTFILE\" \"$BULKEXTRACTPATH\" \"$MEPFILENAME\" \"$MEPRELFILENAME\" \"$TemplateSectionExclusionList\" \"$TemplateExclusionList\" \"$ParentType\" \"$EBOMHeader\" \"$OBSHeader\" \"$MEPHeader\" \"$MEPDistHeader\" \"$TVVLink\" \"$TemplateDataHeader\" \"$MasterDataHeader\" \"$PRISMAELIGIBLETYPE\"; quit;"
				returnCode=$?
				echo '\n\n\n\t\t\tError Code from the script run is '$returnCode
				echo 'Error Code from the script run is '$returnCode>>$BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				
				echo "=======================================Total Objects Extracted=======================================" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				echo "=====================================================================================================" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				cd $BASEDIR/../Output/
				fileCount=`ls -l *.txt|wc -l` 
				for filename in *.txt; do
				echo "$filename Count is :" $(( $(wc -l < $filename) -1 ))>> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
				done
				cd $BASEDIR
				if [ $returnCode == 0 ]; then
					cd $BASEDIR/../Scripts
					if [ $fileCount == 6 ]; then
						sh ./uploadmbox.sh "Config/PrismaStringResource.config"
						echo "2. uploadmbox.sh is running." >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
					else
						echo "2. All type of files not generated. Hence, Files not uploaded to MBOX. Please check Output Folder. Mail Sent" >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
						echo -e "$FilesMissingMsgBody" | mail -s "$FilesMissingMsgSubject" "$MsgList"
					fi
				else
					echo "2. Script Run Failed. Mail sent." >> $BASEDIR/../Log/TrutoPrismaExtraction$FileDynamics.log
					echo -e "$ScriptFailMsgBody" | mail -s "$ScriptFailMsgSubject" "$MsgList"
				fi
				
			#######
			fi
		fi
		fi
fi
#date +%m"/"%d"/"%Y >  $BASEDIR/../Config/PrismaRun.GO
