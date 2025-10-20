# Prompt 1
- "Describe this medical image with a focus on **key observations and high-level features**."
  "Cover aspects relevant to these features: Plane, Image quality, Modality, Position, Organ, and overall relationships between structures."
  "Include overall anatomical structures and significant spatial relationships between multiple structures, if present."
  "If the image contains only one object, you may skip describing relationships or Knowledge Graph connections."
  "Provide enough context for a clinical expert to understand the image, but avoid disclaimers, repeated warnings, or unrelated commentary."
  "Do not provide a final diagnosis—only describe what is visible and significant."’
# Prompt 2
- f"Here is the full image for context. Below is a cropped version highlighting {label}."
"Describe this region with focus on **key observations and fine-grained details**."
"Cover aspects relevant to these features: Color, Shape, Size, and Abnormal findings."
"Include potential abnormalities that are visible in this region.”
"Avoid repeating items, unrelated structures, disclaimers, or unnecessary explanations."
"Prioritize concise, clinically meaningful descriptions."
"Do not provide a diagnosis—only describe what is visible and significant in this region."
