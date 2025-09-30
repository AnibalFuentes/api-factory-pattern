from pydantic import BaseModel, Field
from typing import Dict, Any, Optional,List
from enum import Enum
from datetime import datetime

class ProviderType(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ON_PREMISE = "on_premise"
    # ORACLE = "oracle"

class VMRequest(BaseModel):
    provider_type: ProviderType = Field(..., description="Tipo de proveedor cloud")
    parameters: Dict[str, Any] = Field(..., description="Parámetros específicos del proveedor")

class VMResponse(BaseModel):
    request_id: str = Field(..., description="ID único de la solicitud")
    status: str = Field(..., description="success o error")
    vm_id: Optional[str] = Field(None, description="ID de la VM creada")
    error_message: Optional[str] = Field(None, description="Mensaje de error si aplica")
    provider_type: str = Field(..., description="Tipo de proveedor utilizado")
    timestamp: str = Field(..., description="Timestamp de la respuesta")

class ProviderInfo(BaseModel):
    name: str
    supported: bool = True
    required_parameters: list[str] = []

class VMStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    PENDING = "pending"
    TERMINATED = "terminated"

class VMDetails(BaseModel):
    vm_id: str = Field(..., description="ID único de la VM")
    provider_type: str = Field(..., description="Tipo de proveedor")
    status: VMStatus = Field(..., description="Estado actual de la VM")
    instance_type: Optional[str] = Field(None, description="Tipo de instancia")
    region: Optional[str] = Field(None, description="Región/ubicación")
    created_at: str = Field(..., description="Fecha de creación")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parámetros de creación")

class VMListResponse(BaseModel):
    total_vms: int = Field(..., description="Número total de VMs")
    vms_by_provider: Dict[str, int] = Field(..., description="Conteo por proveedor")
    vms: List[VMDetails] = Field(..., description="Lista de VMs")

class ProviderVMsResponse(BaseModel):
    provider_type: str = Field(..., description="Tipo de proveedor")
    total_vms: int = Field(..., description="Total de VMs para este proveedor")
    vms: List[VMDetails] = Field(..., description="VMs del proveedor")
    