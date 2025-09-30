from typing import Dict, Any
from models.providers import VMProvider, AWSProvider, AzureProvider, GCPProvider, OnPremiseProvider
from models.schemas import ProviderType, ProviderInfo

class VMProviderFactory:
    """Factory para crear instancias de proveedores de cloud"""
    
    def __init__(self):
        self._providers = {
            ProviderType.AWS: AWSProvider,
            ProviderType.AZURE: AzureProvider,
            ProviderType.GCP: GCPProvider,
            ProviderType.ON_PREMISE: OnPremiseProvider,
        }
    
    def create_provider(self, provider_type: ProviderType) -> VMProvider:
        """Crea una instancia del proveedor basado en el tipo"""
        provider_class = self._providers.get(provider_type)
        
        if not provider_class:
            raise ValueError(f"Proveedor no soportado: {provider_type}")
        
        return provider_class()
    
    def get_available_providers(self) -> Dict[str, ProviderInfo]:
        """Retorna información de todos los proveedores disponibles"""
        providers_info = {}
        
        for provider_type, provider_class in self._providers.items():
            provider_instance = provider_class()
            providers_info[provider_type.value] = ProviderInfo(
                name=provider_instance.provider_name,
                supported=True,
                required_parameters=provider_instance.required_params
            )
        
        return providers_info
    
    def register_provider(self, provider_type: ProviderType, provider_class):
        """Permite registrar nuevos proveedores dinámicamente"""
        self._providers[provider_type] = provider_class