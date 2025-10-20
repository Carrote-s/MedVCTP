!pip install huggingface_hub
!pip install transformers
!pip install accelerate
!pip install torch
!pip install fiftyone
with open("raw_images_with_bbox_new.json", "r") as f:
    rawBBImages = json.load(f)

output_dir = "generated_captions"
os.makedirs(output_dir, exist_ok=True)

temperatures = [0]

for temperature in temperatures:
    dictList = []

    for entry in rawBBImages:
        image_path = entry["image_path"]
        image_id = entry["image_id"]
        img = Image.open(image_path)
        # loops over every bounding box region per image
        for det in entry["detections"]:
            label = det["label"]
            coords = det["bounding_box"]
            croppedImg = crop_bbox(image_path, coords)

            messages = [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are an expert radiologist."}]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Here is the full image for context. Below is a cropped version of the image, highlighting {label}." 
                        "Focus only on key observations and findings within this region, and if necessary, use the full image to gain context."
                        "Include potential abnormalities and relevant anatomical context that are apparent in the region."
                        "Avoid repeating items, unrelated structures, disclaimers, or unnecessary explanations."
                        "Prioritize concise, clinically meaningful descriptions."},
                        {"type": "image", "image": img},
                        {"type": "image", "image": croppedImg}
                    ]
                }
            ]

            #generation of captions
            inputs = processor.apply_chat_template(
                messages, add_generation_prompt=True, tokenize=True,
                return_dict=True, return_tensors="pt"
            ).to(model.device, dtype=torch.bfloat16)

            input_len = inputs["input_ids"].shape[-1]
            do_sample_flag = temperature > 0
            with torch.inference_mode():
                generation = model.generate(
                    **inputs, max_new_tokens=512, 
                    do_sample=do_sample_flag, temperature=temperature if do_sample_flag else None
                )
                generation = generation[0][input_len:]

            decoded = processor.decode(generation, skip_special_tokens=True)
            print(f"Generated caption for image {image_id}, region {label} is:\n{decoded}\n")

            # ---- SAVE RESULT ----
            result = {
                "image_id": image_id,
                "label": label,
                "caption": decoded,
            }
            dictList.append(result)

    output_file = os.path.join(output_dir, f"rCaptions_{temperature}.json")
    with open(output_file, "w") as f:
        json.dump(dictList, f, indent=4)

    print(f"Results for temperature {temperature} saved to {output_file}")













def crop_bbox_with_padding(image_path, bbox, padding=0.05):
    from PIL import Image

    img = Image.open(image_path)
    img_w, img_h = img.size
    x, y, w, h = bbox

    # Expand bbox with padding
    x_pad = w * padding
    y_pad = h * padding

    left = max(int((x - x_pad) * img_w), 0)
    top = max(int((y - y_pad) * img_h), 0)
    right = min(int((x + w + x_pad) * img_w), img_w)
    bottom = min(int((y + h + y_pad) * img_h), img_h)

    return img.crop((left, top, right, bottom))































# Image attribution: Stillwaterising, CC0, via Wikimedia Commons
with open("raw_images.json","r") as f:
  rawImages = json.load(f)

output_dir = "generated_captions"
os.makedirs(output_dir, exist_ok=True)

temperatures = [0]
for temperature in temperatures:
  dictList = []
  for entry in rawImages:
    image_path = entry["image_path"]
    image_id = entry["image_id"]
    image = Image.open(image_path) #could add .rgb here

    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are an expert radiologist."}]
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this medical image with a focus on **key observations and findings**. "
                "Include relevant anatomical structures, potential abnormalities, and significant details."
                "Provide enough context for a clinical expert to understand the image, "
                "but avoid disclaimers, repeated warnings, or any unrelated commentary. "
                "Do not provide a final diagnosis—only describe what is visible and significant."},
                {"type": "image", "image": image}
            ]
        }
    ]

    inputs = processor.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt"
    ).to(model.device, dtype=torch.bfloat16)

    input_len = inputs["input_ids"].shape[-1]
    do_sample_flag = temperature > 0
    with torch.inference_mode():
        generation = model.generate(**inputs, max_new_tokens=512, do_sample=do_sample_flag, temperature = temperature if do_sample_flag else None)
        generation = generation[0][input_len:]

    decoded = processor.decode(generation, skip_special_tokens=True)
    print(f"Generated caption for imagePath: {image_path} is: {decoded}")

    result = {
              "image_id": image_id,
              "caption": decoded,
          }
    dictList.append(result)

  output_file = os.path.join(output_dir, f"gCaptions_{temperature}.json")
    
  with open(output_file, "w") as f:
    json.dump(dictList, f, indent=4)
    
  print(f"Results for temperature {temperature} saved to {output_file}")
