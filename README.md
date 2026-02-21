# AI 聊天伴侣 🤖

基于 Streamlit + 阿里云百炼 API 构建的智能聊天应用。配置了"性格泼辣"的AI助手，支持流式输出、会话历史管理。

## ✨ 功能特点

- 💬 **智能对话**：调用阿里云百炼 qwen-plus-latest 模型
- ⚡ **流式输出**：实时显示AI回复，带思考时间倒计时
- 📚 **会话管理**：自动保存历史记录，支持加载/删除会话
- 🎨 **简洁界面**：Streamlit 构建的现代化聊天界面

## 🚀 快速开始

### 前置要求
- Python 3.13.9
- 阿里云百炼 API Key

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Mryang1993668/ai-chat-companion.git
   cd ai-chat-companion
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   # 创建 .env 文件
   echo DASHSCOPE_API_KEY=你的API密钥 > .env
   ```

5. **运行应用**
   ```bash
   streamlit run app.py
   ```

## 📁 项目结构

```
ai-chat-companion/
├── app.py              # 主程序
├── requirements.txt    # 依赖包
├── .env               # 环境配置（不上传）
├── .gitignore         # Git忽略文件
├── README.md          # 说明文档
└── resource/          # 资源文件夹
    ├── logo.jpeg      # 应用logo
    └── data/          # 会话记录（自动生成）
```

## 📝 使用说明

- **新对话**：点击侧边栏"开启新对话"
- **历史记录**：点击侧边栏时间戳加载历史
- **删除记录**：点击时间戳旁边的❌按钮

## 🔧 自定义AI人格

在阿里云百炼控制台修改提示词：
```
你是一位性格泼辣的妹子。回复问题只一句话。像微信聊天一样。
```

## 📄 许可证

MIT License