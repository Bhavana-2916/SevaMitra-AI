import json
from typing import Optional

from pydantic import BaseModel


class ServiceData(BaseModel):
    serviceName: str
    quickAnswer: str
    eligibility: list[str]
    documents: list[str]
    steps: list[str]
    fees: Optional[str] = None
    processingTime: Optional[str] = None
    officialUrl: Optional[str] = None
    source: Optional[str] = None


# Keep this curated data as the trusted seed and fallback. The ingestion
# command also converts it into searchable chunks for the RAG pipeline.
KNOWLEDGE_BASE: dict[str, ServiceData] = {
    "income certificate": ServiceData(
        serviceName="Income Certificate",
        quickAnswer="An income certificate verifies a person's annual family income for various government services and benefits.",
        eligibility=[
            "Applicant should be a resident of the concerned state.",
            "Income details should be supported by valid documents.",
        ],
        documents=["Aadhaar Card", "Address Proof", "Income-related documents"],
        steps=[
            "Visit the official government service portal.",
            "Select the Income Certificate service.",
            "Fill in the application form.",
            "Upload the required documents.",
            "Submit the application.",
        ],
        fees="As applicable on the official portal",
        processingTime="Depends on the concerned authority",
        officialUrl="https://www.india.gov.in/",
        source="Official Government Information",
    ),
    "pan card": ServiceData(
        serviceName="PAN Card",
        quickAnswer="A PAN (Permanent Account Number) card is required for financial transactions and tax purposes in India.",
        eligibility=["Any Indian citizen or entity required to pay tax."],
        documents=["Identity Proof", "Address Proof", "Date of Birth Proof", "Photograph"],
        steps=[
            "Visit the NSDL or UTIITSL portal.",
            "Fill Form 49A (Indian citizens).",
            "Upload documents and photograph.",
            "Pay the applicable fee.",
            "Submit and note the acknowledgement number.",
        ],
        fees="Approx. ₹100-110 for Indian communication address",
        processingTime="15-20 working days",
        officialUrl="https://www.onlineservices.nsdl.com/",
        source="Official Government Information",
    ),
}


def find_service(message: str) -> Optional[ServiceData]:
    text = message.lower()
    for keyword, service in KNOWLEDGE_BASE.items():
        if keyword in text:
            return service
    return None


def manual_documents() -> list[dict[str, str]]:
    """Expose curated entries to the same chunk/embed pipeline as PDFs."""
    return [
        {
            "filename": f"knowledge-base/{keyword.replace(' ', '-')}.json",
            "text": json.dumps(service.model_dump(), ensure_ascii=False, indent=2),
        }
        for keyword, service in KNOWLEDGE_BASE.items()
    ]