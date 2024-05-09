import os
import uuid
import mimetypes
from typing import TYPE_CHECKING, Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from llama_index.core.schema import Document as LlamaIndexDocument
    from langchain_core.documents import Document as LangchainDocument

class Document(BaseModel):
    doc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    text: str = Field(default="")
    metadata: dict = Field(default={})

    @classmethod
    def class_name(cls) -> str:
        return "Document"

    def get_text(self) -> str:
        """Get the text content of the document."""
        return self.text
    
    def get_metadata(self) -> dict:
        """Get the metadata of the document."""
        return self.metadata
    
    @classmethod
    def _convert_metadata(cls, metadata: dict, framework: Literal["llama_index", "langchain"]) -> dict:
        """
        Convert metadata based on the framework (supported llama_index, langchain).

        Args:
            metadata (dict): Metadata to convert.
            framework (Literal["llama_index", "langchain"]): Framework indicator.

        Returns:
            dict: converted metadata.
        """
        today = datetime.now()
        _metadata: dict = {}
        _metadata["creation_date"] = "%s-%s-%s" % (today.year, today.month, today.day)

        if framework == "llama_index":
            _metadata["page"] = metadata["page_label"]
            _metadata["file_name"] = metadata["file_name"]
            _metadata["file_type"] = metadata["file_type"]

        if framework == "langchain":
            _metadata["page"] = metadata["page"] + 1
            _metadata["file_name"] = os.path.basename(metadata["source"])
            _metadata["file_type"] = mimetypes.guess_type(_metadata["file_name"])[0]

        return _metadata
    
    @classmethod
    def _from_langchain_format(cls, doc: "LangchainDocument") -> "Document":
        """
        Convert a document from LangChain format to spyder_index Document format.

        Args:
            doc (LangchainDocument): Document in LangChain format.

        Returns:
            Document: Converted document.
        """
        
        converted_metadata = cls._convert_metadata(doc.metadata, "langchain")
        return cls(text=doc.page_content, metadata=converted_metadata)
    
    @classmethod
    def _from_llama_index_format(cls, doc: "LlamaIndexDocument", metadata: Optional[dict]) -> "Document":
        """
        Convert a document from LlamaIndex format to spyder_index Document format.

        Args:
            doc (LlamaIndexDocument): Document in LlamaIndex format.
            metadata (Optional[dict]): Additional metadata to include in the converted document.

        Returns:
            Document: Converted document.
        """
        converted_metadata = cls._convert_metadata(doc.metadata, "llama_index")
        
        if metadata:
            converted_metadata = metadata | converted_metadata

        return cls(text=doc.text, metadata=converted_metadata)
