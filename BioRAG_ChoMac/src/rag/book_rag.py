"""
Book-level RAG:
- Đọc dữ liệu văn bản từ ChromaDB
- Tìm kiếm theo cụm từ và từ nguyên vẹn
- Gửi ngữ cảnh liên quan cho Gemini
"""

import asyncio
import re
import unicodedata

import chromadb

from src.config import PERSIST_DIR, TEXT_COLLECTION_NAME


STOP_WORDS = {
    "la", "gi", "tai", "sao", "nhu", "the", "nao",
    "hay", "cho", "biet", "duoc", "mot", "cac",
    "va", "cua", "trong", "voi", "ve", "em",
    "toi", "chung", "ta"
}


def no_accent(text: str) -> str:
    """Loại bỏ dấu tiếng Việt."""
    normalized = unicodedata.normalize("NFD", text)

    return "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )


def normalize_text(text: str) -> str:
    """Chuyển chữ thường, bỏ dấu và chuẩn hóa khoảng trắng."""
    text = no_accent(str(text).lower())
    text = re.sub(r"[^a-z0-9]+", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def load_all_chunks() -> list[dict]:
    """Đọc toàn bộ các đoạn văn bản từ ChromaDB."""
    database_path = str(PERSIST_DIR)

    client = chromadb.PersistentClient(path=database_path)
    collection = client.get_collection(TEXT_COLLECTION_NAME)

    result = collection.get(
        include=["documents", "metadatas"]
    )

    documents = result.get("documents") or []
    metadatas = result.get("metadatas") or []

    chunks = []

    for document, metadata in zip(documents, metadatas):
        if not document:
            continue

        text = document.strip()

        if len(text) < 50:
            continue

        metadata = metadata or {}

        chunks.append({
            "text": text,
            "source": (
                metadata.get("source")
                or metadata.get("pdf_filename")
                or "Sách giáo khoa"
            ),
            "page": (
                metadata.get("page")
                or metadata.get("page_number")
                or "?"
            ),
        })

    return chunks


def find_relevant_chunks(
    question: str,
    chunks: list[dict],
    top_k: int = 10
) -> list[dict]:
    """
    Xếp hạng các đoạn văn dựa trên:
    1. Cụm từ đầy đủ
    2. Cụm hai từ liên tiếp
    3. Các từ nguyên vẹn

    Không dùng phép kiểm tra chuỗi con đơn giản để tránh:
    'sac' khớp nhầm với 'sach'.
    """
    question_normalized = normalize_text(question)

    question_words = [
        word
        for word in question_normalized.split()
        if len(word) > 1 and word not in STOP_WORDS
    ]

    if not question_words:
        return []

    important_phrase = " ".join(question_words)

    bigrams = [
        f"{question_words[index]} {question_words[index + 1]}"
        for index in range(len(question_words) - 1)
    ]

    ranked_chunks = []

    for chunk in chunks:
        text_normalized = normalize_text(chunk["text"])
        text_words = set(text_normalized.split())

        score = 0
        matched_words = 0

        # Khớp toàn bộ cụm từ:
        # "tan sac anh sang"
        if (
            important_phrase
            and important_phrase in text_normalized
        ):
            score += 200

        # Khớp các cụm:
        # "tan sac", "sac anh", "anh sang"
        for bigram in bigrams:
            if bigram in text_normalized:
                score += 40

        # Chỉ so sánh từ nguyên vẹn
        for word in question_words:
            if word in text_words:
                matched_words += 1
                score += 10

        # Yêu cầu khớp ít nhất hai từ quan trọng
        if matched_words >= 2:
            ranked_chunks.append((score, chunk))

    ranked_chunks.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        chunk
        for _, chunk in ranked_chunks[:top_k]
    ]


def build_context(relevant_chunks: list[dict]) -> str:
    """Tạo phần ngữ cảnh gửi cho Gemini."""
    context_parts = []

    for chunk in relevant_chunks:
        text = chunk["text"][:1800]
        source = chunk["source"]
        page = chunk["page"]

        context_parts.append(
            f"=== {source} - trang {page} ===\n{text}"
        )

    return "\n\n".join(context_parts)


async def answer_question(question: str) -> str:
    """Tìm tài liệu và tạo câu trả lời bằng Gemini."""
    from src.rag.gemini_llm import GeminiLLMClient

    chunks = load_all_chunks()

    relevant_chunks = find_relevant_chunks(
        question=question,
        chunks=chunks,
        top_k=12
    )

    if not relevant_chunks:
        return (
            "Không tìm thấy thông tin liên quan "
            "trong cơ sở tri thức."
        )

    context = build_context(relevant_chunks)

    prompt = f"""
Bạn là trợ lý AI hỗ trợ học tập môn Khoa học tự nhiên THCS.
Hãy trả lời hoàn toàn bằng tiếng Việt.

Chỉ sử dụng nội dung sách giáo khoa được cung cấp bên dưới
để trả lời câu hỏi.

--- NỘI DUNG SÁCH GIÁO KHOA ---

{context}

--- CÂU HỎI ---

{question}

--- QUY TẮC ---

1. Trả lời ngắn gọn, chính xác và dễ hiểu.
2. Không tự bổ sung kiến thức không có trong ngữ cảnh.
3. Nếu ngữ cảnh không chứa câu trả lời, hãy trả lời:
   "Thông tin này không được đề cập trong sách giáo khoa."
4. Không nhắc đến các quy tắc hoặc phần ngữ cảnh trong câu trả lời.
"""

    llm = GeminiLLMClient()

    response = await llm.complete(
        [{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=600,
    )

    return response.strip()


if __name__ == "__main__":
    chunks = load_all_chunks()

    print(f"Đã đọc {len(chunks)} chunks từ ChromaDB")
    print(f"Đường dẫn database: {PERSIST_DIR}")

    question = "Tán sắc ánh sáng là gì?"

    print(f"\nCâu hỏi: {question}")

    answer = asyncio.run(answer_question(question))

    print(f"\nTrả lời: {answer}")