try {
    # Ensure SQLite is available
    if (-not (Get-Command sqlite3 -ErrorAction SilentlyContinue)) {
        throw "SQLite3 is not installed or not in PATH"
    }

    # Set encoding for PowerShell output
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

    Get-ChildItem -Path "migrations" -Filter "*.sql" | 
        Sort-Object Name | 
        ForEach-Object { 
            Write-Output "Running migration: $($_.Name)"
            try {
                # Read content with UTF-8 encoding and pipe to SQLite with proper encoding settings
                $sqlContent = Get-Content $_.FullName -Encoding UTF8 -Raw
                $sqlContent | sqlite3 -bail -init "pragma encoding='UTF-8';" "database.sqlite"
                Write-Output "Successfully executed $($_.Name)"
            }
            catch {
                Write-Error "Failed to execute migration $($_.Name): $_"
                throw
            }
        }
    Write-Output "All migrations completed successfully"
}
catch {
    Write-Error "Migration process failed: $_"
    exit 1
}
