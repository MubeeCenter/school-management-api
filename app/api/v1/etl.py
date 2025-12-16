# app/api/v1/etl.py

from fastapi import APIRouter, Query
from app.services.etl_service import etl_service

router = APIRouter(prefix="/etl", tags=["etl"])

@router.post("/run")
def run_etl(clean: bool = Query(False, description="Clean MongoDB fact table before loading")):
    """
    Trigger the internal SQL → MongoDB ETL process.
    """
    total = etl_service.run_full(clean=clean)
    return {
        "message": "Internal ETL completed",
        "records_loaded": total,
        "clean": clean
    }
