# 🚀 VM Provisioning Multi-Cloud API

Una API RESTful unificada para aprovisionar y gestionar máquinas virtuales en múltiples proveedores cloud usando el patrón **Factory Method**.

## 📋 Características

- ✅ **Multi-Cloud**: Soporte para AWS, Azure, GCP y On-Premise
- ✅ **Factory Method**: Arquitectura extensible y mantenible
- ✅ **RESTful API**: Endpoints organizados y documentados
- ✅ **Gestión Completa**: Crear, consultar, filtrar y actualizar VMs
- ✅ **Seguridad**: Logs sanitizados y validación de parámetros
- ✅ **Estadísticas**: Métricas y resúmenes por proveedor

## 🏗️ Arquitectura

```
Cliente → FastAPI Controller → Service Layer → Factory Pattern → Cloud Providers
                                      ↓
                              Repository Pattern → JSON Storage
```

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Acceder a la documentación
- **Swagger UI**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción | Tags |
|--------|----------|-------------|------|
| `GET` | `/` | Información general | Información |
| `GET` | `/health` | Health check | Health Check |
| `GET` | `/api/v1/providers` | Proveedores disponibles | Proveedores |
| `POST` | `/api/v1/vm/provision` | Crear nueva VM | Aprovisionamiento |
| `GET` | `/api/v1/vms` | Todas las VMs | Consultas de VMs |
| `GET` | `/api/v1/vms/provider/{type}` | VMs por proveedor | Consultas de VMs |
| `GET` | `/api/v1/vms/status/{status}` | VMs por estado | Consultas de VMs |
| `GET` | `/api/v1/vms/{vm_id}` | VM específica | Consultas de VMs |
| `GET` | `/api/v1/vms-summary` | Resumen estadístico | Estadísticas |
| `PUT` | `/api/v1/vms/{vm_id}/status` | Actualizar estado | Gestión de Estados |

## 🎯 Ejemplos de Uso con JSON

### 1. 🔥 Crear VM en AWS EC2

```bash
curl -X POST "http://localhost:8000/api/v1/vm/provision" \
-H "Content-Type: application/json" \
-d '{
  "provider_type": "aws",
  "parameters": {
    "instance_type": "t2.micro",
    "region": "us-east-1",
    "vpc": "vpc-1234567890abcdef0",
    "ami": "ami-0abcdef1234567890",
    "key_name": "my-keypair",
    "security_groups": ["web-sg", "ssh-sg"],
    "storage_gb": 20,
    "monitoring_enabled": true,
    "tags": {
      "Environment": "development",
      "Project": "web-app",
      "Owner": "dev-team"
    }
  }
}'
```

### 2. 🔥 Crear VM en Azure Virtual Machines

```bash
curl -X POST "http://localhost:8000/api/v1/vm/provision" \
-H "Content-Type: application/json" \
-d '{
  "provider_type": "azure",
  "parameters": {
    "vm_size": "Standard_B1s",
    "resource_group": "my-resource-group",
    "location": "eastus",
    "image_publisher": "Canonical",
    "image_offer": "UbuntuServer",
    "image_sku": "18.04-LTS",
    "admin_username": "azureuser",
    "storage_account_type": "Standard_LRS",
    "virtual_network": "vnet-main",
    "subnet": "subnet-default",
    "availability_set": "avail-set-1",
    "custom_data": "IyEvYmluL2Jhc2gKZWNobyAiSGVsbG8gQXp1cmUhIiA+IC9ob21lL2F6dXJldXNlci93ZWxjb21lLnR4dA=="
  }
}'
```

### 3. 🔥 Crear VM en Google Cloud Platform

```bash
curl -X POST "http://localhost:8000/api/v1/vm/provision" \
-H "Content-Type: application/json" \
-d '{
  "provider_type": "gcp",
  "parameters": {
    "machine_type": "n1-standard-1",
    "zone": "us-central1-a",
    "project_id": "my-gcp-project-123456",
    "image_family": "ubuntu-2004-lts",
    "image_project": "ubuntu-os-cloud",
    "boot_disk_size": 50,
    "boot_disk_type": "pd-standard",
    "network": "default",
    "subnetwork": "default",
    "external_ip": true,
    "preemptible": false,
    "service_account": "compute-engine@my-project.iam.gserviceaccount.com",
    "metadata": {
      "startup-script": "#!/bin/bash\necho 'Hello GCP!' > /tmp/hello.txt",
      "enable-oslogin": "TRUE"
    },
    "labels": {
      "environment": "production",
      "department": "engineering"
    }
  }
}'
```

### 4. 🔥 Crear VM en Infraestructura On-Premise

