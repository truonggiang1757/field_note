from typing import Optional
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.llm_config import get_chat_model
from app.utils.helpers import load_prompt, prepare_image

DEFAULT_PROMPT="app/templates/concrete_note/concrete_note.txt"
OCR_PROMPT="app/templates/ocr.txt"

class ConcreteNoteService:
    def __init__(
        self,
        model_name: Optional[str] = None,
    ):
        prompt_text = load_prompt(DEFAULT_PROMPT)
        self.prompt = ChatPromptTemplate.from_template(prompt_text)
        self.ocr_prompt = load_prompt(OCR_PROMPT)

        self.model = get_chat_model(model_name)
        self.ocr_model = get_chat_model("5CD-AI/Vintern-3B-R-beta")

        self.parser = JsonOutputParser()
        self.ocr_parser = StrOutputParser()

        self.chain = self.prompt | self.model | self.parser
        self.ocr_chain = self.prompt | self.ocr_model | self.ocr_parser
    
    async def process_file(self, file_content: bytes):
        image_message = prepare_image(file_content, self.ocr_prompt)
        print("Step 1: OCR")
        ocr_res = await self.ocr_model.ainvoke(image_message)
        print(ocr_res)
        ocr_text = ocr_res.content
        print("Step 2: Extract")
        res = await self.chain.ainvoke({"ocr_text": ocr_text})

        return res