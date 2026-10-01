output "rds_endpoint" {
  description = "Dirección de conexión (host) de la base de datos RDS"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "Puerto de escucha de PostgreSQL"
  value       = aws_db_instance.postgres.port
}

output "rds_db_name" {
  description = "Nombre de la base de datos creada"
  value       = aws_db_instance.postgres.db_name
}

output "rds_username" {
  description = "Usuario administrador de PostgreSQL"
  value       = aws_db_instance.postgres.username
}

output "connection_jdbc_url" {
  description = "Cadena de conexión JDBC recomendada para Liquibase"
  value       = "jdbc:postgresql://${aws_db_instance.postgres.endpoint}/${aws_db_instance.postgres.db_name}"
}
