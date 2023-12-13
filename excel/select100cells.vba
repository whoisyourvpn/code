Sub Select100Cells()
    Dim currentCell As Range
    Dim table As ListObject
    Dim startRow As Integer
    Dim totalRows As Integer

    Set currentCell = Selection

    ' Check if the current cell is within the table "ipdb"
    On Error Resume Next
    Set table = currentCell.ListObject
    On Error GoTo 0

    If Not table Is Nothing And table.Name = "ipdb" Then
        startRow = currentCell.Row
        totalRows = table.Range.Rows.Count

        ' Adjust the selection if it exceeds the table's total rows
        If startRow + 99 > table.Range.Rows(startRow).Row + totalRows - 1 Then
            startRow = totalRows - 99 + table.Range.Rows(1).Row
        End If

        ' Select 100 cells including the current cell
        Range(currentCell, currentCell.Offset(99, 0)).Select
    Else
        MsgBox "Please select a cell within the 'ipdb' table.", vbExclamation
    End If
End Sub
