# API de Pedidos – Prueba Técnica DevSecOps

## Descripción General

Este proyecto implementa un flujo completo DevSecOps para desplegar y operar una API REST containerizada sobre AWS utilizando Infraestructura como Código (IaC), automatización CI/CD, validaciones de seguridad, monitoreo y estrategias de rollback.

La solución simula un servicio de gestión de pedidos de restaurante con dos operaciones principales:

- Crear pedidos
- Consultar pedidos

El enfoque principal de la implementación no está centrado en la complejidad de la aplicación, sino en el ciclo completo DevSecOps alrededor de la solución.

---

# Arquitectura de la Solución

```text
Developer
   ↓
GitHub Repository
   ↓
GitHub Actions CI/CD
   ↓
Docker Build + Security Scans
   ↓
Amazon ECR
   ↓
Amazon ECS Fargate
   ↓
Application Load Balancer
   ↓
Flask REST API


# Tecnologías utilizadas

| Componente                  | Tecnología                |
| --------------------------- | ------------------------- |
| Lenguaje                    | Python 3.11               |
| Framework                   | Flask                     |
| Testing                     | Pytest                    |
| Análisis de calidad         | Flake8                    |
| Containerización            | Docker                    |
| CI/CD                       | GitHub Actions            |
| Infraestructura como Código | Terraform                 |
| Cloud Provider              | AWS                       |
| Registro de imágenes        | Amazon ECR                |
| Ejecución de contenedores   | Amazon ECS Fargate        |
| Balanceador de carga        | Application Load Balancer |
| Logging                     | CloudWatch Logs           |
| Escaneo de seguridad        | Trivy                     |
| Backend Terraform           | S3 + DynamoDB             |


# Estructura del proyecto

app/
 ├── src/
 ├── tests/
 ├── Dockerfile
 └── requirements.txt

terraform/
 ├── main.tf
 ├── variables.tf
 ├── outputs.tf
 └── backend.tf

.github/workflows/
 ├── ci.yml
 └── deploy.yml


# Funcionalidades de la Aplicación

## Endpoints

### Health Check

GET /health

Respuesta:

{
  "status": "UP"
}


### Crear Pedido

POST /orders

Request:

{
  "customer": "cliente",
  "items": ["item1", "item2"]
}

Respuesta:

{
  "order_id": 1,
  "status": "created"
}

### Consultar Pedido

GET /orders/{id}

Respuesta:

{
  "customer": "cliente",
  "items": ["item1", "item2"]
}


# Infraestructura como Código (Terraform)

La infraestructura fue aprovisionada utilizando Terraform siguiendo principios de Infraestructura como Código (IaC).

## Recursos Aprovisionados

VPC
Public Subnets
Internet Gateway
Route Tables
Security Groups
ECS Cluster
ECS Service
ECS Task Definition
CloudWatch Log Group
ECR Repository
Application Load Balancer
Target Group
HTTP Listener
IAM Roles y Policies

## Backend Remoto Terraform

El manejo remoto del estado Terraform fue implementado utilizando:

- Amazon S3 para almacenamiento del estado
- DynamoDB para control de concurrencia y locking del state

Esto evita corrupción del state durante ejecuciones concurrentes.

# Pipeline de Integración Continua (CI)

El pipeline CI fue implementado utilizando GitHub Actions.

- Etapas del Pipeline CI
- Checkout del código fuente
-Configuración de Python
- Instalación de dependencias
- Análisis estático de código con Flake8
- Ejecución de pruebas unitarias con Pytest
- Construcción de imagen Docker
- Escaneo de vulnerabilidades con Trivy
- Controles de Seguridad Implementados

El pipeline incorpora controles DevSecOps para evitar despliegues inseguros.

# Escaneo de Vulnerabilidades

Trivy se utiliza para escanear imágenes Docker buscando:

- Vulnerabilidades críticas
- Vulnerabilidades de alta severidad
- Dependencias inseguras
- Security Gates

El pipeline bloquea despliegues si detecta vulnerabilidades críticas.

# Pipeline de Despliegue Continuo (CD)

El pipeline CD ejecuta:

- Autenticación contra AWS
- Autenticación contra Amazon ECR
- Construcción de imagen Docker
- Publicación de imagen en ECR
- Despliegue en ECS Fargate
- Validación de estabilidad del servicio
- Validación post-despliegue mediante Health Check
- Gestión Segura de Secretos

Las credenciales sensibles son gestionadas utilizando GitHub Actions Secrets.

No existen:

- Credenciales hardcodeadas
- Variables sensibles expuestas
- Secretos almacenados en el repositorio
- Estrategia de Versionamiento

Las imágenes Docker son versionadas utilizando el SHA del commit GitHub.

Ejemplo:

restaurant-api:<commit-sha>

Esto permite:

- Trazabilidad completa
- Despliegues controlados
- Recuperación de versiones
- Rollback seguro
- Monitoreo y Observabilidad

La solución implementa observabilidad básica utilizando servicios nativos de AWS.

- Componentes de Monitoreo
- CloudWatch Logs

Los logs de la aplicación son centralizados en CloudWatch Logs.

# Monitoreo ECS

ECS monitorea:

- Estado de tareas
- Fallos de despliegue
- Estado del servicio
- Health Checks Application Load Balancer

El ALB valida periódicamente:

/health

Los targets son marcados automáticamente como unhealthy si la aplicación deja de responder correctamente.

Validación Post-Deploy

El pipeline ejecuta validaciones automáticas posteriores al despliegue mediante consultas al endpoint /health.

# Estrategia de Rollback

La estrategia de rollback se basa en revisiones de ECS Task Definition.

Cada despliegue genera una nueva revisión inmutable.

En caso de falla:

- ECS permite regresar rápidamente a una revisión estable anterior
- Las revisiones anteriores permanecen disponibles
- El servicio puede restaurarse rápidamente

Beneficios:

- Recuperación rápida
- Continuidad operativa
- Reducción de downtime
- Trazabilidad de despliegues
- Estrategia de Branching

La solución soporta:

- master → despliegues productivos
- Pull Requests → validaciones automáticas
- Flujo General de Despliegue
- Primer Despliegue

Terraform aprovisiona:

- Networking
- ECS
- ECR
- ALB
- IAM
- Logging
- Despliegue de Aplicación

GitHub Actions:

- Construye imagen Docker
- Ejecuta pruebas
- Ejecuta escaneos de seguridad
- Publica imagen en ECR
- Despliega sobre ECS
- Buenas Prácticas Implementadas
- Infraestructura como Código
- Containerización inmutable
- Gestión segura de secretos
- Escaneo de vulnerabilidades
- IAM Least Privilege
- Backend remoto Terraform
- State locking
- Automatización CI/CD
- Health checks automáticos
- Despliegues trazables
- Observabilidad básica
- Evidencias Generadas

Durante la implementación se generaron evidencias de:

- Aprovisionamiento exitoso Terraform
- ECS Tasks en estado RUNNING
- Targets healthy en ALB
- Ejecuciones exitosas GitHub Actions
- Escaneos de seguridad Trivy
- Funcionamiento API REST
- Validación rollback
- Logs centralizados en CloudWatch
- Posibles Mejoras Futuras

La solución puede evolucionar incorporando:

- Blue/Green deployments
- Canary releases
- AWS WAF
- Monitoreo avanzado con Prometheus/Grafana
- Rollback automático avanzado
- Estrategia multiambiente
- HTTPS/TLS con ACM
- Kubernetes/EKS
- Dashboards avanzados observabilidad

## Conclusión

La solución implementa un flujo DevSecOps completo utilizando AWS, Terraform, Docker, GitHub Actions y ECS Fargate.

La plataforma incorpora automatización CI/CD, controles de seguridad, despliegues containerizados, monitoreo básico y estrategias de rollback siguiendo prácticas modernas DevSecOps.
```
