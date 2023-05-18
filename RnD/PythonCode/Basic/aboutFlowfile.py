import json
import java.io
from org.apache.commons.io import IOUtils
from java.nio.charset import StandardCharsets
from org.apache.nifi.processor.io import StreamCallback,InputStreamCallback, OutputStreamCallback

class OutputWrite(OutputStreamCallback, obj):

def __init__(self):
    self.obj = obj

def process(self, outputStream):

    outputStream.write(bytearray(json.dumps(self.obj).encode('utf')))

###end class###

flowfile = session.get()

if flowfile != None:

    #1)Get Flowfile attribute**
    collection = flowfile.getAttribute('collection')
    dataset = flowfile.getAttribute('dataset')

    #2)Get flowfile content**

    stream_content = session.read(flowfile)
    text_content = IOUtils.toString(stream_content, StandardCharsets.UTF_8)
    json_content = json.loads(text_content)

    records = json_content['result']['count']
    pages = records/10000

    #3) Write flowfile attributes**

    flowfile = session.putAttribute(flowfile, 'collection', collection)
    flowfile = session.putAttribute(flowfile, 'dataset', dataset)

    **#API operations: output_json with desired data**

    output_json = {some data}

    #4) Write final JSON data to output flowfile**

    flowfile = session.write(flowfile, OutputWrite(output_json))

    session.transfer(flowfile, REL_SUCCESS)
    session.commit()