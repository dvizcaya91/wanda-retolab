def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """OCR with PDF/TIFF as source files on GCS"""
    import re
    from google.cloud import vision
    from google.cloud import storage
    from google.protobuf import json_format
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'

    # How many pages should be grouped into each json output file.
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())

    # The actual response for the first page of the input file.
    first_page_response = response.responses[0]
    annotation = first_page_response.full_text_annotation

    # Here we print the full text from the first page.
    # The response contains more information:
    # annotation/pages/blocks/paragraphs/words/symbols
    # including confidence scores and bounding boxes
    print(u'Full text:\n{}'.format(
        annotation.text))

    # open('result_test.txt', 'w').write(annotation.text)


def process_result(text):
    from difflib import get_close_matches

    #text = open('result_test.txt', 'r').read()
    text = text.split('\n')

    fields = {
        "date":"Fecha",
        "product":"Producto",
        "price":"Precio",
        "user_id":"Cedula",
        "user_gender":"Genero",
        "companion_type":"Acompañantes",
        "type_of_traveler":"Tipo",
        "origin":"Origen"
    }

    results = {"category":"Naturaleza",
               "subsector": "Operador",
               "location": "Magdalena",
               "companion_gender": "NA",
               "sons_age": 0,
               "travel_reason": "Vacaciones",
               }
    for key, f in fields.items():

        for t in text:
            if f in t:
                if ':' in t:
                    results[key] = t.split(':')[1]
                elif ' ':
                    results[key] = t.split(' ')[1]
            elif get_close_matches(f, t.split(' ')):
                results[key] = t.split(' ')[1:]
                results[key] = ' '.join(results[key])
    print(results)

    return results

if __name__ == '__main__':
    #async_detect_document('gs://wanda_vision_images/test_1.pdf', 'gs://wanda_vision_images/result')
    process_result('a')