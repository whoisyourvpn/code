Sub Select100CellsInSheet()
    Dim currentCell As Range
    Dim ws As Worksheet
    Dim startRow As Long
    Dim totalRows As Long

    Set ws = ThisWorkbook.Sheets("ipdb")

    ' Check if the selected cell is in the specified sheet
    If Not Intersect(ActiveCell, ws.UsedRange) Is Nothing Then
        Set currentCell = ActiveCell

        ' Calculate the start and end rows for selection
        startRow = currentCell.Row
        totalRows = ws.Cells(ws.Rows.Count, currentCell.Column).End(xlUp).Row

        ' Adjust the selection if it exceeds the total rows
        If startRow + 99 > totalRows Then
            startRow = totalRows - 99
            If startRow < 1 Then startRow = 1 ' Ensure start row is not less than 1
        End If

        ' Select 100 cells including the current cell
        ws.Range(ws.Cells(startRow, currentCell.Column), ws.Cells(startRow + 99, currentCell.Column)).Select
    Else
        MsgBox "The active cell is not in the 'ipdb' sheet.", vbExclamation
    End If
End Sub
