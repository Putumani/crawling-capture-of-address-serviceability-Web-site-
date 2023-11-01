# crawling-capture-of-address-serviceability-Web-site-
RPA/crawling & capture of address-serviceability Web site

Overview:
Inject addresses from input CSV file to https://t-mobilefiber.com/availability/, select first result from autocomplete, and capture result on subsequent Web page
Produce single report CSV file to list result of each address in separate row, appending a new row for each address loop
Produce an address-specific text dump file containing all text appearing on subsequent Web page for each address loop (for archival)
Loop through input CSV file until all addresses return a result in the report CSV file, then end script
Input CSV format: address (enclosed in quotation marks),location_id
Report CSV format: address (enclosed in quotation marks),location_id,result_code

Suggested libraries/resources:
Chromedriver and Chrome
Linux dependencies: 'numpy', 'requests', 'pyperclip', 'selenium', 'termcolor'

Codebase:
Can provide functioning Python scripts of similar address-serviceability Web sites as examples

