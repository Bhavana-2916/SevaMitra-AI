from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
import os

from app.ai.llm import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "English"


class ServiceData(BaseModel):
    serviceName: str
    quickAnswer: str
    eligibility: List[str]
    documents: List[str]
    steps: List[str]
    fees: Optional[str] = None
    processingTime: Optional[str] = None
    officialUrl: Optional[str] = None
    source: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    service: Optional[ServiceData] = None


# Known service data used as CONTEXT for the LLM (a simple stand-in for
# the future RAG/vector-DB pipeline in app/rag/). The LLM is instructed
# to answer only from this context, so it stays grounded instead of
# hallucinating eligibility rules, fees, etc.
KNOWLEDGE_BASE = {
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
    "driving licence": ServiceData(
        serviceName="Driving Licence",
        quickAnswer="A driving licence authorizes a person to legally drive motor vehicles on Indian roads.",
        eligibility=[
            "Minimum age 18 for most vehicle categories (16 with guardian consent for gearless two-wheelers up to 50cc).",
            "Must pass a learner's test followed by a driving test.",
        ],
        documents=["Age Proof", "Address Proof", "Passport-size Photographs", "Learner's Licence"],
        steps=[
            "Apply for a Learner's Licence (LL) on the Parivahan portal.",
            "Pass the online learner's test.",
            "Practice driving for at least 30 days.",
            "Book a slot for the permanent licence driving test.",
            "Pass the test and receive your Driving Licence.",
        ],
        fees="As applicable on the Parivahan portal",
        processingTime="Varies by state RTO",
        officialUrl="https://parivahan.gov.in/",
        source="Official Government Information",
    ),
    "aadhaar": ServiceData(
        serviceName="Aadhaar Card",
        quickAnswer="Aadhaar is a 12-digit unique identity number issued to Indian residents, used for identity and address verification.",
        eligibility=["Any resident of India, including children (with guardian details)."],
        documents=["Proof of Identity", "Proof of Address", "Proof of Date of Birth"],
        steps=[
            "Locate the nearest Aadhaar Enrolment Centre.",
            "Fill the enrolment form and submit documents.",
            "Complete biometric capture (fingerprints, iris, photo).",
            "Note the enrolment ID (EID) for tracking.",
            "Download the e-Aadhaar once generated.",
        ],
        fees="Free for new enrolment",
        processingTime="Usually 90 days for the physical card by post",
        officialUrl="https://uidai.gov.in/",
        source="Official Government Information",
    ),
    "pm-kisan": ServiceData(
        serviceName="PM-KISAN Scheme",
        quickAnswer="PM-KISAN provides income support of ₹6,000 per year to eligible farmer families, paid in three instalments.",
        eligibility=[
            "Small and marginal farmer families with cultivable landholding.",
            "Certain categories (institutional landholders, high-income individuals) are excluded.",
        ],
        documents=["Aadhaar Card", "Land Ownership Documents", "Bank Account Details"],
        steps=[
            "Visit the PM-KISAN portal or nearest Common Service Centre.",
            "Register with Aadhaar and land records.",
            "Get your application verified by local revenue officials.",
            "Track status using your registration number on the portal.",
        ],
        fees="Free",
        processingTime="Depends on state verification process",
        officialUrl="https://pmkisan.gov.in/",
        source="Official Government Information",
    ),
    "scholarship": ServiceData(
        serviceName="National Scholarship",
        quickAnswer="National Scholarships provide financial assistance to eligible students for their education based on merit and/or means.",
        eligibility=[
            "Indian student enrolled in a recognized educational institution.",
            "Family income within the scheme's specified limit.",
        ],
        documents=["Aadhaar Card", "Income Certificate", "Bonafide/Admission Certificate", "Bank Account Details"],
        steps=[
            "Register on the National Scholarship Portal (NSP).",
            "Fill in personal, academic, and bank details.",
            "Upload required documents.",
            "Submit and track application status online.",
        ],
        fees="Free to apply",
        processingTime="Varies by scheme and state",
        officialUrl="https://scholarships.gov.in/",
        source="Official Government Information",
    ),
}


def find_service(message: str) -> Optional[ServiceData]:
    text = message.lower()
    for keyword, service in KNOWLEDGE_BASE.items():
        if keyword in text:
            return service
    return None


def fallback_response(service: Optional[ServiceData]) -> ChatResponse:
    """Used when no ANTHROPIC_API_KEY is set, so the app still works."""
    if service:
        return ChatResponse(
            answer="Here is the information I found for your government service query.",
            service=service,
        )
    return ChatResponse(
        answer=(
            "I don't have specific information on that yet. "
            "Try asking about an Income Certificate or PAN Card for now — "
            "more services will be added as the knowledge base grows."
        ),
        service=None,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    service = find_service(request.message)

    # No API key configured yet -> use the plain hardcoded response
    # so the app keeps working while you're setting up the key.
    if not os.getenv("GROQ_API_KEY"):
        print("LLM ERROR: GROQ_API_KEY not found in environment")
        return fallback_response(service)

    context = service.model_dump_json() if service else ""

    try:
        result = generate_answer(
            question=request.message,
            context=context,
            language=request.language or "English",
        )
        return ChatResponse(**result)
    except Exception as e:
        print("LLM ERROR:", repr(e))
        # If the LLM call fails for any reason, don't break the app —
        # fall back to the plain hardcoded response.
        return fallback_response(service)
