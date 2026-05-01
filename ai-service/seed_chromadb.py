import chromadb
import os

# Initialize ChromaDB with persistent storage
client = chromadb.PersistentClient(path="./chroma_data")

# Create or get collection
collection = client.get_or_create_collection(
    name="regulatory_knowledge",
    metadata={"description": "Regulatory compliance domain knowledge"}
)

# 10 domain knowledge documents
documents = [
    {
        "id": "doc001",
        "text": "HIPAA violations can result in fines ranging from $100 to $50,000 per violation, with a maximum of $1.9 million per year for identical violations. The four categories are: unknowing violation, reasonable cause, willful neglect corrected, and willful neglect not corrected. HHS Office for Civil Rights enforces HIPAA rules.",
        "metadata": {"topic": "HIPAA", "industry": "Healthcare", "type": "penalty"}
    },
    {
        "id": "doc002",
        "text": "GDPR penalties are divided into two tiers. Tier 1 fines up to 10 million euros or 2% of global annual turnover for less severe violations. Tier 2 fines up to 20 million euros or 4% of global annual turnover for more serious violations including breaches of basic principles and data subject rights.",
        "metadata": {"topic": "GDPR", "industry": "Technology", "type": "penalty"}
    },
    {
        "id": "doc003",
        "text": "OSHA violations are categorized as: Other-than-Serious up to $16,550 per violation, Serious up to $16,550 per violation, Willful or Repeated up to $165,514 per violation, and Failure to Abate up to $16,550 per day beyond the abatement date. Employers must maintain safe working conditions.",
        "metadata": {"topic": "OSHA", "industry": "Manufacturing", "type": "penalty"}
    },
    {
        "id": "doc004",
        "text": "SEC violations for insider trading can result in civil penalties up to three times the profit gained or loss avoided. Criminal penalties include up to 20 years imprisonment and fines up to $5 million for individuals and $25 million for firms. The SEC enforces securities laws under the Securities Exchange Act of 1934.",
        "metadata": {"topic": "SEC", "industry": "Finance", "type": "penalty"}
    },
    {
        "id": "doc005",
        "text": "SOX compliance violations under Section 302 and 906 can result in fines up to $1 million and 10 years imprisonment for certifying false financial reports. Willful violations carry fines up to $5 million and 20 years imprisonment. CEOs and CFOs are personally liable for financial statement accuracy.",
        "metadata": {"topic": "SOX", "industry": "Finance", "type": "penalty"}
    },
    {
        "id": "doc006",
        "text": "PCI DSS non-compliance fines range from $5,000 to $100,000 per month depending on violation severity and merchant level. After a data breach, fines can increase significantly. Payment card brands like Visa and Mastercard impose these fines on acquiring banks who pass them to merchants.",
        "metadata": {"topic": "PCI DSS", "industry": "Retail", "type": "penalty"}
    },
    {
        "id": "doc007",
        "text": "AML violations under the Bank Secrecy Act can result in civil penalties up to $1 million per day or the amount of the transaction, whichever is greater. Criminal penalties include up to 20 years imprisonment. Financial institutions must implement Know Your Customer procedures and file Suspicious Activity Reports.",
        "metadata": {"topic": "AML", "industry": "Banking", "type": "penalty"}
    },
    {
        "id": "doc008",
        "text": "CCPA violations carry civil penalties of $2,500 per unintentional violation and $7,500 per intentional violation. Consumers can seek statutory damages between $100 and $750 per incident in class action lawsuits. Businesses must provide privacy notices and honor consumer rights to access and delete data.",
        "metadata": {"topic": "CCPA", "industry": "Technology", "type": "penalty"}
    },
    {
        "id": "doc009",
        "text": "FDA regulatory violations for pharmaceutical companies can result in warning letters, consent decrees, product seizures, and injunctions. Financial penalties vary widely with some cases resulting in settlements over $1 billion. Good Manufacturing Practice violations are among the most common findings.",
        "metadata": {"topic": "FDA", "industry": "Pharmaceutical", "type": "penalty"}
    },
    {
        "id": "doc010",
        "text": "FINRA violations for broker-dealers can result in fines from $5,000 to millions of dollars depending on severity. Common violations include failure to supervise, unsuitable recommendations, and market manipulation. FINRA can also suspend or bar individuals from the securities industry permanently.",
        "metadata": {"topic": "FINRA", "industry": "Finance", "type": "penalty"}
    }
]

# Add documents to ChromaDB
print("Seeding ChromaDB with 10 regulatory knowledge documents...\n")

for doc in documents:
    collection.upsert(
        ids=[doc["id"]],
        documents=[doc["text"]],
        metadatas=[doc["metadata"]]
    )
    print(f"✅ Added: {doc['id']} — {doc['metadata']['topic']}")

print(f"\n✅ ChromaDB seeded successfully!")
print(f"Total documents in collection: {collection.count()}")