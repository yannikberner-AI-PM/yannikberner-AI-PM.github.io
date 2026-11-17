import AppKit
import WebKit

let args = CommandLine.arguments
let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
class Capture: NSObject, WKNavigationDelegate {
    var web: WKWebView!
    var window: NSWindow!
    func start() {
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .nonPersistent()
        web = WKWebView(frame: NSRect(x:0,y:0,width:1680,height:1300), configuration:config)
        web.navigationDelegate = self
        web.pageZoom = 0.85
        window = NSWindow(contentRect:web.frame, styleMask:[.borderless], backing:.buffered, defer:false)
        window.contentView = web
        let rules = #"[{"trigger":{"url-filter":"^https?://"},"action":{"type":"block"}},{"trigger":{"url-filter":"^http://127[.]0[.]0[.]1:4198/"},"action":{"type":"ignore-previous-rules"}}]"#
        WKContentRuleListStore.default().compileContentRuleList(forIdentifier:"capture-loopback-only", encodedContentRuleList:rules) { list,error in
            guard let list=list else { print(String(describing:error));exit(4) }
            self.web.configuration.userContentController.add(list)
            self.web.load(URLRequest(url:URL(string:CommandLine.arguments[1])!))
        }
    }
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline:.now()+1) {
            let script = try! String(contentsOfFile:CommandLine.arguments[2], encoding:.utf8)
            self.web.evaluateJavaScript(script) { result,error in
                if let error = error { print(error); exit(1) }
                print(String(describing:result))
                DispatchQueue.main.asyncAfter(deadline:.now()+0.5) {
                    let snapshot = WKSnapshotConfiguration()
                    if let dict = result as? [String:Any], let rect = dict["capture"] as? [String:Double] {
                        snapshot.rect = NSRect(x:rect["x"]!*0.85,y:rect["y"]!*0.85,width:rect["width"]!*0.85,height:rect["height"]!*0.85)
                    }
                    self.web.takeSnapshot(with:snapshot) { image,error in
                        guard let image=image, let tiff=image.tiffRepresentation, let bitmap=NSBitmapImageRep(data:tiff), let png=bitmap.representation(using:.png,properties:[:]) else { print(String(describing:error));exit(2) }
                        try! png.write(to:URL(fileURLWithPath:CommandLine.arguments[3]))
                        print("Saved \(bitmap.pixelsWide)x\(bitmap.pixelsHigh)")
                        exit(0)
                    }
                }
            }
        }
    }
}
let capture=Capture()
capture.start()
DispatchQueue.main.asyncAfter(deadline:.now()+20) { print("Capture timeout");exit(3) }
app.run()
