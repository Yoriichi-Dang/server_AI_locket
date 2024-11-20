
class CaptionService:
    def __init__(self):
        pass
    def vqa(self,image,question):
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        model_id = 'damo/mplug_visual-question-answering_coco_large_en'
        input_vqa = {
            'image': image,
            'question': question,
        }

        pipeline_vqa = pipeline(Tasks.visual_question_answering, model=model_id)
        return (pipeline_vqa(input_vqa)["text"])

    def image_caption(self,image):
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks

        model_id = 'damo/mplug_image-captioning_coco_large_en'
        input_caption = image

        pipeline_caption = pipeline(Tasks.image_captioning, model=model_id)
        result = pipeline_caption(input_caption)
        return result['caption']

    def image_text_retrieval(self,image_inputs,question_input):
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        from PIL import Image
        import matplotlib.pyplot as plt

        # Initialize the retrieval pipeline
        model = 'damo/mplug_image-text-retrieval_flickr30k_large_en'
        pipeline_retrieval = pipeline(Tasks.image_text_retrieval, model=model)

        # Define image file paths and the query
        images = image_inputs
        query = question_input

        # Perform retrieval by comparing the query with each image
        results = []
        for image_path in images:
            input_data = {'image': image_path, 'question': query}
            result = pipeline_retrieval(input_data)
            results.append({'image': image_path, 'score': result['scores'][1]})  # Adjust index for score if necessary

        # Find the image with the highest score
        best_result = max(results, key=lambda x: x['score'])
        return best_result["image"]
