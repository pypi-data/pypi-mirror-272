import onnx
model = onnx.load('./model/chinese-bert-wwm-ext.onnx')
outputs = model.graph.output
for output in outputs:
    print(output.name)