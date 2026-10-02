# ==============================================================================
# PROYECTO: Inteligencia de Negocios - Examen Unidad I (Pacompia)
# INFRAESTRUCTURA COMO CÓDIGO (IaC) - AWS RDS POSTGRESQL CON TERRAFORM
# NOTA: Se usa VPC y subnets con IDs fijos para compatibilidad con cuentas
#       universitarias AWS Academy que restringen DescribeVpcs en EC2.
# ==============================================================================

# Variables locales con IDs de infraestructura de red
# (Configura los valores reales en terraform.tfvars o en GitHub Secrets)
locals {
  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids
}

# Security Group para habilitar acceso a PostgreSQL (puerto 5432)
resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-${var.environment}-rds-sg"
  description = "Permite trafico entrante a PostgreSQL para Power BI y Liquibase"
  vpc_id      = local.vpc_id

  ingress {
    description = "Acceso a puerto PostgreSQL desde IPs autorizadas"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  egress {
    description = "Trafico de salida libre"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# Grupo de subnets para la base de datos RDS (requiere al menos 2 AZs)
resource "aws_db_subnet_group" "db_subnet_group" {
  name        = "${var.project_name}-${var.environment}-subnet-group"
  description = "Grupo de subnets para PostgreSQL RDS de SUSALUD BI"
  subnet_ids  = local.subnet_ids

  tags = {
    Name = "${var.project_name}-subnet-group"
  }
}

# Parámetros del motor de base de datos
resource "aws_db_parameter_group" "postgres_params" {
  name   = "${var.project_name}-${var.environment}-pg15-params"
  family = "postgres15"

  parameter {
    name  = "client_encoding"
    value = "UTF8"
  }

  tags = {
    Name = "${var.project_name}-pg15-params"
  }
}

# Instancia de base de datos RDS PostgreSQL
resource "aws_db_instance" "postgres" {
  identifier        = "${var.project_name}-${var.environment}-db"
  engine            = "postgres"
  engine_version    = "15.7"
  instance_class    = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  storage_type      = "gp3"

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  parameter_group_name   = aws_db_parameter_group.postgres_params.name

  publicly_accessible = true
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name = "${var.project_name}-rds-instance"
  }
}
