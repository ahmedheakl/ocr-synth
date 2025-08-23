# import numpy as np
# import torch
# from PIL import Image, ImageDraw, ImageFont
# from doclayout_yolo import YOLOv10
# from huggingface_hub import hf_hub_download
# import matplotlib.pyplot as plt
# import random

# # YOLOv10 label mapping
# YOLO_LABELS = {
#     "title": "title",
#     "plain text": "Text",
#     "abandon": "title",
#     "figure": "Figure",
#     "figure_caption": "Caption",
#     "table": "Table",
#     "table_caption": "Caption",
#     "table_footnote": "Text",
#     "isolate_formula": "Text",
#     "formula_caption": "Caption",
# }

# # Colors for different element types
# COLORS = {
#     "title": "#FF6B6B",
#     "Text": "#4ECDC4", 
#     "Figure": "#45B7D1",
#     "Caption": "#FFA07A",
#     "Table": "#98D8C8",
#     "Picture": "#F7DC6F",
# }

# class SimpleLayoutDetector:
#     def __init__(self, model_path=None):
#         """Initialize the layout detector with YOLO model"""
#         if model_path is None:
#             # Download from HuggingFace Hub
#             filepath = hf_hub_download(
#                 repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
#                 filename="doclayout_yolo_docstructbench_imgsz1024.pt"
#             )
#             self.model = YOLOv10(filepath)
#         else:
#             self.model = YOLOv10(model_path)
        
#         self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
#         self.image_size = 1024

#     def predict(self, image_path_or_pil):
#         """Run prediction on an image"""
#         # Load image
#         if isinstance(image_path_or_pil, str):
#             image = Image.open(image_path_or_pil).convert("RGB")
#         else:
#             image = image_path_or_pil.convert("RGB")
        
#         # Convert to numpy for YOLO
#         image_np = np.array(image)
        
#         # Run prediction
#         results = self.model.predict(
#             image_np, 
#             imgsz=self.image_size, 
#             conf=0.2, 
#             device=self.device
#         )[0]
        
#         # Parse results
#         predictions = []
#         for box in results.boxes:
#             bbox = box.xyxy[0].cpu().numpy()
#             label_id = int(box.cls[0])
#             confidence = float(box.conf[0])
#             label_str = list(YOLO_LABELS.keys())[label_id]
            
#             predictions.append({
#                 "bbox": bbox.tolist(),
#                 "label": YOLO_LABELS.get(label_str, label_str),
#                 "confidence": confidence
#             })
        
#         return image, predictions

#     def draw_boxes(self, image, predictions, show_confidence=True):
#         """Draw bounding boxes on the image"""
#         # Create a copy to draw on
#         draw_image = image.copy()
#         draw = ImageDraw.Draw(draw_image)
        
#         # Try to load a font, fallback to default if not available
#         try:
#             font = ImageFont.truetype("arial.ttf", 16)
#         except:
#             font = ImageFont.load_default()
        
#         for pred in predictions:
#             bbox = pred["bbox"]
#             label = pred["label"]
#             confidence = pred["confidence"]
            
#             # Get color for this label
#             color = COLORS.get(label, "#000000")
            
#             # Draw bounding box
#             draw.rectangle(bbox, outline=color, width=3)
            
#             # Prepare text
#             if show_confidence:
#                 text = f"{label}: {confidence:.2f}"
#             else:
#                 text = label
            
#             # Draw text background
#             text_bbox = draw.textbbox((bbox[0], bbox[1]), text, font=font)
#             text_width = text_bbox[2] - text_bbox[0]
#             text_height = text_bbox[3] - text_bbox[1]
            
#             draw.rectangle(
#                 [bbox[0], bbox[1] - text_height - 4, bbox[0] + text_width + 4, bbox[1]], 
#                 fill=color
#             )
            
#             # Draw text
#             draw.text((bbox[0] + 2, bbox[1] - text_height - 2), text, fill="white", font=font)
        
#         return draw_image

#     def detect_and_visualize(self, image_path_or_pil, save_path=None, show=True):
#         """Complete pipeline: detect layout and visualize results"""
#         # Run prediction
#         image, predictions = self.predict(image_path_or_pil)
        
