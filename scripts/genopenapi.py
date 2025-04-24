#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

# 配置参数
OPENAPI_ROOT = Path("./api/openapi")
GEN_SERVER = ["gin-server"]
OUTPUT_BASE = Path("internal/common/client")

def get_go_bin_path():
    """获取Go二进制路径"""
    try:
        # 方法1：检查常见的Go安装路径
        go_paths = [
            os.path.expanduser("~/go/bin"),
            "/usr/local/go/bin",
            str(subprocess.run(["go", "env", "GOPATH"], 
                              check=True, 
                              capture_output=True, 
                              text=True).stdout).strip() + "/bin"
        ]
        
        for path in go_paths:
            if (Path(path)/"oapi-codegen").exists():
                return path
        
        # 方法2：通过which查找
        which_path = subprocess.run(["which", "oapi-codegen"],
                                  capture_output=True,
                                  text=True)
        if which_path.returncode == 0:
            return str(Path(which_path.stdout.strip()).parent)
        
    except Exception:
        pass
    
    return None

def check_oapi_codegen():
    """检查oapi-codegen是否可用"""
    go_bin_path = get_go_bin_path()
    if go_bin_path:
        # 将Go二进制路径临时添加到PATH
        env = os.environ.copy()
        env["PATH"] = f"{go_bin_path}:{env['PATH']}"
        return env
    
    print("\nERROR: oapi-codegen not found in PATH", file=sys.stderr)
    print("Possible solutions:", file=sys.stderr)
    print("1. Install oapi-codegen:", file=sys.stderr)
    print("   go install github.com/deepmap/oapi-codegen/v2/cmd/oapi-codegen@latest", file=sys.stderr)
    print("2. Ensure your Go bin directory is in PATH", file=sys.stderr)
    print(f"   Current PATH: {os.getenv('PATH')}", file=sys.stderr)
    sys.exit(1)

def run_oapi_codegen(env, *args):
    """运行oapi-codegen命令"""
    cmd = ["oapi-codegen"] + list(args)
    try:
        result = subprocess.run(cmd, 
                              check=True,
                              env=env,
                              capture_output=True,
                              text=True)
        print(f"[SUCCESS] {' '.join(cmd)}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(f"Exit code: {e.returncode}", file=sys.stderr)
        print(f"Error output:\n{e.stderr}", file=sys.stderr)
        sys.exit(1)

def main():
    # 检查运行环境和工具
    env = check_oapi_codegen()
    
    # 示例调用
    run_oapi_codegen(
        env,
        "-generate", "types",
        "-o", "internal/order/ports/openapi_types.gen.go",
        "-package", "ports",
        "api/openapi/order.yml"
    )
    
    run_oapi_codegen(
        env,
        "-generate", "gin-server",
        "-o", "internal/order/ports/openapi_types.gen.go",
        "-package", "ports",
        "api/openapi/order.yml"
    )
    run_oapi_codegen(
        env,
        "-generate", "types",
        "-o", "internal/common/client/order/openapi_types.gen.go",
        "-package", "order",
        "api/openapi/order.yml"
    )
    run_oapi_codegen(
        env,
        "-generate", "client",
        "-o", "internal/common/client/order/openapi_client.gen.go",
        "-package", "order",
        "api/openapi/order.yml"
    )
    

if __name__ == "__main__":
    main()