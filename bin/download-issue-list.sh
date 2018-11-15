#!/usr/bin/env bash

set -e

ISSUES_LIST="`date +%F-issueslist`"
PCR_LIST="`date +%F-PCRlist`"
DETAILED_PCR_LIST="`date +%F`-PCRlist(detailed)"
ALL_DETAILED_ISSUES_LIST="`date +%F`-marc - all issues details (Thales Solutions Asia)"

# Download results of JIRA issues
# Uses 'marc - ALL OPEN RTU issues, and CLOSED/RESOLVED last 30 days' filter
OPEN_AND_RECENTLY_CLOSED_URL="http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-excel-current-fields/15151/SearchRequest-15151.xls?tempMax=1000"

# Save the results to YYYY-mm-dd-issueslist.html
./download-jira-issues.py -f ${OPEN_AND_RECENTLY_CLOSED_URL} -o ${ISSUES_LIST}.html


# Download results of JIRA issues
# Uses 'marc - PCR Status (customer only)' filter
CUSTOMER_ONLY_ISSUES_URL="http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-excel-current-fields/15142/SearchRequest-15142.xls?tempMax=1000"

# Save the results to YYYY-mm-dd-PCRlist.html
./download-jira-issues.py -f ${CUSTOMER_ONLY_ISSUES_URL} -o ${PCR_LIST}.html


# Download results of JIRA issues
# Use 'marc - PCR Status (customer only)' filter
CUSTOMER_ONLY_ISSUES_FULL_URL="http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-fullcontent/15142/SearchRequest-15142.html?tempMax=1000"

# Save the results to YYYY-mm-dd-PCRlist(detailed).html
./download-jira-issues.py -f ${CUSTOMER_ONLY_ISSUES_FULL_URL} -o ${DETAILED_PCR_LIST}.html
# Convert the output into a PDF file
wkhtmltopdf ${DETAILED_PCR_LIST}.html ${DETAILED_PCR_LIST}.pdf


# Download results of JIRA issues
# Use 'marc - PCR Status (customer only)' filter
ALL_ISSUES_INTERNAL_ONLY_URL="http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-fullcontent/15151/SearchRequest-15151.html?tempMax=1000"

# Save the results to YYYY-mm-dd-marc - all issues details (Thales Solutions Asia).html
./download-jira-issues.py -f ${ALL_ISSUES_INTERNAL_ONLY_URL} -o "${ALL_DETAILED_ISSUES_LIST}.html"

# Convert the output into a PDF file
wkhtmltopdf "${ALL_DETAILED_ISSUES_LIST}.html" "${ALL_DETAILED_ISSUES_LIST}.pdf"

libreoffice --calc --headless --convert-to xls:"MS Excel 97" ${ISSUES_LIST}.html
libreoffice --calc --headless --convert-to xls:"MS Excel 97" ${PCR_LIST}.html

RTUREP_DOC_SVN="${HOME}/Documents/rturep/2 Project Execution Data/2.2 Work Products/04_Software/SprintReportsStatistics"

svn up "${RTUREP_DOC_SVN}"

# Copy the output to a local SVN repo
cp -f ${ISSUES_LIST}.xls "${RTUREP_DOC_SVN}/issueslist.xls"
cp -f ${ISSUES_LIST}.html "${RTUREP_DOC_SVN}/issueslist.html"
cp -f ${PCR_LIST}.xls "${RTUREP_DOC_SVN}/PCRlist.xls"
cp -f ${PCR_LIST}.html "${RTUREP_DOC_SVN}/PCRlist.html"

cp -f ${DETAILED_PCR_LIST}.pdf "${RTUREP_DOC_SVN}/PCRlist(detailed).pdf"
cp -f "${ALL_DETAILED_ISSUES_LIST}.pdf" "${RTUREP_DOC_SVN}/marc - all issues details (Thales Solutions Asia).pdf"

svn add "${RTUREP_DOC_SVN}/issueslist.xls"
svn add "${RTUREP_DOC_SVN}/issueslist.html"
svn add "${RTUREP_DOC_SVN}/PCRlist.xls"
svn add "${RTUREP_DOC_SVN}/PCRlist.html"

svn ci -m "TY (bot): Auto-update sprint statistics" "${RTUREP_DOC_SVN}"
