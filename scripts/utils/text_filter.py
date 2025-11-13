import re

def _filter_import(response: str) -> str:
    """
    Removes all the import statements enclosed in a Python code block of a textual response.
    """
    pattern = re.compile(r"```python(.*?)(?:```|$)", re.DOTALL)

    def _remove_import_from_python_block(block):
        text = block.splitlines()
        filtered_text = [sentence for sentence in text if not sentence.strip().startswith("import ")]
        return '\n'.join(filtered_text)

    new_response = pattern.sub(lambda m: "```python\n" + _remove_import_from_python_block(m.group(1)) + (
        "\n```" if m.group(0).endswith("```") else ""), response)
    return new_response

def _complete_dictionary(dictionary: str) -> str:
    """
    Completes a dictionary with all the syntax it needs, if any.
    """
    open_sqm = dictionary.count("'")
    open_dqm = dictionary.count('"')
    open_brackets = dictionary.count('[') - dictionary.count(']')
    open_braces = dictionary.count('{') - dictionary.count('}')

    if open_sqm % 2 != 0:
        dictionary += "'"
    if open_dqm % 2 != 0:
        dictionary += '"'
    if open_brackets > 0:
        dictionary += ']' * open_brackets
    if open_braces > 0:
        dictionary += '}' * open_braces

    return dictionary

def _filter_dataset(response: str) -> str:
    """
    Removes all the datasets enclosed in a Python code block of a textual response.
    """
    python_block_pattern = re.compile(r"```python(.*?)(?:```|$)", re.DOTALL)
    dictionary_pattern = re.compile(r'\s*\w+\s*=\s*\{[^}]*?\[\s*[^]]*?\s*]\s*,?[^}]*?}')

    def _remove_dataset_from_python_block(block: str) -> str:
        # completes block if it is an incomplete dictionary, otherwise returns it as is
        block = _complete_dictionary(block)
        return dictionary_pattern.sub("", block)

    new_response = python_block_pattern.sub(
        lambda m: "```python\n" + _remove_dataset_from_python_block(m.group(1)) +
                  ("```\n" if m.group(0).endswith("```") else ""),
        response
    )
    return new_response

def _filter_extra_newlines(response: str) -> str:
    """
    Replace three or more consecutive newlines with two newlines.
    """
    new_response = re.sub(r'\n{3,}', '\n\n', response)
    return new_response

def filter_llm_response(response: str) -> str:
    """
    Removes all the lines of code enclosed in a Python code block of a textual response that
    are not meaningful. Such lines of code include: import statements, datasets, extra newlines.
    """
    new_response = response
    new_response = _filter_import(new_response)
    new_response = _filter_dataset(new_response)
    new_response = _filter_extra_newlines(new_response)
    new_response = new_response.strip()
    if new_response == "```python":
        return ""
    else:
        return new_response