```bash
curl -X POST "http://localhost:8000/api/v1/vm/provision" \
-H "Content-Type: application/json" \
-d '{
  "provider_type": "on_premise",
  "parameters": {
    "cpu_cores": 4,
    "ram_gb": 8,
    "storage_gb": 100,
    "host_server": "hypervisor-01.company.local",
    "datastore": "datastore1",
    "network": "VM Network",
    "os_template": "ubuntu-20.04-template",
    "vm_folder": "Development",
    "resource_pool": "dev-pool",
    "thin_provisioning": true,
    "cpu_hot_add": true,
    "memory_hot_add": false,
    "nested_virtualization": true,
    "firmware": "bios",
    "disk_controller": "SCSI",
    "cdrom_enabled": true,
    "usb_controller": true
  }
}'
```

### 5. 🔥 Crear VM con Configuración Avanzada (AWS)

```bash
curl -X POST "http://localhost:8000/api/v1/vm/provision" \
-H "Content-Type: application/json" \
-d '{
  "provider_type": "aws",
  "parameters": {
    "instance_type": "m5.large",
    "region": "us-west-2",
    "vpc": "vpc-0a1b2c3d4e5f67890",
    "subnet_id": "subnet-1234567890abcdef0",
    "ami": "ami-0c02fb55956c7d316",
    "key_name": "production-key",
    "security_group_ids": ["sg-0123456789abcdef0", "sg-0fedcba9876543210"],
    "iam_instance_profile": "EC2-S3-Access",
    "user_data": "IyEvYmluL2Jhc2gKc3VkbyBhcHQtZ2V0IHVwZGF0ZQpzdWRvIGFwdC1nZXQgLXkgaW5zdGFsbCBhcGFjaGUyCmVjaG8gJ0hlbGxvIGZyb20gQ1VSTCEnID4gL3Zhci93d3cvaHRtbC9pbmRleC5odG1sCnN5c3RlbWN0bCBlbmFibGUgYXBhY2hlMgpzeXN0ZW1jdGwic3RhcnQgYXBhY2hlMg==",
    "ebs_optimized": true,
    "volume_type": "gp3",
    "volume_size": 100,
    "volume_iops": 3000,
    "volume_throughput": 125,
    "monitoring": true,
    "placement_group": "web-tier-pg",
    "tenancy": "default",
    "elastic_gpu_associations": ["egp-assoc-1234567890abcdef0"],
    "elastic_inference_accelerators": ["eia-assoc-1234567890abcdef0"],
    "credit_specification": {
      "cpu_credits": "standard"
    },
    "cpu_options": {
      "core_count": 2,
      "threads_per_core": 2
    },
    "capacity_reservation_specification": {
      "capacity_reservation_preference": "open"
    },
    "hibernation_options": {
      "configured": true
    },
    "metadata_options": {
      "http_tokens": "required",
      "http_put_response_hop_limit": 2,
      "http_endpoint": "enabled"
    },
    "enclave_options": {
      "enabled": true
    },
    "tags": {
      "Name": "web-server-01",
      "Environment": "production",
      "Application": "customer-portal",
      "CostCenter": "12345",
      "DataClassification": "confidential",
      "Backup": "enabled",
      "PatchGroup": "production-servers"
    }
  }
}'
```

## 📈 Consultas y Filtros

### 1. 📋 Obtener todas las VMs (paginado)
```bash
curl "http://localhost:8000/api/v1/vms?limit=10&offset=0"
```

### 2. 🔍 Filtrar VMs por proveedor
```bash
# Todas las VMs de AWS
curl "http://localhost:8000/api/v1/vms/provider/aws"

# VMs de Azure con estado 'running'
curl "http://localhost:8000/api/v1/vms/provider/azure?status=running"
```

### 3. 🎯 Filtrar VMs por estado
```bash
# Todas las VMs en ejecución
curl "http://localhost:8000/api/v1/vms/status/running"

# VMs detenidas
curl "http://localhost:8000/api/v1/vms/status/stopped"
```

### 4. 📊 Obtener resumen estadístico
```bash
curl "http://localhost:8000/api/v1/vms-summary"
```

### 5. 🔎 Buscar VM específica por ID
```bash
curl "http://localhost:8000/api/v1/vms/i-1234567890abcdef0"
```

### 6. ⚡ Actualizar estado de VM
```bash
curl -X PUT "http://localhost:8000/api/v1/vms/i-1234567890abcdef0/status" \
-H "Content-Type: application/json" \
-d '{"new_status": "stopped"}'
```

## 🎛️ Respuestas de Ejemplo

