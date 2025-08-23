# from PIL import Image
# from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
# import torch
# import os

# def load_and_process_image(image_path):
#     """Load and preprocess the image"""
#     if not os.path.exists(image_path):
#         raise FileNotFoundError(f"Image not found at: {image_path}")
    
#     image = Image.open(image_path)
#     if image.mode != 'RGB':
#         image = image.convert('RGB')
    
#     return image

# def main():
#     # Configuration
#     model_name = "NAMAA-Space/Qari-OCR-0.1-VL-2B-Instruct"
#     image_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/cropped_regions/crop_2_Text_conf0.527.png"
#     max_tokens = 2000
    
#     print("Loading model and processor...")
    
#     # Load model and processor
#     model = Qwen2VLForConditionalGeneration.from_pretrained(
#         model_name,
#         torch_dtype=torch.float16,  # Explicitly set dtype
#         device_map="auto",
#         trust_remote_code=True
#     )
    
#     processor = AutoProcessor.from_pretrained(
#         model_name, 
#         trust_remote_code=True
#     )
    
#     # Load image
#     print("Loading image...")
#     image = load_and_process_image(image_path)
    
#     # Prepare prompt
#     prompt = "Extract all text from this image. Return only the plain text content without any formatting or explanations."
    
#     # Method 1: Standard approach
#     print("Attempting standard processing...")
#     try:
#         # Prepare inputs
#         inputs = processor(
#             images=image,
#             text=prompt,
#             return_tensors="pt"
#         )
        
#         # Move to device
#         device = "cuda" if torch.cuda.is_available() else "cpu"
#         inputs = {k: v.to(device) for k, v in inputs.items()}
        
#         # Generate
#         with torch.no_grad():
#             outputs = model.generate(
#                 **inputs,
#                 max_new_tokens=max_tokens,
#                 do_sample=False,
#                 pad_token_id=processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id
#             )
        
#         # Decode
#         generated_text = processor.batch_decode(
#             outputs, 
#             skip_special_tokens=True
#         )[0]
        
#         # Extract only the generated part (remove input prompt)
#         if prompt in generated_text:
#             generated_text = generated_text.split(prompt)[-1].strip()
        
#         print("Extracted text:")
#         print(generated_text)
#         return generated_text
        
#     except Exception as e:
#         print(f"Standard approach failed: {e}")
        
#         # Method 2: Chat template approach
#         print("Trying chat template approach...")
#         try:
#             messages = [
#                 {
#                     "role": "user", 
#                     "content": [
#                         {"type": "image", "image": image},
#                         {"type": "text", "text": prompt}
#                     ]
#                 }
#             ]
            
#             # Apply chat template
#             text = processor.apply_chat_template(
#                 messages, 
#                 tokenize=False, 
#                 add_generation_prompt=True
#             )
            
#             # Process with explicit image handling
#             inputs = processor(
#                 text=[text],
#                 images=[image],
#                 return_tensors="pt",
#                 padding=True
#             )
            
#             device = "cuda" if torch.cuda.is_available() else "cpu"
#             inputs = {k: v.to(device) for k, v in inputs.items()}
            
#             with torch.no_grad():
#                 generated_ids = model.generate(
#                     **inputs,
#                     max_new_tokens=max_tokens,
#                     do_sample=False,
#                     pad_token_id=processor.tokenizer.pad_token_id or processor.tokenizer.eos_token_id
#                 )
            
#             # Trim input tokens from output
#             generated_ids_trimmed = [
#                 out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
#             ]
            
#             output_text = processor.batch_decode(
#                 generated_ids_trimmed, 
#                 skip_special_tokens=True, 
#                 clean_up_tokenization_spaces=False
#             )[0]
            
#             print("Extracted text (chat template method):")
#             print(output_text)
#             return output_text
            
#         except Exception as e2:
#             print(f"Chat template approach also failed: {e2}")
            
#             # Debug information
#             print("\nDebug Information:")
#             print(f"Image mode: {image.mode}")
#             print(f"Image size: {image.size}")
#             print(f"Model device: {next(model.parameters()).device}")
#             print(f"CUDA available: {torch.cuda.is_available()}")
#             print(f"Processor tokenizer type: {type(processor.tokenizer)}")
            
#             return None

# if __name__ == "__main__":
#     result = main()
#     if result is None:
#         print("OCR extraction failed with all methods.")


from paddleocr import PaddleOCR

# Initialize with recognition only
ocr = PaddleOCR(
    use_angle_cls=True, 
    lang='ar',
    rec_model_dir=None,  # Use default
    use_gpu=True,
    show_log=False
)

# For text recognition only (if you have cropped text images)
img_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/cropped_regions/crop_2_Text_conf0.527.png"

# Since your image appears to be a cropped text region, you can use:
result = ocr.ocr(img_path, det=False, cls=False)  # Skip detection, only recognize

print("Recognized text:")
if result and result[0]:
    for line in result[0]:
        print(f"Text: {line[0]}, Confidence: {line[1]:.3f}")
