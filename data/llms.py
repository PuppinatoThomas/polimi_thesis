from experiments.model.llm import GPT, Gemini, DeepSeek

llms = [
    GPT(
       model_name="gpt-5"
    ),
    Gemini(
       model_name="gemini-2.0-flash"
    ),
    DeepSeek(
       model_name="deepseek-reasoner"
    )
]

def get_llm(llm_name):

    for llm in llms:
        if llm.name == llm_name:
            return llm

    raise ValueError(f"No such LLM: {llm_name}")