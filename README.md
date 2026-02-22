# AI 聊天伴侣 🤖

基于 Streamlit + 阿里云百炼 API 构建的智能聊天应用。支持自定义AI角色、流式输出、会话历史管理。

## ✨ 功能特点

- 💬 **智能对话**：调用阿里云百炼 qwen-plus 模型
- ⚡ **流式输出**：实时显示AI回复，模拟打字效果
- 🎭 **自定义角色**：可随时修改AI性格、语气和说话方式
- 📚 **会话管理**：自动保存历史记录，支持加载/删除会话
- 🎨 **简洁界面**：Streamlit 构建的现代化聊天界面

## 🚀 快速开始

### 前置要求
- Python 3.8+
- 阿里云百炼 API Key

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/Mryang1993668/ai-chat-companion.git
   cd ai-chat-companion
创建虚拟环境

bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
安装依赖

bash
pip install -r requirements.txt
配置环境变量

bash
# 创建 .env 文件
echo DASHSCOPE_API_KEY=你的API密钥 > .env
运行应用

bash
streamlit run app_new.py
📁 项目结构
text
ai-chat-companion/
├── app_new.py          # 主程序（新版本）
├── app.py              # 旧版本（可选）
├── requirements.txt    # 依赖包
├── .env               # 环境配置（不上传）
├── .gitignore         # Git忽略文件
├── README.md          # 说明文档
└── resource/          # 资源文件夹
    ├── logo.jpeg      # 应用logo
    └── data/          # 会话记录（自动生成）
        └── *.json     # 历史会话文件
📝 使用说明
基本聊天
在底部输入框输入消息，按回车发送

AI 会实时流式回复，模拟打字效果

自定义AI角色
在侧边栏的"AI角色"文本框中修改角色设定

修改后发送任意消息即可生效

示例角色：

text
你叫小甜甜，你是一位温柔可爱的姑娘，请用微信聊天的方式与用户聊天
或

text
你是一位性格泼辣的妹子，回复问题只一句话，像微信聊天一样
会话管理
开启新对话：点击侧边栏"开启新对话"按钮

查看历史：侧边栏显示所有保存的会话（按时间命名）

加载历史：点击会话时间戳加载之前的对话

删除历史：点击会话右侧的❌按钮删除

⚙️ 技术细节
API调用方式
python
responses = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus",
    messages=st.session_state.messages,  # 包含system、user、assistant消息
    result_format='message',
    stream=True,
    incremental_output=True
)
会话存储格式
json
{
    "current_time": "20231201143022",
    "messages": [
        {"role": "system", "content": "角色设定..."},
        {"role": "user", "content": "用户消息"},
        {"role": "assistant", "content": "AI回复"}
    ]
}
📦 依赖项
text
streamlit>=1.28.0
dashscope>=1.14.0
python-dotenv>=1.0.0
🔧 版本更新
v2.0 (app_new.py)
✨ 新增侧边栏实时修改AI角色功能

🎯 优化system消息处理逻辑

🚀 简化API调用，移除冗余代码

💾 完善会话历史持久化存储

v1.0 (app.py)
基础聊天功能

流式输出

会话历史管理

📄 许可证
MIT License

text

主要修改内容：
1. 更新了功能特点（强调自定义角色）
2. 将运行文件改为 `app_new.py`
3. 增加了"自定义AI角色"使用说明
4. 添加了技术细节（API调用和存储格式）
5. 增加了版本更新记录
6. 更新了依赖版本信息