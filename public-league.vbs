Set fso = CreateObject("Scripting.FileSystemObject")
Set shell = CreateObject("WScript.Shell")
openBrowser = True
For Each arg In WScript.Arguments
  If LCase(arg) = "--no-browser" Then openBrowser = False
Next
root = fso.GetParentFolderName(WScript.ScriptFullName)
pythonw = root & "\.venv\Scripts\pythonw.exe"
launcher = root & "\tools\public_league.py"
shell.CurrentDirectory = root
shell.Run """" & pythonw & """ """ & launcher & """ serve --port 8791 --exit-with-browser", 0, False
If openBrowser Then
  WScript.Sleep 1200
  shell.Run "http://127.0.0.1:8791", 1, False
End If
