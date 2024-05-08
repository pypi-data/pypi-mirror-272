from typing import ClassVar


class CaseCommentTemplate:
    MALICIOUS_DNS_ALERT: ClassVar = [
        {"type": "header", "value": {"level": 1, "text": "Alerta de DNS Malicioso"}},
        {"type": "header", "value": {"level": 2, "text": "Domínio Suspeito: {dominio_suspeito}"}},
        {
            "type": "unordered_list",
            "value": [
                "IP associado: {ip_associado}",
                "Registrado em: {data_registro}",
                "Atualizado em: {data_atualizacao}",
            ],
        },
    ]
    CASE_MONITORING_DNS_ALERT_YARA: ClassVar = [
        {"type": "header", "value": {"level": 1, "text": "Monitoramento DNS - REGRA YARA"}},
        {"type": "paragraph", "value": "Assunto: Possível Domínio Malicioso Detectado"},
        {
            "type": "paragraph",
            "value": "Descrição: Durante nossas rotinas de monitoramento, identificamos um domínio que exibe "
            "características suspeitas e que pode ser potencialmente malicioso. Solicitamos uma revisão "
            "imediata para determinar a natureza deste domínio e tomar as medidas necessárias para garantir a "
            "segurança da nossa rede e dos nossos dados.",
        },
        {"type": "header", "value": {"level": 2, "text": "Detalhes:"}},
        {
            "type": "unordered_list",
            "value": [
                "Nome do domínio: {dominio_suspeito}",
                "Regra de Detecção: {regra_deteccao}",
                "Client: {cliente}",
            ],
        },
        {"type": "header", "value": {"level": 2, "text": "Recomendações Iniciais:"}},
        {"type": "paragraph", "value": "adicionar recomendaçõe"},
        {"type": "header", "value": {"level": 2, "text": "Observações Adicionais:"}},
        {"type": "paragraph", "value": "adicionar recomendaçõe"},
    ]
