def get_application_data(
    **kwargs,
):
    return {
        'id': '3c819c1d-6587-448d-8ba4-3b6f23e87ed4',
        'user': '43f619df-3ba2-4d9d-bcdd-270484eac44d',
        'user_name': 'VittorinoColiandro',
        'service': 'pagamento-tari',
        'service_id': 'df171f10-bea7-4701-afd5-797693fd3b08',
        'service_name': 'PagamentoTari',
        'service_group_name': None,
        'tenant_id': '2eeb8374-c8f9-4260-9e94-22504e262eb1',
        'subject': None,
        'data': {
            'applicant.data.email_address': 'info@comune.bugliano.pi.it',
            'applicant.data.Born.data.natoAIl': '1976-09-01T00:00:00+01:00',
            'applicant.data.Born.data.place_of_birth': 'Ponsacco',
            'applicant.data.completename.data.name': 'Vittorino',
            'applicant.data.completename.data.surname': 'Coliandro',
            'applicant.data.gender.data.gender': 'maschio',
            'applicant.data.address.data.address': 'ViaGramsci',
            'applicant.data.address.data.house_number': '1',
            'applicant.data.address.data.municipality': 'Bugliano',
            'applicant.data.address.data.county': 'PI',
            'applicant.data.address.data.postal_code': '56056',
            'applicant.data.fiscal_code.data.fiscal_code': 'CLNVTR76P01G822Q',
            'payment_amount': '10',
        },
        'compiled_modules': [],
        'attachments': [],
        'creation_time': 1651137330,
        'created_at': '2022-04-28T11:15:30+02:00',
        'submission_time': 1651137521,
        'submitted_at': '2022-04-28T11:18:41+02:00',
        'latest_status_change_time': 1651137521,
        'latest_status_change_at': '2022-04-28T11:18:41+02:00',
        'protocol_folder_number': None,
        'protocol_folder_code': None,
        'protocol_number': None,
        'protocol_document_id': None,
        'protocol_numbers': [],
        'protocol_time': None,
        'protocolled_at': None,
        'outcome': None,
        'outcome_motivation': None,
        'outcome_file': None,
        'outcome_attachments': [],
        'outcome_protocol_number': None,
        'outcome_protocol_document_id': None,
        'outcome_protocol_numbers': None,
        'outcome_protocol_time': None,
        'outcome_protocolled_at': None,
        'payment_type': None,
        'payment_data': {
            'reason': 'PagamentoTari-3c819c1d-6587-448d-8ba4-3b6f23e87ed4',
            'amount': '10',
            'expire_at': '2022-04-28T11:18:41+02:00',
            'split': [{'code': '2020/1', 'amount': '8', 'meta': {}}, {'code': '2020/2', 'amount': '2', 'meta': {}}],
            'notify': {
                'url': 'https://www2.stanzadelcittadino.it'
                '/comune-di-bugliano/api/applications/3c819c1d-6587-448d-8ba4-3b6f23e87ed4/payment',
                'method': 'POST',
            },
            'landing': {
                'url': 'https://www2.stanzadelcittadino.it'
                '/comune-di-bugliano/pratiche/3c819c1d-6587-448d-8ba4-3b6f23e87ed4/detail',
                'method': 'GET',
            },
        },
        'status': '1500',
        'status_name': 'status_payment_pending',
        'authentication': {
            'authentication_method': 'spid',
            'session_id': 'abc123abc123abc123abc123abc123abc123abc123',
            'spid_code': '123456789',
            'spid_level': None,
            'certificate_issuer': None,
            'certificate_subject': None,
            'certificate': None,
            'instant': '2000-01-01T00-00Z',
            'session_index': 'abc123abc123abc123abc123abc123abc123abc123',
        },
        'links': [],
        'meetings': [],
        'integrations': [],
        'backoffice_data': None,
        'flow_changed_at': '2022-04-28T11:18:41+02:00',
        'locale': 'IT',
        'event_version': '2.0',
        'event_id': 'bb7044e4-066c-4bf7-915e-87ee97270eae',
        **kwargs,
    }


def get_application_minimal_applicant_data(**kwargs):
    return {
        'applicant.data.completename.data.name': 'Vittorino',
        'applicant.data.completename.data.surname': 'Coliandro',
        'applicant.data.fiscal_code.data.fiscal_code': 'CLNVTR76P01G822Q',
        'payment_amount': '3',
        **kwargs,
    }


