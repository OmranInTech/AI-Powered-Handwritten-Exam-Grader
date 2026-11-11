from transformers import TrOCRProcessor, VisionEncoderDecoderModel, AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

class ModelLoader:
    def __init__(self):
        self.trocr_processor = None
        self.trocr_model = None
        self.qwen_tokenizer = None
        self.qwen_model = None
        self.embedding_model = None

    def load_trocr(self):
        model_id = "microsoft/trocr-base-handwritten"

        self.trocr_processor = TrOCRProcessor.from_pretrained(
            model_id,
            local_files_only=True
        )
        self.trocr_model = VisionEncoderDecoderModel.from_pretrained(
            model_id,
            local_files_only=True
        )

    def load_qwen(self):
        model_id = "Qwen/Qwen2.5-1.5B-Instruct"

        self.qwen_tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            local_files_only=True
        )
        self.qwen_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            local_files_only=True
        )

    def load_embeddings(self):
        self.embedding_model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            local_files_only=True
        )
