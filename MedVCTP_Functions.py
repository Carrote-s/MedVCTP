import string

def normalize(ans):
    return ans.strip().lower().strip(string.punctuation)
    
def med_vctp(image_path, question, examples5, gCaption, rCaption = None):
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
    #print('2' + conclusion)
    if '###' in conclusion:
        parts = conclusion.split('###')
        rationale = parts[0].strip()
        answer = parts[-1].strip()  # last part should be the yes/no
    else:
      rationale, answer = conclusion, 'unknown'   
    refined_rationale = rationaleCheck(question, responseConcepts, image_path, rationale, examples5)
    #print('3' + refined_rationale)
    refined_answer = run_llama(messages = [
    {"role": "system", "content": "You are a medical visual reasoning assistant. Base your reasoning on provided medical image context and stay visually grounded and medically accurate."},
    {"role": "user", "content": f"""Here is a rationale to a specific question: {refined_rationale}. 
    Here is the question: {question}.
    Use the rationale to give a yes/no answer to the question. Output should be one word."""}
    ])
    #print('4' + refined_answer)
    return refined_rationale, refined_answer

def rationaleCheck(question, information, image_path, rationale, examples, maxIter=3, threshold_method='manual', manual_thresh=30):
    openedImage = Image.open(image_path)
    modRationale = rationale
    best_rationale = modRationale
    best_score = -1.0  # initialize as very low
    for x in range(maxIter):
        improvMsg = [
            {"role": "system", "content": "You are a medical visual reasoning assistant. Base your reasoning on provided medical image context and stay visually grounded and medically accurate."},
            {"role": "user", "content": f"""Review this rationale: {modRationale} you generated for the question: {question}. 
            If it uses irrelevant or inaccurate information, remake it based strictly on the provided information base: {information}.
Try to remake the rationale based off the information provided, and the question mentioned earlier. 
Make sure that you strictly utilize information directly from the information base to generate a conclusion with a concise rationale.
Again, here are the 5 different reasoning examples consisting of an answer to the question and a rationale quickly explaining why the answer was chosen and is correct:
{examples}
**Do not use any factual information from these examples; rely solely on the summary provided.**
Make sure the rationales you generate for the given question at hand that use the information base provided earlier are 1-2 sentences maximum, written so that someone can use it to immediately answer the question"""
            }
        ]
        accepted, rejected, scores, thresh = confirm_module.confirm(
            openedImage, [modRationale], threshold_method, top_pct=0.5, manual_thresh=manual_thresh
        )
        # unwrap single-value tensor into float
        if isinstance(scores, torch.Tensor):
            current_score = float(scores.item())
        else:
            current_score = float(scores)
        # Track the highest scoring rationale
        if current_score > best_score:
            best_score = current_score
            best_rationale = modRationale
        if accepted:
            return modRationale
        else:
            modRationale = run_llama(improvMsg)
    # Fallback: if no rationale passed the threshold, return the one with highest score
    return best_rationale