#         # Draw boxes
#         result_image = self.draw_boxes(image, predictions)
        
#         # Print detected elements
#         print(f"Detected {len(predictions)} layout elements:")
#         for i, pred in enumerate(predictions):
#             print(f"  {i+1}. {pred['label']} (confidence: {pred['confidence']:.3f})")
        
#         # Save if requested
#         if save_path:
#             result_image.save(save_path)
#             print(f"Result saved to: {save_path}")
        
#         # Show if requested
#         if show:
#             plt.figure(figsize=(12, 8))
#             plt.imshow(result_image)
#             plt.axis('off')
#             plt.title("Document Layout Detection")
#             plt.tight_layout()
#             plt.show()
        
#         return result_image, predictions

# # Example usage
# if __name__ == "__main__":
#     # Initialize detector
#     detector = SimpleLayoutDetector(model_path="/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/models/doclayout_yolo_docstructbench_imgsz1024.pt")
    
#     # Example: process an image
#     # Replace 'your_image.jpg' with your image path
#     image_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/testing_images/13026818_section_219_portrait_one_col_arabic_template_0_image_0.png"  # Change this to your image path
    
#     try:
#         # Detect and visualize
#         result_image, predictions = detector.detect_and_visualize(
#             image_path, 
#             save_path="layout_detection_result.jpg",
#             show=True
#         )
        
#     except FileNotFoundError:
#         print("Please replace 'your_image.jpg' with the path to your image file")
#         print("\nAlternatively, you can use it programmatically:")
#         print("detector = SimpleLayoutDetector()")
#         print("result_image, predictions = detector.detect_and_visualize('path/to/your/image.jpg')")

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont
from doclayout_yolo import YOLOv10
from huggingface_hub import hf_hub_download
import matplotlib.pyplot as plt
import json
import os
from datetime import datetime
from transformers import NougatProcessor, VisionEncoderDecoderModel

# YOLOv10 label mapping
YOLO_LABELS = {
    "title": "title",
    "plain text": "Text",
    "abandon": "title",
    "figure": "Figure",
    "figure_caption": "Caption",
    "table": "Table",
    "table_caption": "Caption",
    "table_footnote": "Text",
    "isolate_formula": "Text",
    "formula_caption": "Caption",
}

# Colors for different element types
COLORS = {
    "title": "#FF6B6B",
    "Text": "#4ECDC4", 
    "Figure": "#45B7D1",
    "Caption": "#FFA07A",
    "Table": "#98D8C8",
    "Picture": "#F7DC6F",
}

