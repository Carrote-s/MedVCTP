import string

def normalize(ans):
    return ans.strip().lower().strip(string.punctuation)
    
def med_vctp1(image_path, question, examples5, gCaption, rCaption = None):
    # Define messages
    message1 = f"""This is the medical question at hand about a specific image: {question}. Here is a global caption describing the entire image: {gCaption}. 
    Here are all regional captions for the same image that describe a certain region summarized by the label next to it: {rCaption}
    Your goal is to identify what specific information from the global and regional captions provided are useful for understanding and answering the question.
    Create a summary of the specific information that is concise yet informational and relevant to the question, so that it can be answered properly later.
    The summary can be 4 sentences maximum.
    Make the summary informative enough so that someone without access to the image can use the summary to answer the question, but make it concise enough so that someone can understand it properly"""
    messages1 = [
    {"role": "system", "content": "You are a medical visual reasoning assistant. Base your reasoning on provided medical image context and stay visually grounded and medically accurate."},
    {"role": "user", "content": message1}
    ]
    # Generate concepts & information
    responseConcepts = run_llama(messages1, max_new_tokens = 400)
    #print('1' + responseConcepts)
    message2 = f"""Here is a summary of the relevant concepts and information useful to answering the question at hand: {responseConcepts}. 
    Here is the question that the summary provides useful information to answer: {question}
    The answer to this question is a single word, yes or no. 
    Provided below is a list of 5 different reasoning examples, consisting of an answer to the question and a rationale quickly explaining why the answer was chosen and is correct.
    {examples5}
    Use only the summary provided to generate the rationale. Do not infer or introduce any information not in the summary.
    Use the summary intended to help create the rationale and answer the question. Separate the rationale and answer by 3 hashtags, ###. 
    The rationale should be 1-2 sentences maximum and concise, and the answer should be yes or no to answer the question.
    Make sure the rationale is written so that someone can use it to immediately answer the question given at hand"""
    messages2 = [
    {"role": "system", "content": "You are a medical visual reasoning assistant. Base your reasoning on provided medical image context and stay visually grounded and medically accurate."},
    {"role": "user", "content": message2}
    ]
    # Generate rationale & answer (Conclusion)
    conclusion = run_llama(messages2 , max_new_tokens = 400)
    rationale, answer = parse_vctp_output(conclusion)
    #print('2' + conclusion)
    return rationale, answer
    
def parse_vctp_output(conclusion):
    # Lowercase for normalization
    conclusion = conclusion.lower().strip()
    # Remove leading numbers like "2" or "2###"
    conclusion = conclusion.lstrip("0123456789. ").replace("2###", "").strip()
    # Extract yes/no
    if conclusion.startswith("yes"):
        answer = "yes"
        rationale = conclusion[len("yes"):].strip(" \n#")
    elif conclusion.startswith("no"):
        answer = "no"
        rationale = conclusion[len("no"):].strip(" \n#")
    else:
        # fallback: search for 'yes' or 'no' in the first 20 chars
        if "yes" in conclusion[:20]:
            answer = "yes"
        elif "no" in conclusion[:20]:
            answer = "no"
        else:
            answer = "unknown"
        rationale = conclusion
    return rationale, answer
