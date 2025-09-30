
### **4. models/providers.py** - Clases de Proveedores

from abc import ABC, abstractmethod
from typing import Dict, Any
import uuid
from .schemas import VMResponse
import logging

logger = logging.getLogger(__name__)

class VMProvider(ABC):
    """Clase abstracta base para todos los proveedores de cloud"""
    
    def __init__(self):
        self.logger = logger
    
    @abstractmethod
    def create_vm(self, parameters: Dict[str, Any]) -> VMResponse:
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        pass
    
    def log_provisioning(self, request_id: str, message: str):
        """Método protegido para logging seguro"""
        safe_message = self._sanitize_sensitive_data(message)
        self.logger.info(f"[{request_id}] {safe_message}")
    
    def _sanitize_sensitive_data(self, data: str) -> str:
        """Elimina información sensible para logs"""
        sensitive_keys = ['password', 'credential', 'token', 'key', 'secret']
        result = data
        for key in sensitive_keys:
            result = result.replace(key, '***')
        return result
    
    def _generate_request_id(self) -> str:
        return f"req_{uuid.uuid4().hex[:8]}"

class AWSProvider(VMProvider):
    """Proveedor específico para AWS EC2"""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "AWS"
        self.required_params = ["instance_type", "region", "vpc", "ami"]
    
    def create_vm(self, parameters: Dict[str, Any]) -> VMResponse:
        request_id = self._generate_request_id()
        
        try:
            self.log_provisioning(request_id, f"Iniciando creación de VM en {self.provider_name}")
            
            # Validar parámetros
            if not self.validate_parameters(parameters):
                return VMResponse(
                    request_id=request_id,
                    status="error",
                    error_message=f"Parámetros inválidos para {self.provider_name}",
                    provider_type=self.provider_name,
                    timestamp=self._get_timestamp()
                )
            
            # Simular lógica específica de AWS
            instance_type = parameters.get("instance_type", "t2.micro")
            region = parameters.get("region", "us-east-1")
            
            # Aquí iría la llamada real a boto3/EC2
            vm_id = f"i-{uuid.uuid4().hex[:8]}"
            
            self.log_provisioning(request_id, f"VM {vm_id} creada exitosamente en {region}")
            
            return VMResponse(
                request_id=request_id,
                status="success",
                vm_id=vm_id,
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            self.log_provisioning(request_id, f"Error en {self.provider_name}: {str(e)}")
            return VMResponse(
                request_id=request_id,
                status="error",
                error_message=str(e),
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return all(param in parameters for param in self.required_params)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

class AzureProvider(VMProvider):
    """Proveedor específico para Azure Virtual Machines"""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "Azure"
        self.required_params = ["vm_size", "resource_group", "location"]
    
    def create_vm(self, parameters: Dict[str, Any]) -> VMResponse:
        request_id = self._generate_request_id()
        
        try:
            self.log_provisioning(request_id, f"Iniciando creación de VM en {self.provider_name}")
            
            if not self.validate_parameters(parameters):
                return VMResponse(
                    request_id=request_id,
                    status="error",
                    error_message=f"Parámetros inválidos para {self.provider_name}",
                    provider_type=self.provider_name,
                    timestamp=self._get_timestamp()
                )
            
            # Simular lógica específica de Azure
            vm_size = parameters.get("vm_size", "Standard_B1s")
            resource_group = parameters.get("resource_group", "default-rg")
            
            vm_id = f"az-vm-{uuid.uuid4().hex[:8]}"
            
            self.log_provisioning(request_id, f"VM {vm_id} creada en resource group {resource_group}")
            
            return VMResponse(
                request_id=request_id,
                status="success",
                vm_id=vm_id,
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            return VMResponse(
                request_id=request_id,
                status="error",
                error_message=str(e),
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return all(param in parameters for param in self.required_params)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

class GCPProvider(VMProvider):
    """Proveedor específico para Google Cloud Compute Engine"""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "GCP"
        self.required_params = ["machine_type", "zone", "project_id"]
    
    def create_vm(self, parameters: Dict[str, Any]) -> VMResponse:
        request_id = self._generate_request_id()
        
        try:
            self.log_provisioning(request_id, f"Iniciando creación de VM en {self.provider_name}")
            
            if not self.validate_parameters(parameters):
                return VMResponse(
                    request_id=request_id,
                    status="error",
                    error_message=f"Parámetros inválidos para {self.provider_name}",
                    provider_type=self.provider_name,
                    timestamp=self._get_timestamp()
                )
            
            # Simular lógica específica de GCP
            machine_type = parameters.get("machine_type", "n1-standard-1")
            zone = parameters.get("zone", "us-central1-a")
            
            vm_id = f"gcp-vm-{uuid.uuid4().hex[:8]}"
            
            self.log_provisioning(request_id, f"VM {vm_id} creada en zona {zone}")
            
            return VMResponse(
                request_id=request_id,
                status="success",
                vm_id=vm_id,
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            return VMResponse(
                request_id=request_id,
                status="error",
                error_message=str(e),
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return all(param in parameters for param in self.required_params)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

class OnPremiseProvider(VMProvider):

    """Proveedor para infraestructura on-premise"""
    
    def __init__(self):
        super().__init__()
        self.provider_name = "OnPremise"
        self.required_params = ["cpu_cores", "ram_gb", "storage_gb"]
    
    def create_vm(self, parameters: Dict[str, Any]) -> VMResponse:
        request_id = self._generate_request_id()
        
        try:
            self.log_provisioning(request_id, f"Iniciando creación de VM en {self.provider_name}")
            
            if not self.validate_parameters(parameters):
                return VMResponse(
                    request_id=request_id,
                    status="error",
                    error_message=f"Parámetros inválidos para {self.provider_name}",
                    provider_type=self.provider_name,
                    timestamp=self._get_timestamp()
                )
            
            # Simular lógica específica on-premise
            cpu_cores = parameters.get("cpu_cores", 2)
            ram_gb = parameters.get("ram_gb", 4)
            
            vm_id = f"onprem-vm-{uuid.uuid4().hex[:8]}"
            
            self.log_provisioning(request_id, f"VM {vm_id} creada con {cpu_cores} CPUs y {ram_gb}GB RAM")
            
            return VMResponse(
                request_id=request_id,
                status="success",
                vm_id=vm_id,
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
            
        except Exception as e:
            return VMResponse(
                request_id=request_id,
                status="error",
                error_message=str(e),
                provider_type=self.provider_name,
                timestamp=self._get_timestamp()
            )
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        return all(param in parameters for param in self.required_params)
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

# class OracleCloudProvider(VMProvider):
    """Proveedor específico para Oracle Cloud Infrastructure (OCI)"""
    
    # def __init__(self):
    #     super().__init__()
    #     self.provider_name = "Oracle Cloud"
    #     self.required_params = ["compartment_id", "shape", "availability_domain", "subnet_id"]
    
    # def create_vm(self, parameters: Dict[str, Any]) -> VMResponse:
    #     request_id = self._generate_request_id()
        
    #     try:
    #         self.log_provisioning(request_id, f"Iniciando creación de VM en {self.provider_name}")
            
    #         # Validar parámetros específicos de Oracle
    #         if not self.validate_parameters(parameters):
    #             return VMResponse(
    #                 request_id=request_id,
    #                 status="error",
    #                 error_message=f"Parámetros inválidos para {self.provider_name}. Requeridos: {', '.join(self.required_params)}",
    #                 provider_type=self.provider_name,
    #                 timestamp=self._get_timestamp()
    #             )
            
    #         # Simular lógica específica de Oracle Cloud
    #         compartment_id = parameters.get("compartment_id")
    #         shape = parameters.get("shape", "VM.Standard.E2.1.Micro")
    #         availability_domain = parameters.get("availability_domain", "AD-1")
            
    #         # Validaciones adicionales específicas de Oracle
    #         validation_error = self._validate_oracle_specifics(parameters)
    #         if validation_error:
    #             return VMResponse(
    #                 request_id=request_id,
    #                 status="error",
    #                 error_message=validation_error,
    #                 provider_type=self.provider_name,
    #                 timestamp=self._get_timestamp()
    #             )
            
    #         # Simular llamada a API de OCI
    #         # En un caso real, aquí usarías el SDK de Oracle
    #         vm_id = f"ocid1.instance.oc1..{uuid.uuid4().hex[:32]}"
            
    #         # Configuraciones específicas de Oracle
    #         self._configure_boot_volume(parameters)
    #         self._configure_network(parameters)
            
    #         self.log_provisioning(
    #             request_id, 
    #             f"VM Oracle creada: {vm_id} en compartment {compartment_id}"
    #         )
            
    #         return VMResponse(
    #             request_id=request_id,
    #             status="success",
    #             vm_id=vm_id,
    #             provider_type=self.provider_name,
    #             timestamp=self._get_timestamp()
    #         )
            
    #     except Exception as e:
    #         self.log_provisioning(request_id, f"Error en Oracle Cloud: {str(e)}")
    #         return VMResponse(
    #             request_id=request_id,
    #             status="error",
    #             error_message=f"Error Oracle Cloud: {str(e)}",
    #             provider_type=self.provider_name,
    #             timestamp=self._get_timestamp()
    #         )
    
    # def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
    #     """Valida parámetros requeridos para Oracle Cloud"""
    #     return all(param in parameters for param in self.required_params)
    
    # def _validate_oracle_specifics(self, parameters: Dict[str, Any]) -> str:
    #     """Validaciones específicas de Oracle Cloud"""
        
    #     # Validar formato de compartment ID
    #     compartment_id = parameters.get("compartment_id", "")
    #     if not compartment_id.startswith("ocid1.compartment."):
    #         return "Compartment ID debe comenzar con 'ocid1.compartment.'"
        
    #     # Validar shape de Oracle
    #     shape = parameters.get("shape", "")
    #     valid_shapes = ["VM.Standard.E2.1.Micro", "VM.Standard.E2.1", "VM.Standard.E2.2"]
    #     if shape and shape not in valid_shapes:
    #         return f"Shape no válido. Válidos: {', '.join(valid_shapes)}"
        
    #     # Validar availability domain
    #     ad = parameters.get("availability_domain", "")
    #     valid_ads = ["AD-1", "AD-2", "AD-3"]
    #     if ad and ad not in valid_ads:
    #         return f"Availability Domain no válido. Válidos: {', '.join(valid_ads)}"
        
    #     return ""
    
    # def _configure_boot_volume(self, parameters: Dict[str, Any]):
    #     """Configura el volumen de boot específico de Oracle"""
    #     image_id = parameters.get("image_id", "ocid1.image.oc1..aaaaaaaaexample")
    #     boot_volume_size = parameters.get("boot_volume_size_gb", 50)
        
    #     self.log_provisioning(
    #         self._generate_request_id(),
    #         f"Configurando boot volume: {image_id}, tamaño: {boot_volume_size}GB"
    #     )
    
    # def _configure_network(self, parameters: Dict[str, Any]):
    #     """Configura red específica de Oracle"""
    #     subnet_id = parameters.get("subnet_id")
    #     assign_public_ip = parameters.get("assign_public_ip", True)
        
    #     self.log_provisioning(
    #         self._generate_request_id(),
    #         f"Configurando red: subnet={subnet_id}, public_ip={assign_public_ip}"
    #     )
    
    # def _get_timestamp(self):
    #     return datetime.now().isoformat()