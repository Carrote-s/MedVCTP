Message1
- This is the medical question at hand about a specific image: {question}. Here is a global caption describing the entire image: {gCaption}. 
    Here are all regional captions for the same image that describe a certain region summarized by the label next to it: {rCaption}
    Your goal is to identify what specific information from the global and regional captions provided are useful for understanding and answering the question.
    Create a summary of the specific information that is concise yet informational and relevant to the question, so that it can be answered properly later.
    The summary can be 4 sentences maximum.
    Make the summary informative enough so that someone without access to the image can use the summary to answer the question, but make it concise enough so that someone can understand it properly
Message2
  - Here is a summary of the relevant concepts and information useful to answering the question at hand: {responseConcepts}. 
    Here is the question that the summary provides useful information to answer: {question}
    The answer to this question is a single word, yes or no. 
    Provided below is a list of 5 different reasoning examples, consisting of an answer to the question and a rationale quickly explaining why the answer was chosen and is correct.
    {examples5}
    Use only the summary provided to generate the rationale. Do not infer or introduce any information not in the summary.
    Use the summary intended to help create the rationale and answer the question. Separate the rationale and answer by 3 hashtags, ###. 
    The rationale should be 1-2 sentences maximum and concise, and the answer should be yes or no to answer the question.
    Make sure the rationale is written so that someone can use it to immediately answer the question given at hand
Message3
- Here is a rationale to a specific question: {refined_rationale}. 
    Here is the question: {question}.
    Use the rationale to give a yes/no answer to the question. Output should be one word.
Message4
- Review this rationale: {modRationale} you generated for the question: {question}. 
            If it uses irrelevant or inaccurate information, remake it based strictly on the provided information base: {information}.
Try to remake the rationale based off the information provided, and the question mentioned earlier. 
Make sure that you strictly utilize information directly from the information base to generate a conclusion with a concise rationale.
Again, here are the 5 different reasoning examples consisting of an answer to the question and a rationale quickly explaining why the answer was chosen and is correct:
{examples}
**Do not use any factual information from these examples; rely solely on the summary provided.**
Make sure the rationales you generate for the given question at hand that use the information base provided earlier are 1-2 sentences maximum, written so that someone can use it to immediately answer the question
