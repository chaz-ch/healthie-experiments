
STAGE_GLOBAL_PROVIDER_ID = "3920603"
PROD_GLOBAL_PROVIDER_ID = "10666933"
# prod IDs
# 10410358 Karam Elabd          karam@cascaidhealth.com
# 10578403 Tim Herby            tim@cascaidhealth.com
# 10666933 Bridget Krueger      bridget@cascaidhealth.com
# 10578423 Rakesh Patel         rakesh@cascaidhealth.com
# 11008105 Janelle Scachetti    janelle@cascaidhealth.com
# 11008180 Andrea Stage         andrea@cascaidhealth.com
# 10578357 Johann Windt         johann@cascaidhealth.com
# stage IDs
# 3920603	Johann Windt        johann@cascaidhealth.com
# 3969705	Kingsley McGowan    kingsley@cascaidhealth.com
# 3970418	Karam Elabd         karam@cascaidhealth.com
# 3980519	Rakesh Patel        rakesh@cascaidhealth.com
# 3980540	Julia Bauer         julia@cascaidhealth.com
# 3980568	Dave Nicoletti      dave@cascaidhealth.com
# 3980624	Alex Galeazzi       alex@cascaidhealth.com
# 3980644	Donald Sawyer       donald@cascaidhealth.com
# 3980681	Greg Wolff          greg@cascaidhealth.com
# 3980691	Naomi Myhill        naomi@cascaidhealth.com
# 3980737	Bridget Krueger     bridget@cascaidhealth.com
# 3980759	Saawan Patel        saawan@cascaidhealth.com
# 4048025	Amar Kemsaram       amarnath@cascaidhealth.com
# 4272109	Selbin Provider     selbin+provider@fountane.com
# 4283712	Abani Provider      abani+provider@fountane.com

def get_global_provider_id(environment: str) -> str:
    if environment == "STAGE":
        return STAGE_GLOBAL_PROVIDER_ID
    elif environment == "PROD":
        return PROD_GLOBAL_PROVIDER_ID
    else:
        raise ValueError(f"Invalid environment: {environment}")

# stage groups:
# 94781 Project Alpha 0
# 93581 SMI Inbound 40
# prod groups:
# 2 groups found
# 72139 Project Alpha Group 1
# 70105 SimonMed Inbound 79

STAGE_SMI_INBOUND_GROUP_ID = "93581"
PROD_SMI_INBOUND_GROUP_ID = "70105"

def get_smi_inbound_group_id(environment: str) -> str:
    if environment == "STAGE":
        return STAGE_SMI_INBOUND_GROUP_ID
    elif environment == "PROD":
        return PROD_SMI_INBOUND_GROUP_ID
    else:
        raise ValueError(f"Invalid environment: {environment}")

# tag IDs
# Tag name                                 Stage      Prod
# 'Chart::ChartCreated':                  '32333'    '68195'
# 'Chart::OrderCreated':                  '32334'    '68203'
# 'Consent::TelemedicineSigned':          '32335'    '68188'
# 'Engagement::Responsive':               '32336'    '68198'
# 'Engagement::Unresponsive':             '32337'    '68204'

# 'Status::Created':                      '32355'    '68194'
STAGE_CREATED_TAG = "32355"
PROD_CREATED_TAG = "68194"

# 'Status::Invited':                      '32356'    '68207'
STAGE_INVITED_TAG = "32356"
PROD_INVITED_TAG = "68207"

# 'Status::Accessed':                     '32354'    '68193'
STAGE_ACCESSED_TAG = "32354"
PROD_ACCESSED_TAG = "68193"

