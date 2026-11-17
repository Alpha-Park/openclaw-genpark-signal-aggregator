# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkSignalAggregator

client = OpenClawGenParkSignalAggregator()

TOOLS = [
    {
        "name": "apply_kalman_filter",
        "description": "Applies 1D discrete Kalman filter to track latent market/agent signals from noisy data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "measurements": {"type": "array", "items": {"type": "number"}},
                "process_variance": {"type": "number"},
                "measurement_variance": {"type": "number"}
            },
            "required": ["measurements"]
        }
    },
    {
        "name": "detect_volatility_and_regime_bursts",
        "description": "Detects anomalous volatility bursts or regime shifts using rolling Z-score.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "time_series": {"type": "array", "items": {"type": "number"}},
                "window_size": {"type": "integer"},
                "z_threshold": {"type": "number"}
            },
            "required": ["time_series"]
        }
    },
    {
        "name": "compute_shannon_entropy_gain",
        "description": "Calculates Shannon information entropy reduction and uncertainty bits gained.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prior_probs": {"type": "array", "items": {"type": "number"}},
                "posterior_probs": {"type": "array", "items": {"type": "number"}}
            },
            "required": ["prior_probs", "posterior_probs"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "apply_kalman_filter":
            res = client.apply_kalman_filter(args["measurements"], args.get("process_variance"), args.get("measurement_variance"))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "detect_volatility_and_regime_bursts":
            res = client.detect_volatility_and_regime_bursts(args["time_series"], args.get("window_size", 10), args.get("z_threshold", 2.5))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "compute_shannon_entropy_gain":
            res = client.compute_shannon_entropy_gain(args["prior_probs"], args["posterior_probs"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}), flush=True)
                continue
            if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str):
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}), flush=True)
                continue
            # JSON-RPC notifications never receive a response or execute request-only tools.
            if "id" not in req:
                continue
            if req["method"] == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": 'openclaw-genpark-signal-aggregator', "version": "1.0.0"}
                }}), flush=True)
                continue
            if req["method"] == "ping":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}), flush=True)
                continue
            if req["method"] not in ("tools/list", "tools/call"):
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": "Method not found"}}), flush=True)
                continue
            if req["method"] == "tools/call":
                params = req.get("params")
                if not isinstance(params, dict) or not isinstance(params.get("arguments", {}), dict) or params.get("name") not in ('apply_kalman_filter', 'detect_volatility_and_regime_bursts', 'compute_shannon_entropy_gain'):
                    print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": "Unknown tool or invalid arguments"}}), flush=True)
                    continue
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