class LayoutDetectorWithOCR:
    def __init__(self, layout_model_path=None, confidence_threshold=0.5):
        """Initialize the layout detector with YOLO model and Arabic OCR"""
        
        # Initialize layout detection model
        if layout_model_path is None:
            # Download from HuggingFace Hub
            filepath = hf_hub_download(
                repo_id="juliozhao/DocLayout-YOLO-DocStructBench",
                filename="doclayout_yolo_docstructbench_imgsz1024.pt"
            )
            self.layout_model = YOLOv10(filepath)
        else:
            self.layout_model = YOLOv10(layout_model_path)
        
        # Initialize Arabic OCR model
        print("Loading Arabic OCR model...")
        self.ocr_processor = NougatProcessor.from_pretrained("MohamedRashad/arabic-small-nougat")
        self.ocr_model = VisionEncoderDecoderModel.from_pretrained("MohamedRashad/arabic-small-nougat")
        
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.ocr_model.to(self.device)
        self.image_size = 1024
        self.confidence_threshold = confidence_threshold
        self.context_length = 2048
        
        print(f"Models loaded on device: {self.device}")

    def predict_layout(self, image_path_or_pil):
        """Run layout prediction on an image"""
        # Load image
        if isinstance(image_path_or_pil, str):
            image = Image.open(image_path_or_pil).convert("RGB")
        else:
            image = image_path_or_pil.convert("RGB")
        
        # Convert to numpy for YOLO
        image_np = np.array(image)
        
        # Run prediction
        results = self.layout_model.predict(
            image_np, 
            imgsz=self.image_size, 
            conf=0.2,  # Use lower conf for detection, we'll filter later
            device=self.device
        )[0]
        
        # Parse results and filter by confidence
        predictions = []
        for box in results.boxes:
            bbox = box.xyxy[0].cpu().numpy()
            label_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label_str = list(YOLO_LABELS.keys())[label_id]
            
            # Filter by confidence threshold
            if confidence >= self.confidence_threshold:
                predictions.append({
                    "bbox": bbox.tolist(),
                    "label": YOLO_LABELS.get(label_str, label_str),
                    "confidence": confidence
                })
        print("predictions: ", predictions)
        return image, predictions

    def crop_image_region(self, image, bbox):
        """Crop a region from the image based on bbox coordinates"""
        x1, y1, x2, y2 = [int(coord) for coord in bbox]
        
        # Ensure coordinates are within image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(image.width, x2)
        y2 = min(image.height, y2)
        
        cropped_image = image.crop((x1, y1, x2, y2))
        return cropped_image

    def extract_text_with_ocr(self, cropped_image):
        """Extract text from a cropped image using Arabic OCR"""
        try:
            # Prepare image for the OCR model
            pixel_values = self.ocr_processor(cropped_image, return_tensors="pt").pixel_values
            
            # Generate transcription
            outputs = self.ocr_model.generate(
                pixel_values.to(self.device),
                min_length=1,
                max_new_tokens=self.context_length,
                bad_words_ids=[[self.ocr_processor.tokenizer.unk_token_id]],
            )
            
            # Decode the output
            text_sequence = self.ocr_processor.batch_decode(outputs, skip_special_tokens=True)[0]
            text_sequence = self.ocr_processor.post_process_generation(text_sequence, fix_markdown=False)
            
            return text_sequence.strip()
        
        except Exception as e:
            print(f"Error during OCR: {str(e)}")
            return ""

    def process_document(self, image_path_or_pil, save_crops=False, crops_dir="cropped_regions"):
        """Complete pipeline: detect layout, extract text, and return results"""
        
        print("Running layout detection...")
        # Run layout prediction
        image, predictions = self.predict_layout(image_path_or_pil)
        
        if not predictions:
            print("No predictions with confidence >= threshold found.")
            return []
        
        print(f"Found {len(predictions)} layout elements with confidence >= {self.confidence_threshold}")
        
        # Create directory for cropped images if requested
        if save_crops and not os.path.exists(crops_dir):
            os.makedirs(crops_dir)
        
        # Process each prediction
        results = []
        for i, pred in enumerate(predictions):
            print(f"Processing region {i+1}/{len(predictions)}: {pred['label']} (conf: {pred['confidence']:.3f})")
            
            # Crop the image region
            cropped_image = self.crop_image_region(image, pred['bbox'])
            
            # Save cropped image if requested
            if save_crops:
                crop_filename = f"crop_{i+1}_{pred['label']}_conf{pred['confidence']:.3f}.png"
                crop_path = os.path.join(crops_dir, crop_filename)
                cropped_image.save(crop_path)
            
            # Extract text using OCR
            extracted_text = self.extract_text_with_ocr(cropped_image)
            
            # Store results
            result = {
                "region_id": i + 1,
                "bbox": pred['bbox'],
                "label": pred['label'],
                "confidence": pred['confidence'],
                "extracted_text": extracted_text,
                "text_length": len(extracted_text)
            }
            
            results.append(result)
            print(f"  Extracted text length: {len(extracted_text)} characters")
            if extracted_text:
                preview = extracted_text[:100] + "..." if len(extracted_text) > 100 else extracted_text
                print(f"  Text preview: {preview}")
        
        return results

    def save_results_to_json(self, results, output_path, image_path=None, include_metadata=True):
        """Save results to JSON file with optional metadata"""
        
        # Prepare the output data
        output_data = {
            "results": results,
            "summary": {
                "total_regions": len(results),
                "confidence_threshold": self.confidence_threshold,
                "regions_by_type": {}
            }
        }
        
        # Add metadata if requested
        if include_metadata:
            output_data["metadata"] = {
                "timestamp": datetime.now().isoformat(),
                "source_image": image_path if isinstance(image_path, str) else "PIL Image",
                "device_used": self.device,
                "layout_model": "DocLayout-YOLO",
                "ocr_model": "MohamedRashad/arabic-small-nougat"
            }
        
        # Calculate summary statistics
        for result in results:
            label = result['label']
            if label not in output_data["summary"]["regions_by_type"]:
                output_data["summary"]["regions_by_type"][label] = 0
            output_data["summary"]["regions_by_type"][label] += 1
        
        # Save to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"Results saved to: {output_path}")
        return output_data

    def draw_boxes_with_text(self, image, results, show_confidence=True):
        """Draw bounding boxes on the image with text preview"""
        # Create a copy to draw on
        draw_image = image.copy()
        draw = ImageDraw.Draw(draw_image)
        
        # Try to load a font, fallback to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        for result in results:
            bbox = result["bbox"]
            label = result["label"]
            confidence = result["confidence"]
            text_preview = result["extracted_text"][:30] + "..." if len(result["extracted_text"]) > 30 else result["extracted_text"]
            
            # Get color for this label
            color = COLORS.get(label, "#000000")
            
            # Draw bounding box
            draw.rectangle(bbox, outline=color, width=3)
            
            # Prepare text
            if show_confidence:
                display_text = f"{label}: {confidence:.2f}\n{text_preview}"
            else:
                display_text = f"{label}\n{text_preview}"
            
            # Draw text background
            text_lines = display_text.split('\n')
            max_width = max([draw.textlength(line, font=font) for line in text_lines])
            text_height = len(text_lines) * 20  # Approximate line height
            
            draw.rectangle(
                [bbox[0], bbox[1] - text_height - 4, bbox[0] + max_width + 4, bbox[1]], 
                fill=color
            )
            
            # Draw text
            y_offset = bbox[1] - text_height - 2
            for line in text_lines:
                draw.text((bbox[0] + 2, y_offset), line, fill="white", font=font)
                y_offset += 20
        
        return draw_image

    def process_and_save(self, image_path, output_json_path="document_analysis.json", 
                        visualize=True, save_visualization=None, save_crops=False):
        """Complete pipeline with visualization and saving"""
        
        print(f"Processing document: {image_path}")
        print(f"Confidence threshold: {self.confidence_threshold}")
        
        # Load the original image
        image = Image.open(image_path).convert("RGB")
        
        # Process the document
        results = self.process_document(image_path, save_crops=save_crops)
        
        if not results:
            print("No regions found for processing.")
            return None
        
        # Save results to JSON
        output_data = self.save_results_to_json(results, output_json_path, image_path)
        
        # Create visualization
        if visualize or save_visualization:
            result_image = self.draw_boxes_with_text(image, results)
            
            if visualize:
                plt.figure(figsize=(15, 10))
                plt.imshow(result_image)
                plt.axis('off')
                plt.title(f"Document Layout Detection & OCR Results\n{len(results)} regions processed")
                plt.tight_layout()
                plt.show()
            
            if save_visualization:
                result_image.save(save_visualization)
                print(f"Visualization saved to: {save_visualization}")
        
        return output_data

# Example usage
if __name__ == "__main__":
    # Initialize detector with OCR
    detector = LayoutDetectorWithOCR(
        layout_model_path="/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/models/doclayout_yolo_docstructbench_imgsz1024.pt",
        confidence_threshold=0.25
    )
    
    # Process document
    image_path = "/share/users/ahmed_heakl/ymk/OCR/OCR/OCR_benchmarking/testing_images/13026818_section_219_portrait_one_col_arabic_template_0_image_0.png"
    
    try:
        # Run complete pipeline
        results = detector.process_and_save(
            image_path=image_path,
            output_json_path="document_analysis_results.json",
            visualize=True,
            save_visualization="layout_detection_with_ocr.jpg",
            save_crops=True  # Set to True if you want to save cropped regions
        )
        
        print("\n" + "="*50)
        print("PROCESSING COMPLETE!")
        print("="*50)
        print(f"Total regions processed: {len(results['results']) if results else 0}")
        
        if results:
            print("\nSummary by region type:")
            for region_type, count in results['summary']['regions_by_type'].items():
                print(f"  {region_type}: {count} regions")
        
    except FileNotFoundError:
        print("Please update the image_path variable with the correct path to your image file")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()