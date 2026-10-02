variable "aws_region" {
  description = "Región de AWS donde se desplegará la base de datos"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente de despliegue (dev, qa, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Nombre base para el proyecto y recursos"
  type        = string
  default     = "susalud-bi"
}

variable "db_instance_class" {
  description = "Tipo de instancia de base de datos RDS (t3.micro elegible para capa gratuita)"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Almacenamiento asignado en Gigabytes (GB)"
  type        = number
  default     = 20
}

variable "db_name" {
  description = "Nombre inicial de la base de datos PostgreSQL"
  type        = string
  default     = "susalud_db"
}

variable "db_username" {
  description = "Usuario administrador de la base de datos"
  type        = string
  default     = "dbadmin"
}

variable "db_password" {
  description = "Contraseña maestra para la base de datos (sensible)"
  type        = string
  sensitive   = true
  default     = "Susalud2026PassSecure!"
}

variable "allowed_cidr_blocks" {
  description = "Lista de bloques CIDR autorizados para conectarse a PostgreSQL (5432)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# -----------------------------------------------------------------------
# VARIABLES DE RED (para cuentas con SCP que bloquean DescribeVpcs)
# Obtener estos valores manualmente desde la consola de AWS:
# VPC ID  -> AWS Console > VPC > Sus VPCs > copiar el vpc-xxxxxxxx
# Subnets -> AWS Console > VPC > Subredes > copiar 2 IDs de subredes
# -----------------------------------------------------------------------
variable "vpc_id" {
  description = "ID de la VPC donde se desplegará la base de datos (ej: vpc-0abc1234567890abc)"
  type        = string
  default     = "vpc-00000000000000000"
}

variable "subnet_ids" {
  description = "Lista de al menos 2 IDs de subredes en distintas zonas de disponibilidad"
  type        = list(string)
  default     = ["subnet-00000000000000001", "subnet-00000000000000002"]
}
