# Commands for use as IntelliJ or PyCharm external tools on Windows
#
# The run script works fine from a Git Bash shell, but isn't easy to invoke
# from IntelliJ or PyCharm as an external tool.  This script duplicates the
# behavior from the run script for the things that I want to be able to invoke.
# It intentionally does *not* duplicate all of the behavior in the run script.
# For more information, see the notes in DEVELOPER.md.
#
# Run like: powershell.exe -executionpolicy bypass -File tools.ps1 format

param([string]$command)
Switch ($command)
{
    format {
      Write-Output "Running black formatter..." 
      poetry run black .

      Write-Output "`nRunning isort formatter..." 
      $files = cmd /c dir /b /a-d /s src\apologies tests | findstr \.py$
      poetry run isort $files
      Write-Output "done"
    }

    mypy {
      Write-Output "Running mypy checks..." 
      poetry run mypy --config-file=.mypyrc src/apologies tests
    }

    pylint {
      Write-Output "Running pylint checks..." 
      poetry run pylint --rcfile=.pylintrc src/apologies tests
    }
}

