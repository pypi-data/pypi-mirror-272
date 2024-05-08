import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sqlparse
import re

# torch.cuda.is_available()

def sql_model(
    model_name: str = 'defog/sqlcoder-7b',
    cache_dir: str = './',
    device_map: str = 'auto',
    trust_remote_code: bool = True,
    torch_dtype: torch.dtype = torch.float16,
    # load_in_8bit: bool = False,
    # load_in_4bit: bool = False,
    use_cache: bool = True,
    force_download: bool = False,
    resume_download: bool = False,
    output_loading_info: bool = False,
    local_files_only: bool = False,
):
    if torch.cuda.is_available() == True :
        allowed_models = ['defog/sqlcoder-7b', 'defog/sqlcoder-34b-alpha', 'defog/sqlcoder-70b-alpha']
        if model_name not in allowed_models:
            raise ValueError(f"Invalid model_name. Allowed options are {allowed_models}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=trust_remote_code,
            torch_dtype=torch_dtype,
            # load_in_8bit=load_in_8bit,
            # load_in_4bit=load_in_4bit,
            device_map=device_map,
            use_cache=use_cache,
            cache_dir=cache_dir,
            force_download=force_download,
            resume_download=resume_download,
            output_loading_info=output_loading_info,
            local_files_only=local_files_only,
        )
        return model,tokenizer
    else :
        raise RuntimeError("GPU support is not available")





def sql_to_string(sql_file_path):
    with open(sql_file_path, 'r') as file:
        sql_text = file.read()

    keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'GROUP BY', 'ORDER BY', 'HAVING', 'UNION', 'INSERT INTO', 'UPDATE', 'DELETE FROM', 'CREATE TABLE']

    keyword_regex = '|'.join(map(re.escape, keywords))
    indent_regex = re.compile(r'(\()|(\))|(\b' + keyword_regex + r'\b)')

    lines = []
    indent_level = 0
    for line in sql_text.split('\n'):
        matches = indent_regex.findall(line)
        for match in matches:
            if match[0]:  
                indent_level += 1
            elif match[1]:  
                indent_level = max(0, indent_level - 1)
            elif match[2]:  
                lines.append('    ' * indent_level + line.strip())
                break
        else:
            lines.append('    ' * indent_level + line.strip())

    python_string = '\n'.join(lines)
    
    return python_string


def generate_schema(question,file_path,main_model):

    torch.cuda.empty_cache()
    torch.cuda.synchronize()

    prompt = """### Task
    Generate a SQL query to answer the following question:
    `{question}`

    ### Database Schema
    This query will run on a database whose schema is represented in this string:

    `{schema}`

    ### SQL
    Given the database schema, here is the SQL query that answers `{question}`:
    ```sql
    """.format(question=question,schema=sql_to_string(file_path))
    
    eos_token_id = main_model[1].eos_token_id

    inputs = main_model[1](prompt, return_tensors="pt").to("cuda")
    generated_ids = main_model[0].generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=eos_token_id,
        pad_token_id=eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=1,

    )

    outputs = main_model[1].batch_decode(generated_ids, skip_special_tokens=True)


    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    # empty cache so that you do generate more results w/o memory crashing
    # particularly important on Colab – memory management is much more straightforward
    # when running on an inference service

    return(sqlparse.format(outputs[0].split("```sql")[-1], reindent=True))