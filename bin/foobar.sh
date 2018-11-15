#!/usr/bin/env bash

set -e

# Download issueslist
./download-jira-issues.py -f http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-excel-current-fields/15151/SearchRequest-15151.xls?tempMax=1000 -o `date +%F`-issueslist.xls

# Download PCRlist
./download-jira-issues.py -f http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-excel-current-fields/15142/SearchRequest-15142.xls?tempMax=1000 -o `date +%F`-PCRlist.xls

# Download PCRlist with full content
./download-jira-issues.py -f http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-fullcontent/15142/SearchRequest-15142.html?tempMax=1000 -o `date +%F`-PCRlist\(detailed\).html

wkhtmltopdf `date +%F`-PCRlist\(detailed\).html `date +%F`-PCRlist\(detailed\).pdf

# Download issueslist with full content
./download-jira-issues.py -f http://jira.eng.sgp-tsa.sg.thales:8080/sr/jira.issueviews:searchrequest-fullcontent/15151/SearchRequest-15151.html?tempMax=1000 -o "`date +%F`-marc - all issues details (Thales Solutions Asia).html"

wkhtmltopdf "`date +%F`-marc - all issues details (Thales Solutions Asia).html" \
            "`date +%F`-marc - all issues details (Thales Solutions Asia).pdf"

RTUREP_DOC_SVN="${HOME}/Documents/nelrtu-doc/2 Project Execution Data/2.2 Work Products/04_Software/SprintReportsStatistics"

# Convert 
libreoffice --calc --convert-to xls:"MS Excel 97" `date +%F-issueslist.xls`
libreoffice --calc --convert-to xls:"MS Excel 97" `date +%F-PCRlist.xls`

# Copy these files and commit to the SVN
cp -f `date +%F-issueslist.xls` "${RTUREP_DOC_SVN}/issueslist.xls"
cp -f `date +%F-PCRlist.xls` "${RTUREP_DOC_SVN}/PCRlist.xls"

cp -f "`date +%F`-PCRlist(detailed).pdf" "${RTUREP_DOC_SVN}/PCRlist(detailed).pdf"
cp -f "`date +%F`-marc - all issues details (Thales Solutions Asia).pdf" "${RTUREP_DOC_SVN}/marc - all issues details (Thales Solutions Asia).pdf"

cd "${RTUREP_DOC_SVN}"
svn up
#svn ci -m "TY (bot): Update the documents for technical meeting"
