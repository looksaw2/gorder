### 生成proto的python代码

import os
import subprocess
import sys
from pathlib import Path

## API的路径
API_ROOT = Path("./api")
GO_OUT_DIR = Path("internal/common/genproto")
PROTOC_INCLUDE = "/usr/local/include/"


### 检查是否从项目的根路径运行
def check_run_from_root():
    script_path = Path(__file__).resolve()
    if not str(script_path).endswith("scripts/genproto.py"):
        print("Please run this script from the project root directory.")
        sys.exit(255)
        
def find_proto_dirs():
    """返回所有包含 .proto 文件的唯一目录名（去重）"""
    proto_dirs = set()
    for proto_file in Path(".").rglob("*.proto"):
        proto_dirs.add(proto_file.parent.name)
    return sorted(proto_dirs)

def find_proto_files():
    """返回所有 .proto 文件的路径"""
    return list(Path(".").rglob("*.proto"))

def clean_genproto_dir():
    """清理生成目录"""
    if GO_OUT_DIR.exists():
        print(f"Cleaning existing {GO_OUT_DIR}...")
        for item in GO_OUT_DIR.glob("*"):
            if item.is_dir():
                subprocess.run(["rm", "-rf", str(item)], check=True)
            else:
                item.unlink()
    else:
        GO_OUT_DIR.mkdir(parents=True, exist_ok=True)

def run_protoc(proto_dir):
    """调用 protoc 生成代码"""
    service = proto_dir[:-2]  # 假设目录名格式为 'servicev1'
    proto_file = f"{service}.proto"
    proto_path = API_ROOT / proto_dir / proto_file

    print(f"Generating code for {service}...")
    subprocess.run([
        "protoc",
        f"-I={PROTOC_INCLUDE}",
        f"-I={API_ROOT}",
        f"--go_out={GO_OUT_DIR}",
        "--go_opt=paths=source_relative",
        "--go-grpc_opt=require_unimplemented_servers=false",
        f"--go-grpc_out={GO_OUT_DIR}",
        "--go-grpc_opt=paths=source_relative",
        str(proto_path)
    ], check=True)

def main():
    check_run_from_root()
    clean_genproto_dir()

    proto_dirs = find_proto_dirs()
    proto_files = find_proto_files()

    print(f"Directories containing protos: {proto_dirs}")
    print(f"Proto files: {[str(f) for f in proto_files]}")

    for dir_name in proto_dirs:
        run_protoc(dir_name)

    print("Protoc generation completed successfully!")

if __name__ == "__main__":
    main()