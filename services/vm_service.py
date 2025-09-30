from typing import Dict, Any, List
from factories.provider_factory import VMProviderFactory
from models.providers import VMProvider
from models.schemas import VMRequest, VMResponse, ProviderType, ProviderInfo, VMDetails, VMStatus, VMListResponse, ProviderVMsResponse
from services.vm_repository import VMRepository
from datetime import datetime

class VMProvisioningService:
    """Servicio principal para el aprovisionamiento de VMs"""
    
    def __init__(self):
        self.provider_factory = VMProviderFactory()
        self.vm_repository = VMRepository()
        self.logger = None
    
    def set_logger(self, logger):
        self.logger = logger
    
    def provision_vm(self, vm_request: VMRequest) -> VMResponse:
        """Procesa una solicitud de aprovisionamiento de VM"""
        
        try:
            # Crear el proveedor específico usando el Factory
            provider = self.provider_factory.create_provider(vm_request.provider_type)
            
            # Ejecutar la creación de la VM
            response = provider.create_vm(vm_request.parameters)
            
            # Si fue exitosa, guardar en el repositorio
            if response.status == "success":
                vm_details = VMDetails(
                    vm_id=response.vm_id,
                    provider_type=vm_request.provider_type.value,
                    status=VMStatus.RUNNING,
                    instance_type=vm_request.parameters.get("instance_type") or 
                                 vm_request.parameters.get("vm_size") or 
                                 vm_request.parameters.get("machine_type"),
                    region=vm_request.parameters.get("region") or 
                           vm_request.parameters.get("location") or 
                           vm_request.parameters.get("zone"),
                    created_at=response.timestamp,
                    parameters=self._sanitize_parameters(vm_request.parameters)
                )
                self.vm_repository.save_vm(vm_details)
            
            return response
            
        except ValueError as e:
            # Proveedor no soportado
            return VMResponse(
                request_id=f"error_{id(vm_request)}",
                status="error",
                error_message=str(e),
                provider_type=vm_request.provider_type.value,
                timestamp=self._get_timestamp()
            )
        except Exception as e:
            # Error general
            return VMResponse(
                request_id=f"error_{id(vm_request)}",
                status="error",
                error_message=f"Error interno: {str(e)}",
                provider_type=vm_request.provider_type.value,
                timestamp=self._get_timestamp()
            )
    
    def _sanitize_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Elimina información sensible de los parámetros antes de guardar"""
        sensitive_keys = ['password', 'credential', 'token', 'key', 'secret', 'api_key']
        sanitized = parameters.copy()
        
        for key in sanitized.keys():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                sanitized[key] = "***HIDDEN***"
        
        return sanitized
    
    def get_all_vms(self) -> VMListResponse:
        """Obtiene todas las VMs creadas"""
        all_vms = self.vm_repository.get_all_vms()
        summary = self.vm_repository.get_vms_summary()
        
        return VMListResponse(
            total_vms=summary["total_vms"],
            vms_by_provider=summary["vms_by_provider"],
            vms=all_vms
        )
    
    def get_vms_by_provider(self, provider_type: str) -> ProviderVMsResponse:
        """Obtiene VMs filtradas por proveedor"""
        vms = self.vm_repository.get_vms_by_provider(provider_type)
        
        return ProviderVMsResponse(
            provider_type=provider_type,
            total_vms=len(vms),
            vms=vms
        )
    
    def get_vms_by_status(self, status: VMStatus) -> List[VMDetails]:
        """Obtiene VMs filtradas por estado"""
        return self.vm_repository.get_vms_by_status(status)
    
    def get_vm_by_id(self, vm_id: str) -> VMDetails:
        """Obtiene una VM específica por ID"""
        vm = self.vm_repository.get_vm_by_id(vm_id)
        if not vm:
            raise ValueError(f"VM con ID {vm_id} no encontrada")
        return vm
    
    def get_vms_summary(self) -> Dict:
        """Obtiene un resumen estadístico de las VMs"""
        return self.vm_repository.get_vms_summary()
    
    def update_vm_status(self, vm_id: str, new_status: VMStatus) -> bool:
        """Actualiza el estado de una VM"""
        return self.vm_repository.update_vm_status(vm_id, new_status)
    
    def get_available_providers(self) -> Dict[str, ProviderInfo]:
        """Obtiene la lista de proveedores disponibles"""
        return self.provider_factory.get_available_providers()
    
    def _get_timestamp(self):
        return datetime.now().isoformat()