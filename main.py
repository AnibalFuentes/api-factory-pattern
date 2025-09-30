from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import uvicorn

from models.schemas import VMRequest, VMResponse, ProviderInfo, VMListResponse, ProviderVMsResponse, VMStatus
from services.vm_service import VMProvisioningService

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("vm_provisioning_api")

# Crear aplicación FastAPI con tags organizados
app = FastAPI(
    title="VM Provisioning Multi-Cloud API",
    description="""
    API unificada para aprovisionar y gestionar máquinas virtuales en diferentes proveedores cloud.
    
    Características principales:
    
     ✅ Aprovisionamiento Multi-Cloud: Crea VMs en AWS, Azure, GCP y On-Premise
     ✅ Patrón Factory Method: Arquitectura extensible y mantenible
     ✅ Gestión de VMs: Consulta, filtra y actualiza máquinas virtuales
     ✅ Estadísticas: Resúmenes y métricas por proveedor
     ✅ Seguridad: Logs sanitizados y validación de parámetros
    
    Proveedores soportados:
    - AWS EC2
    - Azure Virtual Machines  
    - Google Cloud Compute Engine
    - Infraestructura On-Premise
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "anidev0308@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Inicializar servicio
vm_service = VMProvisioningService()
vm_service.set_logger(logger)

# =============================================================================
# ENDPOINTS DE INFORMACIÓN Y HEALTH CHECK
# =============================================================================

@app.get("/", tags=["Información"])
async def root():
    """Endpoint raíz con información general de la API"""
    return {
        "message": "VM Provisioning Multi-Cloud API",
        "version": "1.0.0",
        "description": "API unificada para aprovisionamiento de máquinas virtuales multi-cloud",
        "endpoints": {
            "provision": "POST /api/v1/vm/provision",
            "providers": "GET /api/v1/providers",
            "all_vms": "GET /api/v1/vms",
            "vms_by_provider": "GET /api/v1/vms/provider/{provider_type}",
            "vms_by_status": "GET /api/v1/vms/status/{status}",
            "vm_by_id": "GET /api/v1/vms/{vm_id}",
            "vms_summary": "GET /api/v1/vms-summary",
            "health": "GET /health"
        }
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check del API - Verifica estado del servicio"""
    return {
        "status": "healthy", 
        "service": "vm_provisioning",
        "timestamp": vm_service._get_timestamp()
    }

# =============================================================================
# ENDPOINTS DE PROVEEDORES
# =============================================================================

@app.get("/api/v1/providers", 
         response_model=dict[str, ProviderInfo],
         tags=["Proveedores"],
         summary="Obtener proveedores disponibles",
         description="Retorna la lista de todos los proveedores cloud soportados y sus parámetros requeridos")
async def get_available_providers():
    try:
        providers = vm_service.get_available_providers()
        return providers
    except Exception as e:
        logger.error(f"Error obteniendo proveedores: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# =============================================================================
# ENDPOINTS DE APROVISIONAMIENTO
# =============================================================================

@app.post("/api/v1/vm/provision", 
          response_model=VMResponse,
          tags=["Aprovisionamiento"],
          summary="Crear nueva máquina virtual",
          description="""
          Endpoint principal para aprovisionar máquinas virtuales en cualquier proveedor cloud soportado.
          
          ### Parámetros por proveedor:
          
          AWS:
          - instance_type (ej: t2.micro)
          - region (ej: us-east-1) 
          - vpc (ej: vpc-123456)
          - ami (ej: ami-0abcdef1234567890)
          
          Azure:
          - vm_size (ej: Standard_B1s)
          - resource_group (ej: my-resource-group)
          - location (ej: eastus)
          
          GCP:
          - machine_type (ej: n1-standard-1)
          - zone (ej: us-central1-a)
          - project_id (ej: my-project-123)
          
          On-Premise:
          - cpu_cores (ej: 2)
          - ram_gb (ej: 4)
          - storage_gb (ej: 50)
          """)
async def provision_vm(vm_request: VMRequest):
    try:
        logger.info(f"Solicitud de aprovisionamiento recibida para {vm_request.provider_type}")
        
        # Procesar la solicitud
        response = vm_service.provision_vm(vm_request)
        
        # Log del resultado
        if response.status == "success":
            logger.info(f"VM creada exitosamente: {response.vm_id}")
        else:
            logger.error(f"Error creando VM: {response.error_message}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

# =============================================================================
# ENDPOINTS DE CONSULTA DE VMs
# =============================================================================

@app.get("/api/v1/vms", 
         response_model=VMListResponse,
         tags=["Consultas de VMs"],
         summary="Obtener todas las VMs",
         description="Retorna todas las máquinas virtuales creadas, organizadas por tipo de proveedor con paginación")
async def get_all_vms(
    limit: int = Query(100, ge=1, le=1000, description="Límite de resultados por página"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    try:
        response = vm_service.get_all_vms()
        
        # Aplicar paginación
        if offset < len(response.vms):
            response.vms = response.vms[offset:offset + limit]
        else:
            response.vms = []
        
        return response
        
    except Exception as e:
        logger.error(f"Error obteniendo VMs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get("/api/v1/vms/provider/{provider_type}", 
         response_model=ProviderVMsResponse,
         tags=["Consultas de VMs"],
         summary="Obtener VMs por proveedor",
         description="Retorna máquinas virtuales filtradas por un proveedor cloud específico")
async def get_vms_by_provider(
    provider_type: str,
    status: Optional[VMStatus] = Query(None, description="Filtrar por estado específico")
):
    try:
        # Validar que el proveedor existe
        providers = vm_service.get_available_providers()
        if provider_type not in providers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {provider_type} no encontrado. Proveedores disponibles: {list(providers.keys())}"
            )
        
        response = vm_service.get_vms_by_provider(provider_type)
        
        # Filtrar por estado si se especifica
        if status:
            response.vms = [vm for vm in response.vms if vm.status == status]
            response.total_vms = len(response.vms)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo VMs por proveedor: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get("/api/v1/vms/status/{status}", 
         response_model=VMListResponse,
         tags=["Consultas de VMs"],
         summary="Obtener VMs por estado",
         description="Retorna máquinas virtuales filtradas por estado específico")
async def get_vms_by_status(status: VMStatus):
    try:
        vms = vm_service.get_vms_by_status(status)
        
        # Calcular resumen por proveedor
        vms_by_provider = {}
        for vm in vms:
            vms_by_provider[vm.provider_type] = vms_by_provider.get(vm.provider_type, 0) + 1
        
        return VMListResponse(
            total_vms=len(vms),
            vms_by_provider=vms_by_provider,
            vms=vms
        )
        
    except Exception as e:
        logger.error(f"Error obteniendo VMs por estado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@app.get("/api/v1/vms/{vm_id}",
         tags=["Consultas de VMs"],
         summary="Obtener VM por ID",
         description="Retorna los detalles completos de una máquina virtual específica usando su ID único")
async def get_vm_by_id(vm_id: str):
    try:
        vm = vm_service.get_vm_by_id(vm_id)
        return vm
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error obteniendo VM por ID: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# =============================================================================
# ENDPOINTS DE ESTADÍSTICAS Y MÉTRICAS
# =============================================================================

@app.get("/api/v1/vms-summary",
         tags=["Estadísticas"],
         summary="Resumen de VMs",
         description="Retorna un resumen estadístico con métricas agregadas de todas las máquinas virtuales")
async def get_vms_summary():
    try:
        summary = vm_service.get_vms_summary()
        return summary
        
    except Exception as e:
        logger.error(f"Error obteniendo resumen de VMs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

# =============================================================================
# ENDPOINTS DE GESTIÓN DE ESTADOS
# =============================================================================

@app.put("/api/v1/vms/{vm_id}/status",
         tags=["Gestión de Estados"],
         summary="Actualizar estado de VM",
         description="Actualiza el estado de una máquina virtual existente")
async def update_vm_status(vm_id: str, new_status: VMStatus):
    try:
        success = vm_service.update_vm_status(vm_id, new_status)
        
        if success:
            return {
                "message": f"Estado de VM {vm_id} actualizado a {new_status}",
                "vm_id": vm_id,
                "new_status": new_status,
                "timestamp": vm_service._get_timestamp()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"VM con ID {vm_id} no encontrada"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error actualizando estado de VM: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )