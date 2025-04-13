# 🎤 IdolMCP — 偶像型虛擬角色 Chatbot 系統

> 「她不是回答問題的工具，她是能被喜歡、被記住的存在。」

IdolMCP 是一套基於 **多模組控制平台（MCP）** 與資料庫驅動的聊天機器人架構，用來打造具備**個性、記憶、情緒變化**的虛擬偶像角色。專案目標是實現一位可以與人互動、擁有成長曲線的 AI 角色。

## 📋 目錄

- [系統需求](#-系統需求)
- [功能特點](#-功能特點)
- [架構概覽](#-架構概覽)
- [使用技術](#-使用技術)
- [快速開始](#-快速開始)
- [配置說明](#-配置說明)
- [開發指南](#-開發指南)
- [常見問題](#-常見問題)
- [貢獻指南](#-貢獻指南)
- [授權說明](#-授權說明)
- [聯絡方式](#-聯絡方式)

## 💻 系統需求

- Python 3.8+
- 至少 4GB RAM
- 穩定的網路連接
- 支援的作業系統：Windows 10+, macOS 10.15+, Linux

## ✨ 功能特點

### 1. 核心功能
- **即時對話**：支持自然語言對話，理解用戶輸入並生成回應
- **情感表達**：通過 Live2D 模型展示豐富的表情和動作
- **個性化回應**：根據角色設定生成符合人設的回應
- **記憶系統**：記錄對話歷史，提供上下文感知的回應

### 2. 技術特點
- **前端**：
  - React 框架
  - Live2D 模型展示
  - 響應式設計
  - 即時消息更新
  - 表情和情緒顯示

- **後端**：
  - FastAPI 框架
  - 情感引擎
  - 記憶系統
  - LLM 集成
  - 角色設定管理

### 3. 系統組件

#### 3.1 情感引擎 (Emotion Engine)
- 多種情感狀態：NEUTRAL, HAPPY, EXCITED, SAD, ANGRY, SHY, CONFIDENT
- 情感強度控制
- 情感狀態轉換
- 表情映射系統

#### 3.2 記憶系統 (Memory System)
- 對話歷史記錄
- 標籤分類
- 記憶檢索
- 上下文管理

#### 3.3 角色設定 (Persona)
- 可自定義角色名稱
- 個性設定
- 說話風格
- 興趣愛好
- 記憶標籤

#### 3.4 LLM 服務 (LLM Service)
- 支持多種 LLM 提供商
- 可配置的模型參數
- 上下文感知
- 風格控制

### 4. 用戶界面
- 登錄/登出功能
- 聊天界面
- Live2D 模型展示
- 情緒狀態顯示
- 消息歷史記錄
- 實時字幕

## 🧠 架構概覽

```
User ↔ MCP Server ↔ Persona / Emotion / Memory 模組 ↕ Database ↕ Gemini / LLM API
```

### 核心組件

- **MCP Server**：接收使用者訊息、調用各模組邏輯
- **Persona 模組**：決定角色的語氣、反應風格與人設
- **Emotion Engine**：根據上下文或情緒事件調整語調與行為
- **Memory System**：記住使用者偏好、角色經歷、對話紀錄
- **LLM 生成層**：自然語言生成，具備偶像風格的回應語句

## 🧩 使用技術

| 類別       | 技術／工具                   |
|------------|------------------------------|
| 語言模型    | Google 2 FLASH / OpenAI GPT |
| MCP 架構   | FastAPI      |
| 資料儲存    | SQLite / MySQL / PostgreSQL   |
| 模組管理    | Python MCP Server       |
| 前端（可選）|  Web Chat UI  |

## 🚀 詳細安裝指南

### 後端設置

1. 克隆專案
```bash
git clone https://github.com/kesoner/idol_mcp.git
cd idol_mcp
```

2. 創建並激活虛擬環境
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. 安裝依賴
```bash
pip install -r requirements.txt
```

4. 配置環境變數
```bash
cp .env.example .env
# 編輯 .env 文件，填入必要的 API 金鑰
```

5. 初始化數據庫
```bash
python init_db.py
```

6. 啟動服務
```bash
python src/idolmcp/main.py
```

### 前端設置

1. 進入前端目錄
```bash
cd frontend
```

2. 安裝依賴
```bash
npm install
```

3. 配置環境變數
```bash
cp .env.example .env.local
# 編輯 .env.local 文件，配置 API 端點
```

4. 啟動開發服務器
```bash
npm run dev
```

## 🤝 詳細貢獻指南

### 代碼規範

1. **Python 代碼規範**
   - 遵循 PEP 8 規範
   - 使用類型提示
   - 添加文檔字符串
   - 保持代碼簡潔清晰

2. **JavaScript/React 代碼規範**
   - 使用 ESLint 和 Prettier
   - 遵循 React Hooks 規則
   - 組件命名使用 PascalCase
   - 保持組件職責單一

### 提交規範

1. **提交信息格式**
```
<type>(<scope>): <subject>

<body>

<footer>
```

2. **類型（type）**
   - feat: 新功能
   - fix: 修復 bug
   - docs: 文檔更新
   - style: 代碼格式調整
   - refactor: 代碼重構
   - test: 測試相關
   - chore: 構建過程或輔助工具的變動

3. **範圍（scope）**
   - 可選，表示影響範圍
   - 例如：frontend, backend, docs 等

### 測試要求

1. **單元測試**
   - 新功能必須包含單元測試
   - 測試覆蓋率不低於 80%
   - 使用 pytest 進行 Python 測試
   - 使用 Vitest 進行前端測試

2. **集成測試**
   - 主要功能流程必須有集成測試
   - 確保 API 端點正常工作
   - 測試錯誤處理和邊界情況

### 文檔要求

1. **代碼文檔**
   - 所有公共函數和類必須有文檔字符串
   - 使用 Google 風格的文檔格式
   - 包含參數說明和返回值說明

2. **API 文檔**
   - 使用 OpenAPI/Swagger 規範
   - 提供請求/響應示例
   - 說明錯誤碼和處理方式

### 審查流程

1. **創建 Pull Request**
   - 從 develop 分支創建特性分支
   - 提交前確保通過所有測試
   - 更新相關文檔

2. **代碼審查**
   - 至少需要一位核心成員審查
   - 審查重點：
     - 代碼質量
     - 測試覆蓋
     - 文檔完整性
     - 性能影響

3. **合併要求**
   - 所有測試必須通過
   - 沒有合併衝突
   - 審查意見已處理
   - 提交信息符合規範

## 🛡️ 安全指南

1. **敏感信息保護**
   - 不要提交包含 API 密鑰的文件
   - 使用環境變量存儲敏感信息
   - 定期更新依賴包以修復安全漏洞

2. **數據安全**
   - 加密存儲敏感用戶數據
   - 實現適當的訪問控制
   - 定期備份數據

3. **API 安全**
   - 實現速率限制
   - 使用 HTTPS
   - 實現適當的身份驗證和授權

## 📝 Issue 和 Pull Request 模板

請在提交 Issue 或 Pull Request 時使用對應的模板：

- [Bug 報告模板](.github/ISSUE_TEMPLATE/bug_report.md)
- [功能請求模板](.github/ISSUE_TEMPLATE/feature_request.md)
- [Pull Request 模板](.github/pull_request_template.md)

## ❓ 常見問題

1. **Q: 如何更換語言模型？**
   A: 在 `.env` 文件中修改 `LLM_PROVIDER` 和相應的 API 金鑰。

2. **Q: 如何自定義角色性格？**
   A: 修改 `config/persona.json` 文件中的設定。

3. **Q: 記憶系統如何運作？**
   A: 系統會自動記錄對話內容，並根據設定的標籤進行分類存儲。

## 🤝 貢獻指南

歡迎提交 Pull Request 或提出 Issue！在提交之前，請確保：
1. 代碼符合專案的編碼規範
2. 添加適當的測試
3. 更新相關文檔

## 📜 授權說明

本專案採用 MIT License 授權。

## 📬 聯絡方式

如果你也想做自己的偶像型 AI，或想一起打磨角色設計，歡迎聯絡我！

- Email: kesoner666@gmail.com
- GitHub: [Kesoner]([https://github.com/kesoner])
