from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from app.ai.llm import generate_answer
from app.rag.knowledge_base import ServiceData, find_service
from app.rag.retriever import retrieve_context


router = APIRouter()


# =========================================================
# REQUEST / RESPONSE
# =========================================================

class ConversationTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "English"
    conversation_context: list[ConversationTurn] = Field(
        default_factory=list
    )


class ChatResponse(BaseModel):
    answer: str
    service: Optional[ServiceData] = None
    needs_more_info: bool = False
    follow_up_questions: list[str] = Field(
        default_factory=list
    )


# =========================================================
# GREETING
# =========================================================

def is_greeting(message: str) -> bool:
    text = " ".join(
        message.lower().strip().split()
    )

    return text in {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "namaste",
        "namaskar",
        "good morning",
        "good afternoon",
        "good evening",
    }


def greeting_response(language: str) -> ChatResponse:
    lang = (language or "English").lower()

    if lang in {"telugu", "te"}:
        return ChatResponse(
            answer=(
                "హలో! 👋 నేను SevaMitra. ప్రభుత్వ సేవలు, "
                "సర్టిఫికెట్లు, స్కాలర్‌షిప్‌లు, పథకాలు, "
                "ఉద్యోగాలు మరియు పరీక్షల గురించి సహాయం చేస్తాను."
            )
        )

    if lang in {"hindi", "hi"}:
        return ChatResponse(
            answer=(
                "नमस्ते! 👋 मैं SevaMitra हूँ। मैं सरकारी सेवाओं, "
                "प्रमाणपत्रों, स्कॉलरशिप, योजनाओं, नौकरियों और "
                "परीक्षाओं में मदद कर सकता हूँ।"
            )
        )

    return ChatResponse(
        answer=(
            "Hello! 👋 I’m SevaMitra. "
            "I can help with government services, certificates, "
            "scholarships, schemes, jobs and examinations."
        )
    )


# =========================================================
# NORMALIZE
# =========================================================

def normalize(message: str) -> str:
    return " ".join(
        message.lower().strip().split()
    )


# =========================================================
# DIGILOCKER CONTINUATION
# =========================================================

DOCUMENT_NAMES = [
    "income certificate",
    "caste certificate",
    "community certificate",
    "birth certificate",
    "death certificate",
    "marks memo",
    "marksheet",
    "degree certificate",
    "driving licence",
    "driving license",
    "pan card",
    "aadhaar",
    "voter id",
]


def extract_document_name(message: str) -> Optional[str]:
    text = normalize(message)

    for document in DOCUMENT_NAMES:
        if document in text:
            return document

    return None


def is_digilocker_download_followup(
    message: str,
    history: list[ConversationTurn],
) -> bool:

    current = normalize(message)

    document_name = extract_document_name(current)

    if not document_name:
        return False

    download_words = [
        "download",
        "downloaded",
        "how can i download",
        "how can we download",
        "how to download",
        "get",
        "get the document",
        "collect",
        "save",
    ]

    digilocker_words = [
        "digilocker",
        "digi locker",
    ]

    # Case 1:
    # Current message itself clearly mentions DigiLocker + download
    current_has_digilocker = any(
        word in current
        for word in digilocker_words
    )

    current_has_download = any(
        word in current
        for word in download_words
    )

    if current_has_digilocker and current_has_download:
        return True

    # Case 2:
    # Current message is a continuation of earlier DigiLocker conversation
    if not history:
        return False

    previous_text = " ".join(
        normalize(turn.content)
        for turn in history[-8:]
    )

    previous_has_digilocker = any(
        word in previous_text
        for word in digilocker_words
    )

    previous_has_download = any(
        word in previous_text
        for word in download_words
    )

    return (
        previous_has_digilocker
        and previous_has_download
    )


def digilocker_download_response(
    document_name: str,
    language: str,
) -> ChatResponse:

    display_name = document_name.title()
    lang = (language or "English").lower()

    if lang in {"telugu", "te"}:
        return ChatResponse(
            answer=(
                f"అవును — మీరు DigiLocker నుండి మీ "
                f"{display_name} download చేయాలనుకుంటున్నారు.\n\n"
                "1. Official DigiLocker website లేదా mobile app open చేయండి.\n"
                "2. మీ existing account తో login అవ్వండి.\n"
                "3. Issued Documents section open చేయండి.\n"
                f"4. {display_name} కోసం search చేయండి.\n"
                "5. Certificate అందుబాటులో ఉంటే open చేసి "
                "Download లేదా Share option ఎంచుకోండి.\n\n"
                "Certificate DigiLocker లో కనిపించకపోతే, "
                "దాన్ని issue చేసిన authority యొక్క official portal లో "
                "download option ఉండవచ్చు."
            ),
            service=None,
            needs_more_info=False,
            follow_up_questions=[],
        )

    if lang in {"hindi", "hi"}:
        return ChatResponse(
            answer=(
                f"हाँ — आप DigiLocker से अपना {display_name} "
                "डाउनलोड करना चाहते हैं।\n\n"
                "1. Official DigiLocker website या mobile app खोलें।\n"
                "2. अपने existing account से login करें।\n"
                "3. Issued Documents section खोलें।\n"
                f"4. {display_name} खोजें।\n"
                "5. Certificate उपलब्ध हो तो उसे खोलें और "
                "Download या Share option चुनें।\n\n"
                "अगर certificate DigiLocker में उपलब्ध नहीं है, "
                "तो उसे जारी करने वाली authority के official portal "
                "पर download option हो सकता है।"
            ),
            service=None,
            needs_more_info=False,
            follow_up_questions=[],
        )

    return ChatResponse(
        answer=(
            f"Yes — you want to download your {display_name} "
            "from DigiLocker.\n\n"
            "1. Open the official DigiLocker website or mobile app.\n"
            "2. Log in to your existing account.\n"
            "3. Open the Issued Documents section.\n"
            f"4. Search for your {display_name}.\n"
            "5. If the certificate is available, open it and select "
            "Download or Share.\n\n"
            "If the certificate is not available in DigiLocker, "
            "the issuing authority may provide a separate download "
            "option on its official portal."
        ),
        service=None,
        needs_more_info=False,
        follow_up_questions=[],
    )


