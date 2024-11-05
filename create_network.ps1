# PowerShell script to create a Docker network called external_network and start Docker Compose services

$networkName = "external_network"

# Check if the network already exists
$networkExists = docker network ls | Select-String -Pattern $networkName
if ($networkExists) {
    Write-Host "Network $networkName already exists."
} else {
    docker network create $networkName
    Write-Host "Network $networkName created successfully."
}