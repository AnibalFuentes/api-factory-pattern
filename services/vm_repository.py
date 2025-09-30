from typing import Dict, List, Optional
from models.schemas import VMDetails, VMStatus, ProviderType
import json
import os
from datetime import datetime

class VMRepository:
    """Repositorio para almacenar y consultar información de VMs creadas"""
    
    def __init__(self, storage_file: str = "vm_storage.json"):
        self.storage_file = storage_file
        self._ensure_storage_file()
    
    def _ensure_storage_file(self):
        """Asegura que el archivo de almacenamiento exista"""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump({"vms": {}}, f)
    
    def save_vm(self, vm_details: VMDetails):
        """Guarda los detalles de una VM creada"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            # Agregar la nueva VM
            if "vms" not in data:
                data["vms"] = {}
            
            data["vms"][vm_details.vm_id] = {
                "vm_id": vm_details.vm_id,
                "provider_type": vm_details.provider_type,
                "status": vm_details.status,
                "instance_type": vm_details.instance_type,
                "region": vm_details.region,
                "created_at": vm_details.created_at,
                "parameters": vm_details.parameters
            }
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error guardando VM: {e}")
    
    def get_all_vms(self) -> List[VMDetails]:
        """Obtiene todas las VMs almacenadas"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            vms = []
            for vm_id, vm_data in data.get("vms", {}).items():
                vms.append(VMDetails(**vm_data))
            
            return sorted(vms, key=lambda x: x.created_at, reverse=True)
            
        except Exception as e:
            print(f"Error leyendo VMs: {e}")
            return []
    
    def get_vms_by_provider(self, provider_type: str) -> List[VMDetails]:
        """Obtiene VMs filtradas por proveedor"""
        all_vms = self.get_all_vms()
        return [vm for vm in all_vms if vm.provider_type.lower() == provider_type.lower()]
    
    def get_vms_by_status(self, status: VMStatus) -> List[VMDetails]:
        """Obtiene VMs filtradas por estado"""
        all_vms = self.get_all_vms()
        return [vm for vm in all_vms if vm.status == status]
    
    def get_vm_by_id(self, vm_id: str) -> Optional[VMDetails]:
        """Obtiene una VM específica por ID"""
        all_vms = self.get_all_vms()
        for vm in all_vms:
            if vm.vm_id == vm_id:
                return vm
        return None
    
    def get_vms_summary(self) -> Dict:
        """Obtiene un resumen de todas las VMs"""
        all_vms = self.get_all_vms()
        
        summary = {
            "total_vms": len(all_vms),
            "vms_by_provider": {},
            "vms_by_status": {},
            "recent_vms": all_vms[:10]  # Últimas 10 VMs
        }
        
        # Conteo por proveedor
        for vm in all_vms:
            provider = vm.provider_type
            status = vm.status
            
            summary["vms_by_provider"][provider] = summary["vms_by_provider"].get(provider, 0) + 1
            summary["vms_by_status"][status] = summary["vms_by_status"].get(status, 0) + 1
        
        return summary
    
    def update_vm_status(self, vm_id: str, new_status: VMStatus) -> bool:
        """Actualiza el estado de una VM"""
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
            
            if vm_id in data.get("vms", {}):
                data["vms"][vm_id]["status"] = new_status
                
                with open(self.storage_file, 'w') as f:
                    json.dump(data, f, indent=2)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error actualizando VM: {e}")
            return False