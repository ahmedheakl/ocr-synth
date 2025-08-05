"""
Script to convert the generated synthetic data into Huggingface format.
"""

from synthetic_data_generation.serializer.json_to_hfds_serializer import JsonToHfdsSerializer

def main():
    JsonToHfdsSerializer().gen_hf_dataset()

if ("__main__" == __name__):
    main()
