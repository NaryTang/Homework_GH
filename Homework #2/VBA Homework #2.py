Sub Multiple_year_stock_data()

# 'Defining variables for wooksheet for loop
Dim ws_num As Integer
Dim starting_ws As Worksheet
Set starting_ws = ActiveSheet
ws_num = ThisWorkbook.Worksheets.Count

# 'creating for loop to loop through worksheets
For i = 1 To ws_num
ThisWorkbook.Worksheets(i).Activate
  
      # 'Starting Ticker activities/loops

      # 'Set initial variable for holding the ticker
      Dim Ticker As String
      Dim Ticker_Vol_Total As Double
      Ticker_Vol_Total = 0

      # 'Keep track of the location for each Ticker in the summary table
      Dim Summary_Table_Row As Integer
      Summary_Table_Row = 2
      
      # 'Define variables and set starting point for calculation of Yearly Change
      Dim Ticker_year_open As Double
      Ticker_year_open = Cells(2, 3).Value
      Dim Ticker_year_close As Double
      Dim Percent_Change As Double

      # 'Define variable for counting all exisiting rows for the for loop
      numrows = Range("A1", Range("A1").End(xlDown)).Rows.Count

      # 'Loop through all Tickers
      For j = 2 To numrows

          # 'Check to see if we are still within the same Ticker, if we are not...
          If Cells(j + 1, 1).Value <> Cells(j, 1).Value Then
            
              # 'Capture Ticker_yearly_change
              Ticker_year_close = Cells(j, 6).Value
              Ticker_yearly_change = Ticker_year_close - Ticker_year_open
              # 'Print Ticker_yearly_change
              Range("K" & Summary_Table_Row).Value = Ticker_yearly_change

              # 'Capture Percent_Change
              If Ticker_year_open <> 0 Then
                  Percent_Change = Ticker_yearly_change / Ticker_year_open
                  # 'format Percent_Change to %
                  Range("L" & Summary_Table_Row).NumberFormat = "0.00%"
                  Range("L" & Summary_Table_Row).Value = Percent_Change
              
              # 'address dividing by 0 issue (PLNT yearly open value is 0)
              Else
                  Range("L" & Summary_Table_Row).Value = 0
              End If

              # 'assign colors to the Ticker yearly change cells
              If Ticker_yearly_change >= 0 Then
                  Range("K" & Summary_Table_Row).Interior.ColorIndex = 4
              Else
                  Range("K" & Summary_Table_Row).Interior.ColorIndex = 3
              End If

              # 'Set the Ticker
              Ticker = Cells(j, 1).Value
              # 'Add to the Ticker Vol Total
              Ticker_Vol_Total = Ticker_Vol_Total + Cells(j, 7).Value
              # 'Print The Ticker name in the summary table
              Range("I" & Summary_Table_Row).Value = Ticker
              # 'Print the Ticker Vol Total to the summary table
              Range("J" & Summary_Table_Row).Value = Ticker_Vol_Total
              # 'add one to the sumamary table row
              Summary_Table_Row = Summary_Table_Row + 1
              

              # 'reset Ticker_Vol_Total
              Ticker_Vol_Total = 0
              # 'reset Ticker year open
              Ticker_year_open = Cells(j + 1, 3).Value

          # 'If the cell immediately following a row is the same ticker...
          Else
              # 'add to the Ticker Total
              Ticker_Vol_Total = Ticker_Vol_Total + Cells(j, 7).Value

          End If

      Next j

      # 'creating setup for Summary Table loop

      # 'Defining variables
      Dim Greatest_percentage_increase As Double
      Dim Greatest_percentage_decrease As Double
      Dim Greatest_Total_Vol As Double

      Dim Greatest_percentage_increase_ticker As String
      Dim Greatest_percentage_decrease_ticker As String
      Dim Greatest_Total_Vol_ticker As String

      Greatest_percentage_increase = Cells(2, 12).Value
      Greatest_percentage_decrease = Cells(2, 12).Value
      Greatest_Total_Vol = Cells(2, 10).Value

    # 'Define variable for counting all exisiting rows for the for loop
    numrows = Range("I1", Range("I1").End(xlDown)).Rows.Count
    #loop through summary table
    For s = 2 To numrows
        If Cells(s + 1, 12).Value > Greatest_percentage_increase Then
            Greatest_percentage_increase = Cells(s + 1, 12).Value
            Cells(2, 17).Value = Greatest_percentage_increase
            Cells(2, 16).Value = Cells(s + 1, 9).Value
            Cells(2, 17).NumberFormat = "0.00%"
        End If
        
        If Cells(s + 1, 12).Value < Greatest_percentage_decrease Then
            Greatest_percentage_decrease = Cells(s + 1, 12).Value
            Cells(3, 17).Value = Greatest_percentage_decrease
            Cells(3, 16).Value = Cells(s + 1, 9).Value
            Cells(3, 17).NumberFormat = "0.00%"
        End If
    
        If Cells(s + 1, 10).Value > Greatest_Total_Vol Then
            Greatest_Total_Vol = Cells(s + 1, 10).Value
            Cells(4, 17).Value = Greatest_Total_Vol
            Cells(4, 16).Value = Cells(s + 1, 9).Value
        End If
    
    Next s

ThisWorkbook.Worksheets(i).Cells(1, 1) = 1

Next

End Sub