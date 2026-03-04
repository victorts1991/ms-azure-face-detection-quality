# Definir variáveis
RG_STATE="rg-terraform-state"
LOCATION="eastus2"
# Gera um nome único para o storage (ex: stfacequalitytfabc123)
ST_NAME="stfacequalitytf$(openssl rand -hex 3)"
CONTAINER="tfstate"

# Criar os recursos na Azure
az group create --name $RG_STATE --location $LOCATION
az storage account create --resource-group $RG_STATE --name $ST_NAME --sku Standard_LRS --encryption-services blob
az storage container create --name $CONTAINER --account-name $ST_NAME

# Esse é o nome que você vai colocar no seu main.tf
echo "----------------------------------------------------"
echo "COPIE ESTE NOME PARA O TERRAFORM: $ST_NAME"
echo "----------------------------------------------------"