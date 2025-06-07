Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python """ & WScript.ScriptFullName & "\..\ImageCollectionViewer.py""", 0
Set WshShell = Nothing