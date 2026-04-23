import hashlib
import json
import os
import uuid
from pathlib import Path

import psycopg2
from openai import OpenAI

SCHEMES = [
    {
        "scheme_name": "PM-KISAN",
        "country": "India",
        "province": None,
        "source_url": "https://pmkisan.gov.in",
        "content": (
            "PM-KISAN provides \u20b96,000 per year in three equal installments of \u20b92,000 "
            "to small and marginal farmer families with combined landholding up to 2 hectares. "
            "Eligibility requires ownership of cultivable land and Aadhaar-linked bank account. "
            "Tenant farmers and sharecroppers are not eligible under the central scheme."
        ),
    },
    {
        "scheme_name": "PMFBY",
        "country": "India",
        "province": None,
        "source_url": "https://pmfby.gov.in",
        "content": (
            "Pradhan Mantri Fasal Bima Yojana provides crop insurance at premium rates of 2% "
            "for Kharif crops, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops. "
            "The remaining premium is shared equally between the central and state governments. "
            "Coverage includes prevented sowing, mid-season adversity, post-harvest losses, and localized calamities."
        ),
    },
    {
        "scheme_name": "Rythu Bharosa",
        "country": "India",
        "province": "Andhra Pradesh",
        "source_url": "https://apagrisnet.gov.in/rythubharosa",
        "content": (
            "Rythu Bharosa provides \u20b913,500 per year to farmer families in Andhra Pradesh "
            "in two installments: \u20b97,500 before Kharif and \u20b96,000 before Rabi season. "
            "Eligible farmers must own agricultural land in Andhra Pradesh and be registered in "
            "the state\u2019s farmer registry. Tenant farmers registered under the Andhra Pradesh "
            "Rights in Land and Pattadar Passbooks Act are also eligible."
        ),
    },
    {
        "scheme_name": "AgriStability",
        "country": "Canada",
        "province": None,
        "source_url": "https://agriculture.canada.ca/en/agricultural-programs-and-services/agristability",
        "content": (
            "AgriStability compensates Canadian farmers when their production margin drops more than "
            "30% below their historical reference margin. The program covers most crops, livestock, "
            "and other commodities. Farmers must enroll by the deadline and pay a participation fee; "
            "the benefit is calculated as 70% of the margin loss below the 30% threshold."
        ),
    },
    {
        "scheme_name": "AgriInvest",
        "country": "Canada",
        "province": None,
        "source_url": "https://agriculture.canada.ca/en/agricultural-programs-and-services/agriinvest",
        "content": (
            "AgriInvest is a savings account program where governments match farmer deposits up to "
            "1% of Allowable Net Sales each year. Farmers can withdraw funds at any time to cover "
            "income declines or make investments. Both the federal and provincial/territorial "
            "governments contribute to the matching deposit."
        ),
    },
]


class CorpusIntegrityError(Exception):
    pass


def _load_approved_sources() -> dict[str, str]:
    path = Path(__file__).parent.parent / "docs" / "approved_sources.json"
    entries = json.loads(path.read_text())
    return {entry["scheme_name"]: entry["sha256"] for entry in entries}


def _verify_hash(scheme_name: str, content: str, approved: dict[str, str]) -> None:
    actual = hashlib.sha256(content.encode()).hexdigest()
    expected = approved.get(scheme_name)
    if expected is None:
        raise CorpusIntegrityError(f"{scheme_name!r} not found in approved_sources.json")
    if actual != expected:
        raise CorpusIntegrityError(f"Hash mismatch for {scheme_name!r}: content has been modified")


def _embed(client: OpenAI, text: str) -> list[float]:
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def _insert(conn, scheme: dict, embedding: list[float]) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO rag_documents
                (id, scheme_name, content, country, province, source_url, content_hash, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (
                str(uuid.uuid4()),
                scheme["scheme_name"],
                scheme["content"],
                scheme["country"],
                scheme["province"],
                scheme["source_url"],
                hashlib.sha256(scheme["content"].encode()).hexdigest(),
                str(embedding),
            ),
        )
    conn.commit()


def main() -> None:
    approved = _load_approved_sources()
    openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    conn = psycopg2.connect(dsn=os.environ["DATABASE_URL"])

    try:
        for scheme in SCHEMES:
            _verify_hash(scheme["scheme_name"], scheme["content"], approved)
            embedding = _embed(openai_client, scheme["content"])
            _insert(conn, scheme, embedding)
            print(f"Ingested: {scheme['scheme_name']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
