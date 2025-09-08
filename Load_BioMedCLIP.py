!pip install open_clip_torch==2.23.0 transformers==4.35.2 matplotlib
from open_clip import create_model_from_pretrained, get_tokenizer # works on open-clip-torch>=2.23.0, timm>=0.9.8
model, preprocess = create_model_from_pretrained('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
tokenizer = get_tokenizer('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')

import torch
from open_clip import create_model_and_transforms, get_tokenizer
from PIL import Image

class BiomedCLIPConfirm:
    def __init__(self, 
                 model_name="hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224",
                 device=None,
                 single_rationale_threshold=20.0):
        """
        Initialize BiomedCLIP confirm module.
        
        Args:
            single_rationale_threshold: float, threshold for accepting a single rationale
        """
        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
        # Load model, tokenizer, and preprocessing transforms
        self.model, _, self.preprocess = create_model_and_transforms(model_name)
        self.tokenizer = get_tokenizer(model_name)
        self.model.to(self.device)
        self.model.eval()
        self.context_length = 256  # Max tokens for rationales
        self.single_rationale_threshold = single_rationale_threshold

    def score_rationales(self, image, rationales, template="This is a generated rationale for an image:"):
        """
        Compute similarity scores between image and list of rationales.
        Returns a tensor of scores.
        """
        # Preprocess image
        if not isinstance(image, torch.Tensor):
            image = self.preprocess(image).unsqueeze(0)  # add batch dim
        image = image.to(self.device)
        # Tokenize rationales
        texts = self.tokenizer([template + r for r in rationales],
                               context_length=self.context_length).to(self.device)
        # Compute embeddings
        with torch.no_grad():
            image_features, text_features, logit_scale = self.model(image, texts)
            scores = (image_features @ text_features.T).squeeze(0) * logit_scale
        return scores

    def confirm(self, image, rationales, threshold_method='percentile', 
                top_pct=0.3, epsilon=0.05, manual_thresh=None):
        """
        Accept/reject rationales based on similarity thresholds.
        
        threshold_method: 'percentile', 'relative_max', or 'manual'
        manual_thresh: float, only used if threshold_method='manual'
        """
        scores = self.score_rationales(image, rationales)
        if threshold_method == 'percentile':
            thresh = torch.quantile(scores, 1 - top_pct)
        elif threshold_method == 'relative_max':
            thresh = scores.max() - epsilon
        elif threshold_method == 'manual':
            if manual_thresh is None:
                raise ValueError("Must provide manual_thresh when using threshold_method='manual'")
            thresh = manual_thresh
        else:
            raise ValueError("threshold_method must be 'percentile', 'relative_max', or 'manual'")
        accepted = [r for r, s in zip(rationales, scores) if s >= thresh]
        rejected = [r for r, s in zip(rationales, scores) if s < thresh]
# Initialize
confirm_module = BiomedCLIPConfirm()
        return accepted, rejected, scores, float(thresh)
