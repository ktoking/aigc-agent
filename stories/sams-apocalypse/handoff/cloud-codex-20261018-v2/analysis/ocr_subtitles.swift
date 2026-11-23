import Foundation
import Vision
import ImageIO
let input=URL(fileURLWithPath:CommandLine.arguments[1])
let files=try FileManager.default.contentsOfDirectory(at:input, includingPropertiesForKeys:nil).filter{$0.pathExtension=="png"}.sorted{$0.lastPathComponent < $1.lastPathComponent}
var results:[[String:Any]]=[]
for (index,url) in files.enumerated() {
  try autoreleasepool {
    let request=VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.recognitionLanguages=["zh-Hans","en-US"]
    request.usesLanguageCorrection=false
    try VNImageRequestHandler(url:url).perform([request])
    let items=(request.results ?? []).compactMap{r -> [String:Any]? in
      guard let c=r.topCandidates(1).first else {return nil}
      return ["text":c.string,"confidence":c.confidence,"y":r.boundingBox.origin.y,"height":r.boundingBox.height]
    }
    results.append(["index":index,"time":Double(index)/5,"file":url.lastPathComponent,"items":items])
  }
}
let bytes=try JSONSerialization.data(withJSONObject:results,options:[.prettyPrinted,.sortedKeys,.withoutEscapingSlashes])
try bytes.write(to:URL(fileURLWithPath:CommandLine.arguments[2]))
print("OCR frames: \(results.count)")
