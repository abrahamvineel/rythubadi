from fastapi import APIRouter, Depends
from presentation.schemas.diagnose_request import DiagnoseRequest
from presentation.schemas.diagnose_response import DiagnoseResponse
from presentation.dependencies.auth import verify_clerk_jwt
from application.agents.crop_diagnosis_state import CropDiagnosisState
from domain.regional_context import RegionalContext
from bootstrap import build_services
import uuid

router = APIRouter()

@router.post("/diagnose", status_code=200)
def diagnose_router(request: DiagnoseRequest,
                    token = Depends(verify_clerk_jwt)):
    crop_diagnosis_agent = _build_crop_diagnosis_agent(request)
    result = build_services().crop_diagnosis_graph.invoke(crop_diagnosis_agent)
    return DiagnoseResponse(llm_diagnosis=result["llm_diagnosis"], confirmation_id=result["confirmation_id"])

def _build_crop_diagnosis_agent(request: DiagnoseRequest) -> CropDiagnosisState:
    return CropDiagnosisState(image_url=request.image_url,
                              crop_type=request.crop_type, 
                              region=RegionalContext(request.province_state),
                              language=request.language,
                              producer_id=request.producer_id,
                              weather_context=None,
                              disease_candidate=None,
                              corpus_matches=None,
                              llm_diagnosis=None,
                              confirmation_id=None,
                              pending_confirmation=False,
                              tools_called=[])
    