def get_status_tag_id(environment: str, status: str) -> str:
    if environment == "STAGE":
        if status == "Created":
            return STAGE_CREATED_TAG
        elif status == "Invited":
            return STAGE_INVITED_TAG
        elif status == "Accessed":
            return STAGE_ACCESSED_TAG
        else:
            raise ValueError(f"Invalid status: {status}")
    elif environment == "PROD":
        if status == "Created":
            return PROD_CREATED_TAG
        elif status == "Invited":
            return PROD_INVITED_TAG
        elif status == "Accessed":
            return PROD_ACCESSED_TAG
        else:
            raise ValueError(f"Invalid status: {status}")
    else:
        raise ValueError(f"Invalid environment: {environment}")

# 'ReportType::MGP':                      '32338'    '68196'
# 'ReportType::MGPH':                     '32339'    '68190'
# 'ReportType::StandardMG':               '32340'    '68202'
STAGE_MGP_REPORT_TYPE_TAG = "32338"
STAGE_MGPH_REPORT_TYPE_TAG = "32339"
STAGE_STD_MG_REPORT_TYPE_TAG = "32340"
PROD_MGP_REPORT_TYPE_TAG = "68196"
PROD_MGPH_REPORT_TYPE_TAG = "68190"
PROD_STD_MG_REPORT_TYPE_TAG = "68202"

def get_report_type_tag_id(environment: str, report_type: str) -> str:
    if environment == "STAGE":
        if report_type == "MGP":
            return STAGE_MGP_REPORT_TYPE_TAG
        elif report_type == "MGPH":
            return STAGE_MGPH_REPORT_TYPE_TAG
        elif report_type == "StandardMG":
            return STAGE_STD_MG_REPORT_TYPE_TAG
        else:
            raise ValueError(f"Invalid report type: {report_type}")
    elif environment == "PROD":
        if report_type == "MGP":
            return PROD_MGP_REPORT_TYPE_TAG
        elif report_type == "MGPH":
            return PROD_MGPH_REPORT_TYPE_TAG
        elif report_type == "StandardMG":
            return PROD_STD_MG_REPORT_TYPE_TAG
        else:
            raise ValueError(f"Invalid report type: {report_type}")
    else:
        raise ValueError(f"Invalid environment: {environment}")

# 'Result::BreastDensity::Dense':         '32349'    '68199'
# 'Result::BreastDensity::NonDense':      '32350'    '68187'
STAGE_DENSE_BREAST_DENSITY_TAG = "32349"
STAGE_NON_DENSE_BREAST_DENSITY_TAG = "32350"
PROD_DENSE_BREAST_DENSITY_TAG = "68199"
PROD_NON_DENSE_BREAST_DENSITY_TAG = "68187"

def get_breast_density_tag_id(environment: str, breast_density: str) -> str:
    if environment == "STAGE":
        if breast_density in ["C", "D"]:
            return STAGE_DENSE_BREAST_DENSITY_TAG
        elif breast_density in ["A", "B"]:
            return STAGE_NON_DENSE_BREAST_DENSITY_TAG
        else:
            raise ValueError(f"Invalid breast density: {breast_density}")
    elif environment == "PROD":
        if breast_density in ["C", "D"]:
            return PROD_DENSE_BREAST_DENSITY_TAG
        elif breast_density in ["A", "B"]:
            return PROD_NON_DENSE_BREAST_DENSITY_TAG
        else:
            raise ValueError(f"Invalid breast density: {breast_density}")
    else:
        raise ValueError(f"Invalid environment: {environment}")

# 'Result::TCLifetimeRisk::Average':      '32351'    '68205'
# 'Result::TCLifetimeRisk::High':         '32352'    '68186'
# 'Result::TCLifetimeRisk::Intermediate': '32353'    '68200'
STAGE_HIGH_LIFETIME_RISK_TAG = "32352"
STAGE_INTERMEDIATE_LIFETIME_RISK_TAG = "32353"
STAGE_AVERAGE_LIFETIME_RISK_TAG = "32351"
PROD_HIGH_LIFETIME_RISK_TAG = "68186"
PROD_INTERMEDIATE_LIFETIME_RISK_TAG = "68200"
PROD_AVERAGE_LIFETIME_RISK_TAG = "68205"