def get_application_payment_data(**kwargs):
    return {
        'reason': 'PagamentoTari-3c819c1d-6587-448d-8ba4-3b6f23e87ed4',
        'amount': '10',
        'expire_at': '2022-04-28T11:18:41+02:00',
        'split': [{'code': '2020/1', 'amount': '8', 'meta': {}}, {'code': '2020/2', 'amount': '2', 'meta': {}}],
        'notify': {
            'url': 'https://www2.stanzadelcittadino.it'
            '/comune-di-bugliano/api/applications/3c819c1d-6587-448d-8ba4-3b6f23e87ed4/payment',
            'method': 'POST',
        },
        'landing': {
            'url': 'https://www2.stanzadelcittadino.it'
            '/comune-di-bugliano/pratiche/3c819c1d-6587-448d-8ba4-3b6f23e87ed4/detail',
            'method': 'GET',
        },
        **kwargs,
    }


def get_payment_event_data(**kwargs):
    return {
        'id': 'bb7044e4-066c-4bf7-915e-87ee97270eae',
        'user_id': '43f619df-3ba2-4d9d-bcdd-270484eac44d',
        'type': 'PAGOPA',
        'tenant_id': '2eeb8374-c8f9-4260-9e94-22504e262eb1',
        'service_id': 'cf9ece67-1956-49c9-af89-a19120485fef',
        'created_at': '2022-06-08T08:28:42+00:00',
        'updated_at': '2022-06-08T10:29:39+02:00',
        'status': 'CREATION_PENDING',
        'reason': 'a51cc065-4fb1-4ace-8d3f-e3a70c867472 - SLVLNZ76P01g843v',
        'remote_id': 'a51cc065-4fb1-4ace-8d3f-e3a70c867472',
        'payment': {
            'transaction_id': None,
            'paid_at': None,
            'expire_at': '2022-09-06T10:28:42+02:00',
            'amount': 1,
            'currency': 'EUR',
            'notice_code': None,
            'iud': 'bb7044e4066c4bf7915e87ee97270eae',
            'iuv': None,
            'split': [],
        },
        'links': {
            'online_payment_begin': {'url': None, 'last_opened_at': None, 'method': 'GET'},
            'online_payment_landing': {
                'url': 'https://devsdc.opencontent.it/'
                'comune-di-bugliano/it/pratiche/a51cc065-4fb1-4ace-8d3f-e3a70c867472/detail',
                'last_opened_at': None,
                'method': 'GET',
            },
            'offline_payment': {'url': None, 'last_opened_at': None, 'method': 'GET'},
            'receipt': {'url': None, 'last_opened_at': None, 'method': 'GET'},
            'notify': [
                {
                    'url': 'https://devsdc.opencontent.it/'
                    'comune-di-bugliano/api/applications/a51cc065-4fb1-4ace-8d3f-e3a70c867472/payment',
                    'method': 'POST',
                    'sent_at': None,
                },
            ],
            'update': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'GET'},
            'confirm': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'PATCH'},
            'cancel': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'PATCH'},
        },
        'payer': {
            'type': 'human',
            'tax_identification_number': 'SLVLNZ76P01G843V',
            'name': 'Lorenzo',
            'family_name': 'Salvadorini',
            'street_name': None,
            'building_number': None,
            'postal_code': None,
            'town_name': None,
            'country_subdivision': None,
            'country': 'IT',
            'email': 'raffaele.luccisano@opencontent.it',
        },
        'locale': 'IT',
        'event_id': 'c5cebc1a-5d6f-4921-bc15-ff0575ea6f75',
        'event_version': '2.0',
        'event_created_at': '2022-06-08T08:28:42+00:00',
        'app_id': 'payment-dispatcher:1.0.15',
        **kwargs,
    }


def get_payment_data(**kwargs):
    return {
        'transaction_id': None,
        'paid_at': None,
        'expire_at': '2022-09-06T10:28:42+02:00',
        'amount': 1,
        'currency': 'EUR',
        'notice_code': None,
        'iud': 'bb7044e4066c4bf7915e87ee97270eae',
        'iuv': None,
        'split': [],
        **kwargs,
    }


def get_split_data(**kwargs):
    return {
        'amount': 1,
        'code': 'CODE',
        'meta': {},
        **kwargs,
    }


