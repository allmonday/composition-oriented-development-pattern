# 使用 Python 3.12 作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirement.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirement.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动 uvicorn 服务
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
