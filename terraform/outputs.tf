output "FACE_API_ENDPOINT" {
  value = module.services.face_endpoint
}

output "FACE_API_KEY" {
  value     = module.services.face_key
  sensitive = true
}

output "STORAGE_ACCOUNT_NAME" {
  value = module.services.storage_account_name
}

output "ACR_LOGIN_SERVER" {
  value = module.cluster.acr_login_server
}