# =========================================================
# SECTOR DETECTION
# =========================================================

def detect_sector(message: str) -> str:
    text = normalize(message)

    if any(
        x in text
        for x in [
            "scholarship",
            "scholarships",
            "nsp",
            "fellowship",
        ]
    ):
        return "scholarship"

    if any(
        x in text
        for x in [
            "upsc",
            "ssc",
            "rrb",
            "ibps",
            "nta",
            "neet",
            "jee",
            "cuet",
            "government exam",
            "government job",
            "govt job",
            "railway job",
            "bank job",
            "police job",
        ]
    ):
        return "exam"

    if any(
        x in text
        for x in [
            "driving licence",
            "driving license",
            "learner licence",
            "learner license",
            "rto",
            "vehicle registration",
            "rc book",
        ]
    ):
        return "driving"

    if any(
        x in text
        for x in [
            "aadhaar",
            "aadhar",
            "pan card",
            "voter id",
            "passport",
            "digilocker",
            "digi locker",
        ]
    ):
        return "identity"

    if any(
        x in text
        for x in [
            "income certificate",
            "caste certificate",
            "community certificate",
            "ews certificate",
            "residence certificate",
            "domicile certificate",
            "birth certificate",
            "death certificate",
            "marriage certificate",
            "disability certificate",
        ]
    ):
        return "certificate"

    if any(
        x in text
        for x in [
            "farmer",
            "farmers",
            "pm kisan",
            "pm-kisan",
            "crop insurance",
            "agriculture",
            "farmer scheme",
            "kisan credit",
            "farming",
        ]
    ):
        return "agriculture"

    if any(
        x in text
        for x in [
            "pension",
            "old age pension",
            "widow pension",
            "disability pension",
            "ration card",
            "welfare scheme",
            "social welfare",
            "housing scheme",
        ]
    ):
        return "welfare"

    if any(
        x in text
        for x in [
            "ayushman",
            "pm-jay",
            "pmjay",
            "health scheme",
            "health card",
            "government hospital",
        ]
    ):
        return "health"

    if any(
        x in text
        for x in [
            "income tax",
            "itr",
            "gst",
            "udyam",
            "msme",
            "startup india",
            "epfo",
            "pf",
            "uan",
            "business registration",
        ]
    ):
        return "business"

    if any(
        x in text
        for x in [
            "municipal",
            "municipality",
            "property tax",
            "water connection",
            "building permission",
            "local government",
            "civic",
        ]
    ):
        return "civic"

    return "general"


# =========================================================
# FOLLOW-UP QUESTIONS
# =========================================================

SECTOR_QUESTIONS = {
    "scholarship": [
        "Which State/UT are you from?",
        "What are you studying? (For example: Class 12, Diploma, B.Tech, Degree, PG)",
    ],
    "exam": [
        "Which exam or job are you interested in?",
        "What is your highest qualification and your age?",
    ],
    "driving": [
        "Which State/UT are you applying in?",
        "Which vehicle class do you need the licence for, and do you already have a Learner's Licence?",
    ],
    "identity": [
        "Which document do you need? (Aadhaar / PAN / Voter ID / Passport / DigiLocker)",
        "What do you want to do? (New / Update / Correction / Download / Status)",
    ],
    "certificate": [
        "Which certificate do you need?",
        "Which State/UT are you applying in, and what is the purpose?",
    ],
    "agriculture": [
        "Which State/UT are you from?",
        "Are you a farmer, tenant farmer or agricultural worker, and what crop/activity is involved?",
    ],
    "welfare": [
        "Which State/UT are you from?",
        "Which benefit do you need? (Pension / Ration / Housing / Welfare / Other)",
    ],
    "health": [
        "Which State/UT are you from?",
        "Which health scheme or service are you asking about?",
    ],
    "business": [
        "Which service do you need? (Udyam / GST / Tax / Startup / PF / Business)",
        "Are you an individual, employee, employer or business owner?",
    ],
    "civic": [
        "Which State/UT and city/municipality are you in?",
        "Which civic service do you need?",
    ],
}


