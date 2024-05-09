from pathlib import Path
from typing import List, Optional

from spyder_index.core.document import Document

from llama_index.readers.file import PDFReader
from llama_index.readers.file import DocxReader
# from llama_index.readers.file import PptxReader
from llama_index.readers.file import HTMLTagReader

# from llama_index.core import download_loader 
from llama_index.core import SimpleDirectoryReader


class DirectoryLoader():
    def __init__(self) -> None:
        self.supported_file_loader = {
        '.pdf': PDFReader(),
        '.docx': DocxReader(), 
        # '.pptx': PptxReader(), #download_loader('PptxReader'),
        '.html': HTMLTagReader(), 
        # '.txt': download_loader('UnstructuredReader'),
        }

    def load_data(self, dir: str, metadata: Optional[dict]) -> List[Document]:

        llama_documents = SimpleDirectoryReader(
            input_dir=Path(dir).absolute(), 
            file_extractor=self.supported_file_loader, 
            required_exts= list(self.supported_file_loader.keys())).load_data()
        
        return [Document()._from_llama_index_format(doc=doc, metadata=metadata) for doc in llama_documents]