def get_split_data_invalid(**kwargs):
    return {
        'c_1': '14.00',
        'c_2': None,
        **kwargs,
    }


def get_split_data_complete():
    return [
        {
            'code': 'c_1',
            'amount': '16.00',
            'meta': {
                'split_type': 'Tipo c1',
                'split_code': 'Codice c1',
                'split_description': 'Descrizione c1',
                'split_budget_chapter': 'Capitolo di bilancio c1',
                'split_assessment': 'Accertamento c1',
            },
        },
        {
            'code': 'c_2',
            'amount': '0.50',
            'meta': {
                'split_type': 'Tipo c2',
                'split_code': 'Codice c2',
                'split_description': 'Descrizione c12',
                'split_budget_chapter': 'Capitolo di bilancio c2',
                'split_assessment': 'Accertamento c2',
            },
        },
    ]


def get_payer_data(**kwargs):
    return {
        'type': 'human',
        'tax_identification_number': 'SLVLNZ76P01G843V',
        'name': 'Lorenzo',
        'family_name': 'Salvadorini',
        'street_name': None,
        'building_number': None,
        'postal_code': None,
        'town_name': None,
        'country_subdivision': None,
        'country': 'IT',
        'email': 'raffaele.luccisano@opencontent.it',
        **kwargs,
    }


def get_links_data(**kwargs):
    return {
        'online_payment_begin': {'url': None, 'last_opened_at': None, 'method': 'GET'},
        'online_payment_landing': {
            'url': 'https://devsdc.opencontent.it/'
            'comune-di-bugliano/it/pratiche/a51cc065-4fb1-4ace-8d3f-e3a70c867472/detail',
            'last_opened_at': None,
            'method': 'GET',
        },
        'offline_payment': {'url': None, 'last_opened_at': None, 'method': 'GET'},
        'receipt': {'url': None, 'last_opened_at': None, 'method': 'GET'},
        'notify': [
            {
                'url': 'https://devsdc.opencontent.it/'
                'comune-di-bugliano/api/applications/a51cc065-4fb1-4ace-8d3f-e3a70c867472/payment',
                'method': 'POST',
                'sent_at': None,
            },
        ],
        'update': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'GET'},
        'confirm': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'PATCH'},
        'cancel': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'PATCH'},
        **kwargs,
    }


def get_links_data_without_cancel_and_confirm(**kwargs):
    return {
        'online_payment_begin': {'url': None, 'last_opened_at': None, 'method': 'GET'},
        'online_payment_landing': {
            'url': 'https://devsdc.opencontent.it/'
            'comune-di-bugliano/it/pratiche/a51cc065-4fb1-4ace-8d3f-e3a70c867472/detail',
            'last_opened_at': None,
            'method': 'GET',
        },
        'offline_payment': {'url': None, 'last_opened_at': None, 'method': 'GET'},
        'receipt': {'url': None, 'last_opened_at': None, 'method': 'GET'},
        'notify': [
            {
                'url': 'https://devsdc.opencontent.it/'
                'comune-di-bugliano/api/applications/a51cc065-4fb1-4ace-8d3f-e3a70c867472/payment',
                'method': 'POST',
                'sent_at': None,
            },
        ],
        'update': {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'GET'},
        **kwargs,
    }


def get_online_payment_begin_data(**kwargs):
    return {'url': None, 'last_opened_at': None, 'method': 'GET', **kwargs}


def get_online_payment_landing_data(**kwargs):
    return {
        'url': 'https://devsdc.opencontent.it/'
        'comune-di-bugliano/it/pratiche/a51cc065-4fb1-4ace-8d3f-e3a70c867472/detail',
        'last_opened_at': None,
        'method': 'GET',
        **kwargs,
    }


def get_notify_data(**kwargs):
    return {
        'url': 'https://devsdc.opencontent.it/'
        'comune-di-bugliano/api/applications/a51cc065-4fb1-4ace-8d3f-e3a70c867472/payment',
        'method': 'POST',
        'sent_at': None,
        **kwargs,
    }


def get_empty_notify_data(**kwargs):
    return {
        'url': None,
        'method': None,
        'sent_at': None,
        **kwargs,
    }


def get_offline_payment_data(**kwargs):
    return {'url': None, 'last_opened_at': None, 'method': 'GET', **kwargs}


def get_update_data(**kwargs):
    return {'url': None, 'last_check_at': None, 'next_check_at': None, 'method': 'GET', **kwargs}
