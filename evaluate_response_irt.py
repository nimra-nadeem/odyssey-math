import json
from agents.evaluate import Evalutor

# from irt.models import LLAMA_INSTRUCT_MODELS, GPT_MODELS_SWEDEN_CENTRAL, GPT_MODELS_EAST_US, QWEN_INSTRUCT_MODELS
from irt.models import MODELS_260

def load_jsonl(filename):
    """Load JSONL file and return a list of dictionaries."""
    with open(filename, 'r') as file:
        return [json.loads(line) for line in file]

def save_jsonl(data, filename):
    """Save a list of dictionaries to a JSONL file."""
    with open(filename, 'w') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')

def extract_model_name(filepath):
  filepath = filepath.replace("_fs_cot", '')
  filepath = filepath.replace("_zs_cot", '')
  return filepath

def process_files(file_pred, model_name):
    """Process files to compare true and predicted answers and save results."""
    sample_items = load_jsonl(file_pred)
    evalution = Evalutor()

    results = []
    for i, sample in enumerate(sample_items):
        print(f"Processing sample {i}")
        
        true_answer = sample["answer"]
        pred_answer = sample[f"{extract_model_name(model_name)}_response"]

        comparison_result = evalution(question=sample["question"], true=true_answer, prediction=pred_answer)

        sample["true"] = true_answer
        sample["pred"] = pred_answer
        sample["is_correct"] = comparison_result
        results.append(sample)

    return results

def main():
    # all_models = LLAMA_INSTRUCT_MODELS + GPT_MODELS_SWEDEN_CENTRAL + GPT_MODELS_EAST_US + QWEN_INSTRUCT_MODELS
    all_models = MODELS_260
    print(f"Evaluating the following models: \n{all_models}")

    SAMPLE_SIZE = 260

    for model_name in all_models:
        print(f"Processing {model_name}...")
        file_name_prefix = model_name.split("/")[-1]
        file_pred = f"irt/jsonl/{SAMPLE_SIZE}/{file_name_prefix}_{SAMPLE_SIZE}_odyssey.jsonl"
        file_out = f"irt/eval/{SAMPLE_SIZE}/{file_name_prefix}_odyssey_eval.jsonl"

        # results = process_files(file_pred, f"allenai/{model_name}") # need to change this line for each family of models
        results = process_files(file_pred, f"{model_name}")

        save_jsonl(results, file_out)
        print(f"Results have been saved to {file_out}.")

if __name__ == "__main__":
    main()
