"""
Utilitários compartilhados
"""
import re
from typing import Optional


def normalize_campaign_name(name: str) -> str:
    """
    Normaliza nome de campanha para matching
    - Remove caracteres especiais
    - Converte para minúsculo
    - Remove espaços extras
    """
    if not name:
        return ""
    
    # Converter para minúsculo
    normalized = name.lower()
    
    # Remover caracteres especiais, manter apenas letras, números e espaços
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    
    # Remover espaços extras
    normalized = ' '.join(normalized.split())
    
    # Substituir espaços por underscore
    normalized = normalized.replace(' ', '_')
    
    return normalized


def extract_utm_params(url: str) -> dict:
    """
    Extrai parâmetros UTM de uma URL
    """
    from urllib.parse import urlparse, parse_qs
    
    params = {}
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        
        for key in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term']:
            if key in query_params:
                params[key] = query_params[key][0]
        
        # Extrair gclid e fbclid se presentes
        if 'gclid' in query_params:
            params['gclid'] = query_params['gclid'][0]
        if 'fbclid' in query_params:
            params['fbclid'] = query_params['fbclid'][0]
            
    except Exception:
        pass
    
    return params


def format_phone_br(phone: str) -> Optional[str]:
    """
    Formata telefone brasileiro
    """
    if not phone:
        return None
    
    # Remover tudo que não é número
    digits = re.sub(r'\D', '', phone)
    
    # Adicionar código do país se não tiver
    if len(digits) == 11:  # Com DDD
        return f"+55{digits}"
    elif len(digits) == 10:  # Fixo com DDD
        return f"+55{digits}"
    elif len(digits) == 9:  # Celular sem DDD
        return f"+5511{digits}"  # Assume SP
    elif len(digits) == 8:  # Fixo sem DDD
        return f"+5511{digits}"
    elif len(digits) == 13 and digits.startswith('55'):
        return f"+{digits}"
    
    return phone  # Retorna original se não conseguir formatar


def calculate_metrics(spend: float, impressions: int, clicks: int, leads: int) -> dict:
    """
    Calcula métricas de campanha
    """
    return {
        'cpc': round(spend / clicks, 4) if clicks > 0 else 0,
        'cpm': round((spend / impressions) * 1000, 4) if impressions > 0 else 0,
        'ctr': round((clicks / impressions) * 100, 4) if impressions > 0 else 0,
        'cpl': round(spend / leads, 4) if leads > 0 else 0,
    }

