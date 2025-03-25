# 前端应用程序

这个前端项目旨在提升 GPT-Researcher 的用户体验，提供直观且高效的自动化研究界面。它提供两种部署选项，以满足不同的需求和环境。

## 选项 1：静态前端（FastAPI）

这是一个使用 FastAPI 提供静态文件服务的轻量级解决方案。

### 前提条件
- Python 3.11+
- pip

### 设置和运行

1. 安装所需的依赖项：
   ```
   pip install -r requirements.txt
   ```

2. 启动服务器：
   ```
   python -m uvicorn main:app
   ```

3. 访问地址：`http://localhost:8000`

### 演示
[查看演示](https://github.com/assafelovic/gpt-researcher/assets/13554167/dd6cf08f-b31e-40c6-9907-1915f52a7110)

---

## 选项 2：NextJS 前端

这是一个功能更丰富、性能更优的解决方案。

### 前提条件
- Node.js（推荐版本 v18.17.0）
- npm

### 设置和运行

1. 进入 NextJS 目录：
   ```
   cd nextjs
   ```

2. 设置 Node.js 版本：
   ```
   nvm install 18.17.0
   nvm use v18.17.0
   ```

3. 安装依赖项：
   ```
   npm install --legacy-peer-deps
   ```

4. 启动开发服务器：
   ```
   npm run dev
   ```

5. 访问地址：`http://localhost:3000`

> 注意：需要先运行选项 1 中的后端服务器（默认地址 `localhost:8000`）。

### 演示
[查看演示](https://github.com/user-attachments/assets/092e9e71-7e27-475d-8c4f-9dddd28934a3)

---

## 如何选择

- **静态前端**：部署快速，轻量级解决方案。  
- **NextJS 前端**：功能丰富、可扩展、性能更优，适合生产环境。  

生产环境推荐使用 NextJS 前端。

---

## 前端功能亮点

我们的前端为 GPT-Researcher 提供了以下增强功能：

1. **直观的研究界面**：简化研究查询的输入过程。  
2. **实时进度跟踪**：提供研究任务的实时可视化反馈。  
3. **交互式结果展示**：清晰、易于导航的研究结果展示。  
4. **自定义设置**：灵活调整研究参数，以适应不同需求。  
5. **响应式设计**：在各种设备上提供优化的使用体验。  

这些功能旨在让研究过程更高效、更人性化，与 GPT-Researcher 强大的多智能体能力相得益彰。