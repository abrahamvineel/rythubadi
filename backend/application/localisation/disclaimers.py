from domain.data_precision import DataPrecision
from domain.language import Language

DISCLAIMERS = {
        DataPrecision.FIELD: {
            Language.EN: "Weather data is field-level (GPS precision).",
            Language.FR: "Les données météo sont au niveau du champ (précision GPS).",
            Language.TE: "వాతావరణ డేటా పొలం స్థాయి (GPS ఖచ్చితత్వం)"
        },
        DataPrecision.DISTRICT: {
            Language.EN: "Weather data is district-level approximation.",
            Language.FR: "Les données météo sont une approximation au niveau du district.",
            Language.TE: "వాతావరణ డేటా జిల్లా స్థాయి అంచనా."
        },
        DataPrecision.PROVINCE: {
            Language.EN: "Weather data is province-level approximation.",
            Language.FR: "Les données météo sont une approximation au niveau provincial.",
            Language.TE: "వాతావరణ డేటా రాష్ట్ర స్థాయి అంచనా."
        },
}

def get_disclaimer(precision: DataPrecision, language: Language) -> str:
    return DISCLAIMERS.get(precision, {}).get(language) \
            or DISCLAIMERS.get(precision, {}).get(Language.EN) 