def get_alr_tag_id(environment: str, alr: float) -> str:
    if environment == "STAGE":
        if alr >= 20:
            return STAGE_HIGH_LIFETIME_RISK_TAG
        if alr >= 15:
            return STAGE_INTERMEDIATE_LIFETIME_RISK_TAG
        else:
            return STAGE_AVERAGE_LIFETIME_RISK_TAG

    elif environment == "PROD":
        if alr >= 20:
            return PROD_HIGH_LIFETIME_RISK_TAG
        if alr >= 15:
            return PROD_INTERMEDIATE_LIFETIME_RISK_TAG
        else:
            return PROD_AVERAGE_LIFETIME_RISK_TAG
    else:
        raise ValueError(f"Invalid environment: {environment}")

# 'Result::BIRADS::0':                    '32343'    '68191'
# 'Result::BIRADS::1':                    '32344'    '68201'
# 'Result::BIRADS::2':                    '32345'    '68189'
# 'Result::BIRADS::3':                    '32346'    '68206'
# 'Result::BIRADS::4':                    '32347'    '68197'
# 'Result::BIRADS::5':                    '32348'    '68185'
STAGE_BIRAD_0_TAG = "32343"
STAGE_BIRAD_1_TAG = "32344"
STAGE_BIRAD_2_TAG = "32345"
STAGE_BIRAD_3_TAG = "32346"
STAGE_BIRAD_4_TAG = "32347"
STAGE_BIRAD_5_TAG = "32348"
PROD_BIRAD_0_TAG = "68191"
PROD_BIRAD_1_TAG = "68201"
PROD_BIRAD_2_TAG = "68189"
PROD_BIRAD_3_TAG = "68206"
PROD_BIRAD_4_TAG = "68197"
PROD_BIRAD_5_TAG = "68185"

def get_birad_tag_id(environment: str, birad: str) -> str:
    if environment == "STAGE":
        if birad == "0":
            return STAGE_BIRAD_0_TAG
        elif birad == "1":
            return STAGE_BIRAD_1_TAG
        elif birad == "2":
            return STAGE_BIRAD_2_TAG
        elif birad == "3":
            return STAGE_BIRAD_3_TAG
        elif birad == "4":
            return STAGE_BIRAD_4_TAG
        elif birad == "5":
            return STAGE_BIRAD_5_TAG
        else:
            raise ValueError(f"Invalid BIRAD: {birad}")
    elif environment == "PROD":
        if birad == "0":
            return PROD_BIRAD_0_TAG
        elif birad == "1":
            return PROD_BIRAD_1_TAG
        elif birad == "2":
            return PROD_BIRAD_2_TAG
        elif birad == "3":
            return PROD_BIRAD_3_TAG
        elif birad == "4":
            return PROD_BIRAD_4_TAG
        elif birad == "5":
            return PROD_BIRAD_5_TAG
        else:
            raise ValueError(f"Invalid BIRAD: {birad}")
    else:
        raise ValueError(f"Invalid environment: {environment}")

# 'Result::BAC::Absent':                  '32341'    '68192'
# 'Result::BAC::Present':                 '32342'    '68184'
STAGE_BAC_DETECTED_TAG = "32342"
STAGE_BAC_NOT_DETECTED_TAG = "32341"
PROD_BAC_DETECTED_TAG = "68184"
PROD_BAC_NOT_DETECTED_TAG = "68192"

def get_bac_tag_id(environment: str, bac_status: str) -> str:
    if environment == "STAGE":
        if bac_status == "Detected":
            return STAGE_BAC_DETECTED_TAG
        else:
            return STAGE_BAC_NOT_DETECTED_TAG
    elif environment == "PROD":
        if bac_status == "Detected":
            return PROD_BAC_DETECTED_TAG
        else:
            return PROD_BAC_NOT_DETECTED_TAG
    else:
        raise ValueError(f"Invalid environment: {environment}")
