function WriteLog(message)
{
    var fso = new ActiveXObject("Scripting.FileSystemObject");
    var fh = fso.OpenTextFile("Path\file.txt", 8, true);
    fh.WriteLine(message);
    fh.Close();
}