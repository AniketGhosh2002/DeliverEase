CurrentYearItems = 

VAR CurrentYear = MAX('Date Table'[Year])

RETURN

CALCULATE([NoOfSelectedItems], 'Date Table'[Year] = CurrentYear)