### Respuesta exitosa (VM creada):
```json
{
  "request_id": "req_a1b2c3d4",
  "status": "success",
  "vm_id": "i-1234567890abcdef0",
  "error_message": null,
  "provider_type": "aws",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Respuesta con error:
```json
{
  "request_id": "req_e5f6g7h8",
  "status": "error",
  "vm_id": null,
  "error_message": "Parámetros inválidos para AWS: falta 'instance_type'",
  "provider_type": "aws",
  "timestamp": "2024-01-15T10:31:22.654321"
}
```

### Resumen de VMs:
```json
{
  "total_vms": 25,
  "vms_by_provider": {
    "aws": 12,
    "azure": 8,
    "gcp": 4,
    "on_premise": 1
  },
  "vms_by_status": {
    "running": 18,
    "stopped": 5,
    "pending": 2
  },
  "recent_vms": [...]
}
```

## 🔧 Parámetros Requeridos por Proveedor

### **AWS EC2**
| Parámetro | Tipo | Requerido | Ejemplo |
|-----------|------|-----------|---------|
| `instance_type` | string | ✅ | `t2.micro`, `m5.large` |
| `region` | string | ✅ | `us-east-1`, `eu-west-1` |
| `vpc` | string | ✅ | `vpc-1234567890abcdef0` |
| `ami` | string | ✅ | `ami-0abcdef1234567890` |
| `key_name` | string | ❌ | `my-keypair` |
| `security_groups` | array | ❌ | `["web-sg", "ssh-sg"]` |

### **Azure Virtual Machines**
| Parámetro | Tipo | Requerido | Ejemplo |
|-----------|------|-----------|---------|
| `vm_size` | string | ✅ | `Standard_B1s`, `Standard_D2s_v3` |
| `resource_group` | string | ✅ | `my-resource-group` |
| `location` | string | ✅ | `eastus`, `westeurope` |
| `image_publisher` | string | ❌ | `Canonical`, `MicrosoftWindowsServer` |
| `admin_username` | string | ❌ | `azureuser` |

### **Google Cloud Platform**
| Parámetro | Tipo | Requerido | Ejemplo |
|-----------|------|-----------|---------|
| `machine_type` | string | ✅ | `n1-standard-1`, `e2-medium` |
| `zone` | string | ✅ | `us-central1-a`, `europe-west1-b` |
| `project_id` | string | ✅ | `my-gcp-project-123456` |
| `image_family` | string | ❌ | `ubuntu-2004-lts` |
| `network` | string | ❌ | `default` |

### **On-Premise**
| Parámetro | Tipo | Requerido | Ejemplo |
|-----------|------|-----------|---------|
| `cpu_cores` | integer | ✅ | `2`, `8`, `16` |
| `ram_gb` | integer | ✅ | `4`, `16`, `32` |
| `storage_gb` | integer | ✅ | `50`, `200`, `1000` |
| `host_server` | string | ❌ | `hypervisor-01.company.local` |
| `os_template` | string | ❌ | `ubuntu-20.04-template` |

## 🛠️ Desarrollo y Extensión

### Añadir nuevo proveedor:

1. **Crear clase del proveedor**:
```python
class OracleCloudProvider(VMProvider):
    def __init__(self):
        super().__init__()
        self.provider_name = "Oracle"
        self.required_params = ["shape", "compartment_id", "availability_domain"]
    
    def create_vm(self, parameters):
        # Lógica específica de Oracle Cloud
        pass
```

2. **Registrar en el factory**:
```python
# En VMProviderFactory
self._providers[ProviderType.ORACLE] = OracleCloudProvider
```

3. **¡Listo!** El nuevo proveedor estará disponible automáticamente.

## 📝 Notas Importantes

- ✅ **Logs seguros**: Información sensible (credenciales, tokens) se sanitiza automáticamente
- ✅ **Validación**: Parámetros se validan según el proveedor específico
- ✅ **Extensible**: Nuevos proveedores sin modificar código existente
- ✅ **Stateless**: API diseñada para escalabilidad horizontal
- ✅ **Documentación**: Swagger UI automática en `/docs`

## 🐛 Solución de Problemas

### Error común: Parámetros faltantes
```json
{
  "status": "error",
  "error_message": "Parámetros inválidos para AWS: falta 'instance_type'"
}
```

**Solución**: Verificar los parámetros requeridos en la documentación del proveedor.

### Error común: Proveedor no soportado
```json
{
  "status": "error", 
  "error_message": "Proveedor no soportado: oracle"
}
```

**Solución**: Usar `GET /api/v1/providers` para ver proveedores disponibles.

---
