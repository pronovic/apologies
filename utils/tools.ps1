# Run script wrapper for use in PyCharm external tools on Windows
#
# The run script works fine from a Git Bash shell, but isn't easy to invoke
# from IntelliJ or PyCharm as an external tool.  This script wraps it so it
# can be invoked more easily.
#
# Run like: powershell.exe -executionpolicy bypass -File tools.ps1 format

param([string]$command)
& 'C:\Program Files\Git\bin\bash.exe' "./run" $command | Out-String

