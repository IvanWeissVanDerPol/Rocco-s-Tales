# List of directories to exclude
$excludedDirs = @(".env", "node_modules", ".venv")  # Add more directories as needed

# Function to recursively list files and directories
function List-Files {
    param (
        [string]$path
    )
    
    Get-ChildItem -Path $path -Recurse | ForEach-Object {
        $itemPath = $_.FullName

        # Check if the item is a directory and if it's in the excluded list
        $isExcluded = $false
        foreach ($excludedDir in $excludedDirs) {
            if ($itemPath -like "*\$excludedDir\*") {
                $isExcluded = $true
                break
            }
        }

        # Print the item if it's not in the excluded list
        if (-not $isExcluded) {
            Write-Output $itemPath
        }
    }
}

# Set the path you want to list files from
$rootPath = "C:\Users\WEISSIVA\Documents\Rocco-s-Tales"  # Change to your desired path

# Call the function
List-Files -path $rootPath

