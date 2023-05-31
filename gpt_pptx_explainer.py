import asyncio
import json
import os

from openai_api import OpenaiApi
from pptx_parser import PptxParser


class GptPptxExplainer:
    """
    Connects between the parsing of the presentation and calling the OpenAi API asynchronously to receive the
    explanation of each slide.
    """

    @classmethod
    async def explain(cls, file_path):
        """
        Receives a path to a pptx file, connects to OpenAi asynchronously and receives the explanation to each slide.
        Creates a json file with the explanation of the presentation.
        :param file_path: str path to a pptx file
        """
        base_file_name = os.path.basename(file_path)
        tasks = []
        gpt_outputs = []
        # Parse the presentation
        for index, slide_text in PptxParser.parse(file_path):
            prompt_content = {
                'slide_index': index,
                'file_title': base_file_name,
                'slide_text': slide_text
            }
            # save the openai explanation results
            tasks.append(
                OpenaiApi.get_model_response(gpt_outputs, prompt_content)
            )
        await asyncio.gather(*tasks)
        # save the results in json
        with open(f'{os.path.splitext(file_path)[0]}_explained.json', 'w') as f:
            f.write(json.dumps(gpt_outputs))


if __name__ == "__main__":
    file_path = input("Enter a pptx file path: ")
    asyncio.run(GptPptxExplainer.explain(file_path))
