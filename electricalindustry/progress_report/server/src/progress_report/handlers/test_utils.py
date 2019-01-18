def get_on_work_person_list_test():
    person_list = ['person_linfeng', 'person_raoguihe', 'person_wangtao']
    return person_list


def get_plan_data_test():
    plan_data_list = [
        {
            'plan_number': 'plan_001',
            'material_name': 'T901H40ADC12V 4脚 23规格',
            'material_code': 'materiel_t901h40adc12v4_23',
            'plan_count': 100,
            'total_plan_qualified_count': 95,
            'total_plan_unqualified_count': 5,
            'current_qualified_count': 70,
            'current_unqualified_count': 10,
            'plan_progress': '95%'
        },
        {
            'plan_number': 'plan_002',
            'material_name': 'T901H40ADC12V 4脚 23规格',
            'material_code': 'materiel_t901h40adc12v4_23',
            'plan_count': 200,
            'total_plan_qualified_count': 100,
            'total_plan_unqualified_count': None,
            'current_qualified_count': 152,
            'current_unqualified_count': None,
            'plan_progress': '50%'
        },
        {
            'plan_number': 'plan_003',
            'material_name': 'T901H40ADC12V 4脚 23规格',
            'material_code': 'materiel_t901h40adc12v4_23',
            'plan_count': 400,
            'total_plan_qualified_count': 100,
            'total_plan_unqualified_count': 15,
            'current_qualified_count': 100,
            'current_unqualified_count': 17,
            'plan_progress': '25%'
        }
    ]
    return plan_data_list