def followup_response(
    sector: str,
    language: str,
) -> ChatResponse:

    questions = SECTOR_QUESTIONS.get(
        sector,
        [
            "Which government service or scheme do you need?",
            "Which State/UT are you from?",
        ],
    )

    lang = (language or "English").lower()

    if lang in {"telugu", "te"}:
        labels = "\n".join(
            f"{i + 1}. {q}"
            for i, q in enumerate(questions)
        )

        return ChatResponse(
            answer=(
                "సరైన information ఇవ్వడానికి ఈ రెండు వివరాలు చెప్పండి:\n\n"
                + labels
            ),
            needs_more_info=True,
            follow_up_questions=questions,
        )

    if lang in {"hindi", "hi"}:
        labels = "\n".join(
            f"{i + 1}. {q}"
            for i, q in enumerate(questions)
        )

        return ChatResponse(
            answer=(
                "सही जानकारी देने के लिए ये दो विवरण बताएं:\n\n"
                + labels
            ),
            needs_more_info=True,
            follow_up_questions=questions,
        )

    labels = "\n".join(
        f"{i + 1}. {q}"
        for i, q in enumerate(questions)
    )

    return ChatResponse(
        answer=(
            "To give you a more accurate answer, please tell me:\n\n"
            + labels
        ),
        needs_more_info=True,
        follow_up_questions=questions,
    )


# =========================================================
# CONVERSATION CONTEXT
# =========================================================

def build_conversation_context(
    current_message: str,
    history: list[ConversationTurn],
) -> str:

    if not history:
        return current_message

    recent = history[-8:]
    lines = []

    for turn in recent:
        content = turn.content.strip()

        if content:
            lines.append(
                f"{turn.role}: {content}"
            )

    if not lines:
        return current_message

    return (
        "Previous conversation:\n"
        + "\n".join(lines)
        + "\n\nCurrent user message:\n"
        + current_message
    )


# =========================================================
# MAIN CHAT
# =========================================================

@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:

        message = request.message.strip()

        if not message:
            return ChatResponse(
                answer="Please enter a question."
            )

        # -------------------------------------------------
        # GREETING
        # -------------------------------------------------

        if is_greeting(message):
            return greeting_response(
                request.language or "English"
            )

        # -------------------------------------------------
        # DIGILOCKER CONTINUATION
        #
        # IMPORTANT:
        # This must happen BEFORE sector detection and RAG.
        # Otherwise "income certificate" can trigger the
        # generic Income Certificate knowledge card.
        # -------------------------------------------------

        if is_digilocker_download_followup(
            message,
            request.conversation_context,
        ):

            document_name = extract_document_name(message)

            if document_name:
                return digilocker_download_response(
                    document_name=document_name,
                    language=request.language or "English",
                )

        # -------------------------------------------------
        # SECTOR
        # -------------------------------------------------

        sector = detect_sector(message)

        lower = normalize(message)

        # -------------------------------------------------
        # PERSONALIZED / ELIGIBILITY QUESTIONS
        # -------------------------------------------------

        recommendation_words = [
            "which",
            "can i apply",
            "am i eligible",
            "eligible",
            "suitable",
            "recommend",
            "available for me",
            "which scheme",
            "which schemes",
            "which scholarship",
            "which scholarships",
            "which exam",
            "which exams",
            "which job",
            "which jobs",
        ]

        wants_personal_match = any(
            word in lower
            for word in recommendation_words
        )

        if (
            wants_personal_match
            and sector != "general"
            and not request.conversation_context
        ):
            return followup_response(
                sector=sector,
                language=request.language or "English",
            )

        # -------------------------------------------------
        # RAG
        # -------------------------------------------------

        service = find_service(message)

        context_parts = []

        if service:

            try:
                context_parts.append(
                    "(Curated knowledge base): "
                    + service.model_dump_json()
                )

            except AttributeError:

                context_parts.append(
                    "(Curated knowledge base): "
                    + service.json()
                )

        rag_context = retrieve_context(message)

        if rag_context:
            context_parts.append(
                rag_context
            )

        context = "\n\n---\n\n".join(
            context_parts
        )

        # -------------------------------------------------
        # CONVERSATION CONTEXT
        # -------------------------------------------------

        effective_question = build_conversation_context(
            current_message=message,
            history=request.conversation_context,
        )

        # -------------------------------------------------
        # GROQ
        # -------------------------------------------------

        result = generate_answer(
            question=effective_question,
            context=context,
            language=request.language or "English",
        )

        return ChatResponse(
            answer=result.get(
                "answer",
                ""
            ),
            service=result.get(
                "service"
            ),
            needs_more_info=bool(
                result.get(
                    "needs_more_info",
                    False
                )
            ),
            follow_up_questions=result.get(
                "follow_up_questions",
                [],
            ),
        )

    except Exception as exc:

        print(
            "CHAT ERROR:",
            repr(exc)
        )

        return ChatResponse(
            answer=(
                "I couldn't process this request right now. "
                "Please try again."
            ),
            service=None,
            needs_more_info=False,
            follow_up_questions=[],
        )